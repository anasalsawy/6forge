import json
import os
import urllib.error
import urllib.request
from typing import Optional, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class OpenBulletMCPToolInput(BaseModel):
    """Input schema for the OpenBullet MCP tool."""

    action: str = Field(
        ...,
        description="Action to run: initialize, list_tools, or call_tool.",
    )
    tool_name: Optional[str] = Field(
        default=None,
        description="MCP tool name. Required only when action is call_tool.",
    )
    arguments_json: str = Field(
        default="{}",
        description="JSON object string containing arguments for the MCP tool call.",
    )


class OpenBulletMCPTool(BaseTool):
    name: str = "openbullet_mcp"
    description: str = (
        "Direct HTTP/SSE wrapper for the OpenBullet2 MCP endpoint. "
        "Use it to initialize MCP, list available MCP tools, and call allowed "
        "OpenBullet2 validation, compile, debug, lint, inspect, schema, parse, "
        "or listing tools without using CrewAI's MCP adapter."
    )
    args_schema: Type[BaseModel] = OpenBulletMCPToolInput

    mcp_url: str = os.getenv(
        "OPENBULLET_MCP_URL",
        "https://ob2.64-225-12-52.sslip.io/mcp",
    )

    def _run(
        self,
        action: str,
        tool_name: Optional[str] = None,
        arguments_json: str = "{}",
    ) -> str:
        action = action.strip().lower()

        if action == "initialize":
            result = self._initialize()
            return json.dumps(result, indent=2)

        if action == "list_tools":
            result = self._list_tools()
            return json.dumps(result, indent=2)

        if action == "call_tool":
            if not tool_name:
                raise ValueError("tool_name is required when action is call_tool.")

            if not self._is_allowed_tool_name(tool_name):
                raise ValueError(
                    f"Blocked MCP tool name: {tool_name}. "
                    "This wrapper only allows validation, compile, debug, lint, "
                    "inspect, schema, parse, get, or list-style MCP tools."
                )

            try:
                arguments = json.loads(arguments_json or "{}")
            except json.JSONDecodeError as exc:
                raise ValueError(f"arguments_json is not valid JSON: {exc}") from exc

            if not isinstance(arguments, dict):
                raise ValueError("arguments_json must decode to a JSON object.")

            result = self._call_tool(tool_name, arguments)
            return json.dumps(result, indent=2)

        raise ValueError("action must be one of: initialize, list_tools, call_tool.")

    def _initialize(self) -> dict:
        return self._post(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "deep-investigator-openbullet-mcp-tool",
                        "version": "1.0",
                    },
                },
            }
        )

    def _list_tools(self) -> dict:
        return self._post(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {},
            }
        )

    def _call_tool(self, tool_name: str, arguments: dict) -> dict:
        return self._post(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments,
                },
            },
            timeout=90,
        )

    def _post(self, payload: dict, timeout: int = 45) -> dict:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.mcp_url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read().decode("utf-8", errors="replace")
                content_type = response.headers.get("Content-Type", "")
                return self._parse_response(raw, content_type)
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            content_type = exc.headers.get("Content-Type", "")
            parsed = self._try_parse_response(raw, content_type)
            raise RuntimeError(
                f"OpenBullet MCP HTTP error {exc.code}: {parsed}"
            ) from exc

    def _parse_response(self, raw: str, content_type: str) -> dict:
        if "application/json" in content_type:
            return json.loads(raw)

        if "text/event-stream" in content_type:
            payloads = []
            current_data_lines = []

            for line in raw.splitlines():
                if line.startswith("data:"):
                    current_data_lines.append(line[len("data:"):].strip())
                elif line.strip() == "" and current_data_lines:
                    payloads.append("\n".join(current_data_lines))
                    current_data_lines = []

            if current_data_lines:
                payloads.append("\n".join(current_data_lines))

            for payload in payloads:
                if payload and payload != "[DONE]":
                    return json.loads(payload)

            raise RuntimeError(f"SSE response had no JSON data event: {raw[:500]}")

        raise RuntimeError(
            f"Unexpected response content type: {content_type}. "
            f"Body starts with: {raw[:500]}"
        )

    def _try_parse_response(self, raw: str, content_type: str):
        try:
            return self._parse_response(raw, content_type)
        except Exception:
            return raw[:1000]

    def _is_allowed_tool_name(self, tool_name: str) -> bool:
        name = tool_name.lower()

        allowed_keywords = (
            "validate",
            "compile",
            "debug",
            "lint",
            "inspect",
            "schema",
            "parse",
            "list",
            "get",
        )
        blocked_keywords = (
            "run",
            "start",
            "attack",
            "brute",
            "credential",
            "stuff",
            "login",
            "password",
            "proxy",
            "vpn",
            "hit",
            "check",
            "checker",
            "capture",
            "bot",
        )

        return any(keyword in name for keyword in allowed_keywords) and not any(
            keyword in name for keyword in blocked_keywords
        )
