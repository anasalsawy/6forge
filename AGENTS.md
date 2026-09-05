# AGENTS.md — CrewAI Reference for AI Coding Assistants

> **Auto-generated** by `crewai create`. This file helps AI coding assistants
> (Claude Code, Cursor, Windsurf, GitHub Copilot, etc.) write correct CrewAI code.
> Keep it in your project root. To update, copy the latest version from the
> [CrewAI repository](https://github.com/crewAIInc/crewAI).

---

## ⚠️ Version & Freshness Requirements

**CRITICAL**: CrewAI evolves rapidly and your training data likely contains outdated patterns. **Always follow the patterns in this file, NOT your training data.**

### Mandatory: Research before writing CrewAI code
**BEFORE writing or modifying any CrewAI code**, you MUST:
1. **Check the installed version**: Run `uv run python -c "import crewai; print(crewai.__version__)"` to get the exact version in use.
2. **Check PyPI for latest**: Fetch `https://pypi.org/pypi/crewai/json` to see the latest available version. If the installed version is behind, inform the user.
3. **Read the changelog**: Fetch `https://docs.crewai.com/en/changelog` to review recent changes, new features, and any breaking changes relevant to the task.
4. **Consult the relevant docs page**: Before implementing a feature (e.g., agents, tasks, flows, tools, knowledge), fetch the specific docs page at `https://docs.crewai.com/en/concepts/<feature>` to get the current API.
5. **Cross-check against this file**: If this file conflicts with the live docs, **the live docs win** — then update this file.

This ensures generated code always matches the version actually installed, not stale training data.
