#!/usr/bin/env python3
"""
Lightweight stdio MCP server exposing Wild Stallion QSP OpenRouter text generation
tools directly to Antigravity (zero external dependencies).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import generate_text as gt  # noqa: E402

SERVER_INFO = {
    "name": "openrouter-writer",
    "version": "1.0.0",
}
PROTOCOL_VERSION = "2024-11-05"

TOOLS = [
    {
        "name": "openrouter_generate_scene",
        "description": (
            "Generate a Russian scene, dialogue, quest beat, or 18+ prose for Wild Stallion QSP "
            "via OpenRouter using project canon (Ilmater, sprintries, 'ты' for Stefan, no env smells)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Scene brief, choreography, or instructions.",
                },
                "brief_file": {
                    "type": "string",
                    "description": "Optional relative path to a brief file (e.g. promt/...).",
                },
                "mode": {
                    "type": "string",
                    "enum": ["nsfw", "dialog", "quest", "fast"],
                    "default": "dialog",
                    "description": "Generation mode: nsfw (18+), dialog, quest, or fast.",
                },
                "model": {
                    "type": "string",
                    "description": "Optional OpenRouter model slug override (e.g. deepseek/deepseek-v4-pro).",
                },
                "characters": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Character keys: stefan, amanda, melissa, sandra, gerhard, lizette, becky, legare.",
                },
                "corruption": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 5,
                    "description": "Optional FamilyCorruptionStage (0..5).",
                },
                "qsp": {
                    "type": "boolean",
                    "default": True,
                    "description": "Format output paragraphs as *pl '...' QSP lines.",
                },
                "max_tokens": {
                    "type": "integer",
                    "default": 900,
                    "description": "Max completion tokens.",
                },
                "reasoning": {
                    "type": "string",
                    "enum": ["off", "low", "medium", "high"],
                    "default": "off",
                    "description": "Reasoning mode for thinking models (default off).",
                },
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "openrouter_list_models",
        "description": "List recommended OpenRouter model presets configured for Wild Stallion QSP.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]


def send_message(obj: dict) -> None:
    data = (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8")
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()


def send_result(req_id: object, result: dict) -> None:
    send_message({"jsonrpc": "2.0", "id": req_id, "result": result})


def send_error(req_id: object, code: int, message: str) -> None:
    send_message({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}})


def handle_generate_scene(args: dict) -> dict:
    gt.load_env_file(gt.REPO_ROOT / ".env")
    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key or api_key == "sk-or-v1-your-key-here":
        return {
            "isError": True,
            "content": [{"type": "text", "text": "OPENROUTER_API_KEY is not configured in .env."}],
        }

    mode = args.get("mode") or "dialog"
    if mode not in gt.MODEL_PRESETS:
        mode = "dialog"
    preset = gt.MODEL_PRESETS[mode]

    model = (args.get("model") or "").strip() or os.environ.get(preset["env_var"], "").strip() or preset["default"]
    user_prompt = (args.get("prompt") or "").strip()
    brief_file = (args.get("brief_file") or "").strip()
    if brief_file:
        bp = Path(brief_file)
        if not bp.is_absolute():
            bp = gt.REPO_ROOT / bp
        if not bp.is_file():
            return {
                "isError": True,
                "content": [{"type": "text", "text": f"Brief file not found: {bp}"}],
            }
        file_text = bp.read_text(encoding="utf-8").strip()
        user_prompt = f"{user_prompt}\n\n{file_text}".strip() if user_prompt else file_text

    if not user_prompt:
        return {
            "isError": True,
            "content": [{"type": "text", "text": "Prompt is empty."}],
        }

    sys_parts = [gt.BASE_SYSTEM_PROMPT, gt.MODE_INSTRUCTIONS[mode]]
    chars = args.get("characters") or []
    if chars:
        char_lines = ["ПЕРСОНАЖИ В СЦЕНЕ:"]
        for c in chars:
            key = str(c).lower()
            char_lines.append(f"- {gt.CHAR_PROFILES.get(key, c)}")
        sys_parts.append("\n".join(char_lines))

    corruption = args.get("corruption")
    if corruption is not None and int(corruption) in gt.CORRUPTION_HINTS:
        sys_parts.append(f"КОРРУПЦИЯ СЕМЬИ:\n- {gt.CORRUPTION_HINTS[int(corruption)]}")

    system_prompt = "\n\n".join(sys_parts)
    max_tokens = int(args.get("max_tokens") or preset["max_tokens"])
    reasoning = args.get("reasoning") or "off"

    raw_text, usage = gt.call_openrouter(
        api_key=api_key,
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=preset["temperature"],
        top_p=preset["top_p"],
        max_tokens=max_tokens,
        reasoning=reasoning,
    )
    use_qsp = args.get("qsp", True)
    final_text = gt.format_qsp_paragraphs(raw_text) if use_qsp else raw_text
    warnings = gt.canon_warnings(raw_text)

    meta_lines = [f"[model={model} | mode={mode} | tokens={usage.get('prompt_tokens', '?')}/{usage.get('completion_tokens', '?')}]"]
    if warnings:
        meta_lines.append("[CANON WARNINGS] " + "; ".join(warnings))
    meta_lines.append("")
    meta_lines.append(final_text)

    return {"content": [{"type": "text", "text": "\n".join(meta_lines)}]}


def handle_list_models() -> dict:
    lines = []
    for mode, cfg in gt.MODEL_PRESETS.items():
        lines.append(f"[{mode}] default: {cfg['default']}")
        for mid, desc in cfg["alternatives"]:
            lines.append(f"  - {mid}: {desc}")
    return {"content": [{"type": "text", "text": "\n".join(lines)}]}


def main() -> int:
    while True:
        raw_line = sys.stdin.buffer.readline()
        if not raw_line:
            break
        line = raw_line.decode("utf-8", errors="replace").strip()
        if not line:
            continue

        try:
            msg = json.loads(line)
        except json.JSONDecodeError as exc:
            send_error(None, -32700, f"Parse error: {exc}")
            continue

        req_id = msg.get("id")
        method = msg.get("method", "")
        params = msg.get("params") or {}

        # Notifications have no id and expect no response.
        if req_id is None:
            continue

        try:
            if method == "initialize":
                send_result(
                    req_id,
                    {
                        "protocolVersion": PROTOCOL_VERSION,
                        "capabilities": {"tools": {}},
                        "serverInfo": SERVER_INFO,
                    },
                )
            elif method == "ping":
                send_result(req_id, {})
            elif method == "tools/list":
                send_result(req_id, {"tools": TOOLS})
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments") or {}
                if tool_name == "openrouter_generate_scene":
                    send_result(req_id, handle_generate_scene(tool_args))
                elif tool_name == "openrouter_list_models":
                    send_result(req_id, handle_list_models())
                else:
                    send_error(req_id, -32601, f"Unknown tool: {tool_name}")
            else:
                send_error(req_id, -32601, f"Method not found: {method}")
        except Exception as exc:
            send_result(
                req_id,
                {"isError": True, "content": [{"type": "text", "text": f"Error: {exc}"}]},
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
