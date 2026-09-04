from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from the_six_stage_forge.gated_pipeline import GatedForgePipeline, GateError, STAGES

st.set_page_config(page_title="Six Stage Forge", page_icon="🔥", layout="wide")

st.title("🔥 Six Stage Forge — Hard-Gated Web App")
st.caption("A stage cannot advance until its completed WORK passes validation and is committed to the next stage.")

with st.sidebar:
    st.header("Runtime")
    model = st.text_input(
        "LLM model",
        value=os.getenv("FORGE_MODEL", "openai/deepseek-ai/DeepSeek-V3.1"),
        help="Featherless model routed through its OpenAI-compatible API. The openai/ prefix is used internally by LiteLLM.",
    )
    api_key = st.text_input(
        "API key override (optional)",
        value="",
        type="password",
        help="Normally leave blank: start_webapp.bat loads your saved Featherless key from .env.",
    )
    validation_retries = st.number_input("Gate retries per stage", min_value=0, max_value=10, value=2, step=1)
    minimum_work_chars = st.number_input("Minimum WORK characters", min_value=1, max_value=10000, value=20, step=1)
    verbose = st.checkbox("Verbose CrewAI logs", value=True)

    st.divider()
    st.markdown("**Preserved reasoning settings**")
    for spec in STAGES:
        st.caption(
            f"Stage {spec.number}: reasoning=True · reasoning attempts={spec.reasoning_attempts} · max_iter={spec.max_iter}"
        )

mission = st.text_area(
    "Mission / general prompt",
    height=130,
    placeholder="What should the six-stage forge ultimately accomplish?",
)
additional_context = st.text_area(
    "Additional context (optional)",
    height=100,
    placeholder="Constraints, background, preferences, environment details...",
)
raw_input = st.text_area(
    "Raw work to forge",
    height=320,
    placeholder="Paste the document, prompt, code, configuration, or other work here.",
)

uploaded = st.file_uploader("Or load raw work from a text/code file", type=None)
if uploaded is not None:
    try:
        uploaded_text = uploaded.getvalue().decode("utf-8")
        if st.button("Use uploaded file as raw work"):
            st.session_state["uploaded_work"] = uploaded_text
            st.rerun()
    except UnicodeDecodeError:
        st.error("This simple input loader expects a UTF-8 text/code file.")

if "uploaded_work" in st.session_state:
    raw_input = st.session_state["uploaded_work"]
    st.info("Uploaded file is loaded for the next run. You can clear it from the button below.")
    if st.button("Clear uploaded work"):
        del st.session_state["uploaded_work"]
        st.rerun()

run_clicked = st.button("Run all 6 gated stages", type="primary", use_container_width=True)

if run_clicked:
    if not raw_input.strip():
        st.error("Raw work cannot be empty.")
        st.stop()

    pipeline = GatedForgePipeline(
        model=model,
        api_key=api_key or None,
        validation_retries=int(validation_retries),
        minimum_work_chars=int(minimum_work_chars),
        verbose=verbose,
    )

    stage_boxes = []
    for spec in STAGES:
        stage_boxes.append(st.empty())

    latest = {}

    def update_stage(result):
        latest[result.stage] = result
        icon = {
            "RUNNING": "⏳",
            "RETRYING": "🔁",
            "VALIDATING": "🔎",
            "COMPLETED": "✅",
            "BLOCKED": "🛑",
        }.get(result.status, "•")
        message = f"{icon} **{result.label}** — {result.status}"
        if result.attempts:
            message += f" · attempt {result.attempts}"
        if result.error and result.status in {"RETRYING", "BLOCKED"}:
            message += f" · gate: `{result.error}`"
        stage_boxes[result.stage - 1].markdown(message)

    try:
        final_work, results = pipeline.run(
            mission=mission,
            raw_input=raw_input,
            additional_context=additional_context,
            on_stage_update=update_stage,
        )
    except GateError as exc:
        st.error(str(exc))
        st.warning("Pipeline stopped. No later stage was allowed to start after the failed gate.")
        partial = [r.to_dict() for _, r in sorted(latest.items())]
        st.download_button(
            "Download partial run log (JSON)",
            data=json.dumps(partial, indent=2),
            file_name="forge_partial_run.json",
            mime="application/json",
        )
        st.stop()
    except Exception as exc:
        st.exception(exc)
        st.stop()

    st.success("All six stages completed and passed their gates.")

    st.subheader("Final committed work")
    st.text_area("Stage 6 WORK", value=final_work, height=500)
    st.download_button(
        "Download final work",
        data=final_work,
        file_name="forge_final_work.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.subheader("Stage evidence")
    tabs = st.tabs([f"Stage {r.stage}" for r in results])
    for tab, result in zip(tabs, results):
        with tab:
            st.markdown(f"**Status:** {result.status}  \n**Attempts:** {result.attempts}")
            st.markdown("**Committed WORK**")
            st.code(result.work, language=None)
            st.markdown("**CHANGELOG**")
            st.code(result.changelog, language=None)
            with st.expander("Raw agent output"):
                st.code(result.raw_output, language=None)

    run_log = [r.to_dict() for r in results]
    st.download_button(
        "Download full run log (JSON)",
        data=json.dumps(run_log, indent=2),
        file_name="forge_run_log.json",
        mime="application/json",
    )
