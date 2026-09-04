from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Optional
import os
import re

import yaml
from crewai import Agent, Crew, LLM, Process, Task

WORK_DELIMITER = "---WORK---"
CHANGELOG_DELIMITER = "---CHANGELOG---"
COMPLETE_MARKER = "STATUS: COMPLETE"


@dataclass(frozen=True)
class StageSpec:
    number: int
    agent_key: str
    label: str
    reasoning_attempts: int
    max_iter: int
    instruction: str


@dataclass
class StageResult:
    stage: int
    label: str
    status: str
    work: str = ""
    changelog: str = ""
    raw_output: str = ""
    attempts: int = 0
    error: str = ""

    def to_dict(self):
        return asdict(self)


STAGES = [
    StageSpec(1, "first_stage_work_enhancer_and_fixer", "Stage 1 — Foundation repair", 1, 1,
              "Begin the forge. Fully inspect, repair, enhance, complete, and restructure the supplied work as needed."),
    StageSpec(2, "second_stage_work_enhancer_and_fixer", "Stage 2 — Deep refinement", 2, 3,
              "Go deeper. Find what Stage 1 missed, repair remaining weaknesses, fill gaps, and strengthen structure and logic."),
    StageSpec(3, "third_stage_work_enhancer_and_fixer", "Stage 3 — Logic and clarity", 3, 3,
              "Continue the forge. Rebuild weak areas, sharpen logic, improve clarity and depth, and fix anything still incomplete."),
    StageSpec(4, "fourth_stage_work_enhancer_and_fixer", "Stage 4 — Professional standard", 3, 3,
              "Push the work to professional standard. Catch prior omissions, tighten logic, elevate language, and ensure completeness."),
    StageSpec(5, "fifth_stage_work_enhancer_and_fixer", "Stage 5 — Airtight pass", 3, 3,
              "Treat this as near-final. Scrutinize every part, remove weakness or redundancy, and make the result coherent and airtight."),
    StageSpec(6, "sixth_stage_final_enhancer_and_delivery_agent", "Stage 6 — Final delivery", 3, 3,
              "Perform the ultimate final pass. Produce the definitive, implementation-ready result for the user."),
]


class GateError(RuntimeError):
    pass


