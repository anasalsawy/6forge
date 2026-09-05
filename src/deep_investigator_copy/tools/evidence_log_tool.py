import os
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class EvidenceLogToolInput(BaseModel):
    """Input schema for the Evidence Log tool."""

    action: str = Field(
        ...,
        description="Action to run: 'append' to add a new raw findings entry, "
        "or 'read_all' to retrieve the full accumulated raw evidence log so far.",
    )
    floor_label: str = Field(
        default="",
        description="Short label for this entry, e.g. 'Floor 2 Research'. "
        "Required when action is 'append'.",
    )
    content: str = Field(
        default="",
        description="The raw findings to store (scraped text, URLs, source metadata). "
        "Required when action is 'append'. Not used for 'read_all'.",
    )


class EvidenceLogTool(BaseTool):
    name: str = "evidence_log"
    description: str = (
        "Persistent raw-evidence log shared across the whole investigation. "
        "Use action='append' to save your raw research findings (scraped content, "
        "URLs, source metadata) to the log instead of retyping them in your final "
        "answer — just confirm what you saved. Use action='read_all' to retrieve "
        "everything saved so far by every floor, when you need to review or "
        "compile the full raw record. This lets raw evidence survive across all "
        "floors without you needing to reproduce it from memory."
    )
    args_schema: Type[BaseModel] = EvidenceLogToolInput

    log_path: str = os.getenv("EVIDENCE_LOG_PATH", "output/evidence_log.md")

    def _run(self, action: str, floor_label: str = "", content: str = "") -> str:
        action = action.strip().lower()

        if action == "append":
            if not content:
                raise ValueError("content is required when action is 'append'.")
            return self._append(floor_label or "Unlabeled entry", content)

        if action == "read_all":
            return self._read_all()

        raise ValueError("action must be one of: append, read_all.")

    def _append(self, floor_label: str, content: str) -> str:
        os.makedirs(os.path.dirname(self.log_path) or ".", exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n## {floor_label}\n\n{content}\n")
        return (
            f"Saved {len(content)} characters under '{floor_label}' to the "
            "evidence log. You do not need to repeat this content in your answer "
            "— just reference it (e.g. by URL) and summarize what it shows."
        )

    def _read_all(self) -> str:
        if not os.path.exists(self.log_path):
            return "The evidence log is currently empty — nothing has been appended yet."
        with open(self.log_path, "r", encoding="utf-8") as f:
            return f.read()
