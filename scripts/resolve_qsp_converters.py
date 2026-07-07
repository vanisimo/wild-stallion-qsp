"""Resolve @qsp/converters entry for verify/build helper scripts."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _candidate_paths() -> list[Path]:
    candidates: list[Path] = []

    appdata = os.environ.get("APPDATA", "")
    if appdata:
        base = Path(appdata) / "npm" / "node_modules"
        candidates.append(base / "@qsp" / "cli" / "node_modules" / "@qsp" / "converters" / "dist" / "index.cjs")
        candidates.append(base / "@qsp" / "converters" / "dist" / "index.cjs")

    program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
    candidates.append(
        Path(program_files) / "nodejs" / "node_modules" / "@qsp" / "converters" / "dist" / "index.cjs"
    )

    return candidates


def resolve_converters_cjs() -> str:
    node = r"""
try {
  process.stdout.write(require.resolve('@qsp/converters/dist/index.cjs'));
} catch (err) {
  process.exit(2);
}
"""
    env = os.environ.copy()
    node_dir = Path(r"C:\Program Files\nodejs")
    npm_dir = Path(env.get("APPDATA", "")) / "npm"
    extra = os.pathsep.join(str(p) for p in (node_dir, npm_dir) if p.exists())
    if extra:
        env["PATH"] = extra + os.pathsep + env.get("PATH", "")

    try:
        return subprocess.check_output(["node", "-e", node], text=True, env=env).strip()
    except subprocess.CalledProcessError:
        pass

    for candidate in _candidate_paths():
        if candidate.is_file():
            return str(candidate)

    raise FileNotFoundError(
        "@qsp/converters not found. Run: npm install -g @qsp/cli"
    )


if __name__ == "__main__":
    try:
        print(resolve_converters_cjs())
    except Exception as exc:
        print(f"Failed to resolve @qsp/converters: {exc}", file=sys.stderr)
        sys.exit(1)