class GatedForgePipeline:
    """Six-stage forge with deterministic stage boundaries.

    A later stage cannot execute until the current stage has returned output,
    passed deterministic validation, and had its WORK body committed as the
    sole work input to the following stage.
    """

    def __init__(
        self,
        model: str = "openai/deepseek-ai/DeepSeek-V3.1",
        api_key: Optional[str] = None,
        validation_retries: int = 2,
        minimum_work_chars: int = 20,
        verbose: bool = True,
    ):
        self.model = model.strip()
        self.validation_retries = max(0, int(validation_retries))
        self.minimum_work_chars = max(1, int(minimum_work_chars))
        self.verbose = verbose
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key.strip()

        config_path = Path(__file__).resolve().parent / "config" / "agents.yaml"
        with config_path.open("r", encoding="utf-8") as f:
            self.agents_config = yaml.safe_load(f)

    def _llm(self) -> LLM:
        return LLM(model=self.model)

    def _build_agent(self, spec: StageSpec) -> Agent:
        return Agent(
            config=self.agents_config[spec.agent_key],
            tools=[],
            reasoning=True,
            max_reasoning_attempts=spec.reasoning_attempts,
            inject_date=True,
            allow_delegation=False,
            max_iter=spec.max_iter,
            max_rpm=None,
            max_execution_time=None,
            llm=self._llm(),
            verbose=self.verbose,
        )

    @staticmethod
    def _normalise_output(value) -> str:
        for attr in ("raw", "output"):
            if hasattr(value, attr):
                candidate = getattr(value, attr)
                if candidate is not None:
                    return str(candidate)
        return str(value)

    def _parse_and_validate(self, raw: str) -> tuple[str, str]:
        text = raw.strip()
        if text.count(WORK_DELIMITER) != 1 or text.count(CHANGELOG_DELIMITER) != 1:
            raise GateError("Output must contain exactly one ---WORK--- and exactly one ---CHANGELOG--- delimiter.")

        work_idx = text.find(WORK_DELIMITER)
        changelog_idx = text.find(CHANGELOG_DELIMITER)
        if work_idx != 0:
            raise GateError("Nothing may appear before ---WORK---.")
        if changelog_idx <= work_idx:
            raise GateError("---CHANGELOG--- must appear after ---WORK---.")

        work = text[work_idx + len(WORK_DELIMITER):changelog_idx].strip()
        changelog = text[changelog_idx + len(CHANGELOG_DELIMITER):].strip()

        if len(work) < self.minimum_work_chars:
            raise GateError(f"WORK is too short to commit ({len(work)} characters; minimum is {self.minimum_work_chars}).")
        if not changelog:
            raise GateError("CHANGELOG is empty.")
        if COMPLETE_MARKER not in changelog.upper():
            raise GateError(f"CHANGELOG must contain '{COMPLETE_MARKER}'.")

        unfinished_patterns = [
            r"\bTODO\b",
            r"\bTBD\b",
            r"\bFIXME\b",
            r"\bPLACEHOLDER\b",
            r"\bINSERT\s+(?:HERE|LATER)\b",
            r"\bTO\s+BE\s+(?:COMPLETED|FILLED|ADDED)\b",
        ]
        for pattern in unfinished_patterns:
            if re.search(pattern, work, flags=re.IGNORECASE):
                raise GateError(f"WORK contains an unfinished marker matching: {pattern}")

        return work, changelog

    def _description(
        self,
        spec: StageSpec,
        mission: str,
        context: str,
        incoming_work: str,
        retry_feedback: str = "",
    ) -> str:
        source_label = "RAW INPUT" if spec.number == 1 else f"COMMITTED WORK FROM STAGE {spec.number - 1}"
        retry = ""
        if retry_feedback:
            retry = f"""

PREVIOUS ATTEMPT WAS REJECTED BY THE HARD GATE:
{retry_feedback}
Repair the output completely. Do not argue with the gate and do not return partial progress.
"""

        return f"""MISSION — always optimize for this goal:
{mission}

ADDITIONAL CONTEXT — use only when relevant:
{context or '(none)'}

STAGE {spec.number} RESPONSIBILITY:
{spec.instruction}

HARD COMPLETION CONTRACT:
- You are inside Stage {spec.number}. Do not describe future work for another stage.
- Do not return partial progress, drafts, placeholders, TODOs, TBDs, or unfinished sections.
- Finish this stage's work before answering.
- The next stage is physically blocked until this output passes validation.
- Return ONLY the two sections below, in this exact order, with nothing before ---WORK---.
- ---WORK--- must contain the entire completed artifact, not a summary of it and not instructions for someone else.
- ---CHANGELOG--- must state what you changed and MUST include the exact line: STATUS: COMPLETE

REQUIRED OUTPUT FORMAT:
---WORK---
<the complete artifact after this stage>
---CHANGELOG---
STATUS: COMPLETE
<precise changes made in this stage>

{source_label}:
{incoming_work}
{retry}""".strip()

    def run(
        self,
        mission: str,
        raw_input: str,
        additional_context: str = "",
        on_stage_update: Optional[Callable[[StageResult], None]] = None,
    ) -> tuple[str, list[StageResult]]:
        mission = (mission or "Improve, repair, complete, and refine the supplied work.").strip()
        current_work = (raw_input or "").strip()
        if not current_work:
            raise ValueError("Raw input cannot be empty.")

        results: list[StageResult] = []

        for spec in STAGES:
            result = StageResult(stage=spec.number, label=spec.label, status="RUNNING")
            if on_stage_update:
                on_stage_update(result)

            last_error = ""
            passed = False
            max_attempts = 1 + self.validation_retries

            for attempt in range(1, max_attempts + 1):
                result.attempts = attempt
                result.status = "RUNNING" if attempt == 1 else "RETRYING"
                if on_stage_update:
                    on_stage_update(result)

                agent = self._build_agent(spec)
                task = Task(
                    description=self._description(
                        spec,
                        mission=mission,
                        context=additional_context,
                        incoming_work=current_work,
                        retry_feedback=last_error,
                    ),
                    expected_output=(
                        "Exactly two sections: ---WORK--- containing the complete artifact and "
                        "---CHANGELOG--- containing STATUS: COMPLETE plus a precise changelog."
                    ),
                    agent=agent,
                    markdown=False,
                )

                stage_crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=self.verbose,
                )

                try:
                    output = stage_crew.kickoff()
                    raw = self._normalise_output(output)
                    result.raw_output = raw
                    result.status = "VALIDATING"
                    if on_stage_update:
                        on_stage_update(result)

                    work, changelog = self._parse_and_validate(raw)
                except Exception as exc:
                    last_error = str(exc)
                    result.error = last_error
                    if attempt < max_attempts:
                        continue
                    result.status = "BLOCKED"
                    results.append(result)
                    if on_stage_update:
                        on_stage_update(result)
                    raise GateError(
                        f"Stage {spec.number} failed its hard completion gate after {max_attempts} attempt(s). "
                        f"Stage {spec.number + 1 if spec.number < 6 else 'delivery'} was NOT started. Last error: {last_error}"
                    ) from exc

                result.work = work
                result.changelog = changelog
                result.error = ""
                result.status = "COMPLETED"
                current_work = work
                passed = True
                results.append(result)
                if on_stage_update:
                    on_stage_update(result)
                break

            if not passed:
                raise GateError(f"Stage {spec.number} did not complete. Pipeline halted.")

        return current_work, results
