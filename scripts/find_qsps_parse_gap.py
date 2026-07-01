import re
import subprocess
import json
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
qsps = repo / ".build" / "qsp-cli" / "dev" / "game.qsps"
text = qsps.read_text(encoding="utf-8")

node = r"""
const {readQsps}=require('C:/Users/SlavID/AppData/Roaming/npm/node_modules/@qsp/cli/node_modules/@qsp/converters/dist/index.cjs');
const fs=require('fs');
const parsed=readQsps(fs.readFileSync(process.argv[1],'utf8'));
console.log(JSON.stringify(parsed.map(l=>l.name)));
"""
parsed_names = set(json.loads(subprocess.check_output(
    ["node", "-e", node, str(qsps)], text=True
)))

regex = []
for line in text.splitlines():
    m = re.match(r"^#(\S+)", line)
    if m:
        regex.append(m.group(1))

first_missing = next(n for n in regex if n not in parsed_names)
idx = regex.index(first_missing)
prev = regex[idx - 1]
print(f"regex={len(regex)} parsed={len(parsed_names)}")
print(f"first missing: {first_missing} (idx {idx})")
print(f"previous ok: {prev}")

lines = text.splitlines()
prev_i = next(i for i, line in enumerate(lines) if line == f"#{prev}")
miss_i = next(i for i, line in enumerate(lines) if line == f"#{first_missing}")
start = max(0, prev_i - 2)
end = min(len(lines), miss_i + 5)
for i in range(start, end):
    print(f"{i+1}: {lines[i]}")