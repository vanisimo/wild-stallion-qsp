"""Stop hook for Antigravity: runs scripts/lint_qsp_changes.py before ending a turn."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        if payload.get("terminationReason") != "NO_TOOL_CALL":
            print(json.dumps({"decision": "allow"}))
            return
        if int(payload.get("executionNum", 1)) > 2:
            print(json.dumps({"decision": "allow"}))
            return

        repo_root = Path(__file__).resolve().parents[2]
        sys.path.insert(0, str(repo_root / "scripts"))
        import lint_qsp_changes

        errors = lint_qsp_changes.run_all_checks(repo_root)
        if errors:
            msg = "[Автопроверка QSP и канона] Обнаружены проблемы:\n- " + "\n- ".join(errors[:6])
            print(json.dumps({"decision": "continue", "reason": msg}))
            return

        print(json.dumps({"decision": "allow"}))
    except Exception:
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
