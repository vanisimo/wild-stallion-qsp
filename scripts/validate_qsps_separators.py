import re
import subprocess
import json
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[1]

converters = subprocess.check_output(
    [sys.executable, str(Path(__file__).with_name("resolve_qsp_converters.py"))],
    text=True,
).strip().replace("\\", "/")

node = f"""
const {{readQsps}}=require('{converters}');
const fs=require('fs');
const parsed=readQsps(fs.readFileSync(0,'utf8'));
console.log(JSON.stringify(parsed.map(l=>l.name)));
"""

def regex_names(text: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"^#(\S+)", text, re.M)]


def parsed_names(text: str) -> set[str]:
    return set(json.loads(subprocess.check_output(
        ["node", "-e", node], input=text, encoding="utf-8"
    )))


issues = []
for path in sorted(repo.glob("modules/**/*.qsps")):
    text = path.read_text(encoding="utf-8")
    rx = regex_names(text)
    pr = parsed_names(text)
    missing = [n for n in rx if n not in pr]
    if missing:
        issues.append((str(path.relative_to(repo)), len(rx), len(pr), missing[:5], len(missing)))

print(f"files with parse gaps: {len(issues)}")
for item in issues:
    rel, rx_count, pr_count, sample, miss_count = item
    print(f"{rel}: regex={rx_count} parsed={pr_count} missing={miss_count} e.g. {sample}")
