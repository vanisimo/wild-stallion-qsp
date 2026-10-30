"""PreToolUse hook for Antigravity: guards qsp-project.json and USER-OWNED TEXT files."""

from __future__ import annotations

import json
import sys
from pathlib import Path

LOCKED_COMPLETED_FILES = {
    "hall_missing_amanda_text.qsps",
    "hall_missing_agent_melissa_text.qsps",
}


def main() -> None:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        tool_call = payload.get("toolCall") or {}
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args") or {}
        target_path_str = args.get("Path") or args.get("TargetFile") or ""

        if not target_path_str:
            print(json.dumps({"decision": "allow"}))
            return

        target_path = Path(target_path_str)
        file_name = target_path.name.lower()

        if file_name == "qsp-project.json":
            print(
                json.dumps(
                    {
                        "decision": "ask",
                        "reason": "Правило AGENTS.md: Не изменять qsp-project.json без явного запроса пользователя.",
                    }
                )
            )
            return

        if file_name in LOCKED_COMPLETED_FILES:
            print(
                json.dumps(
                    {
                        "decision": "ask",
                        "reason": f"Правило AGENTS.md: Файл {target_path.name} помечен как USER-OWNED / ЗАВЕРШЕНО. Любые изменения требуют согласования с пользователем.",
                    }
                )
            )
            return

        if tool_name == "write_file" and target_path.is_file():
            try:
                head = target_path.read_text(encoding="utf-8", errors="ignore")[:1000]
                if "USER-OWNED TEXT" in head:
                    print(
                        json.dumps(
                            {
                                "decision": "ask",
                                "reason": f"Правило AGENTS.md: Файл {target_path.name} содержит метку USER-OWNED TEXT. Полная перезапись через write_file требует подтверждения.",
                            }
                        )
                    )
                    return
            except OSError:
                pass

        print(json.dumps({"decision": "allow"}))
    except Exception:
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
