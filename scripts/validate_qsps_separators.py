import re
import subprocess
import json
from pathlib import Path

repo = Path(__file__).resolve().parents[1]

node = r"""
const {readQsps}=require('C:/Users/SlavID/AppData/Roaming/npm/node_modules/@qsp/cli/node_modules/@qsp/converters/dist/index.cjs');
const fs=require('fs');
const parsed=readQsps(fs.readFileSync(process.argv[1],'utf8'));
console.log(JSON.stringify(parsed.map(l=>l.name)));
"""

def regex_names(text: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"^#(\S+)", text, re.M)]


def parsed_names(text: str) -> set[str]:
    return set(json.loads(subprocess.check_output(
        ["node", "-e", node, "-"], input=text, text=True
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