import json
import re
import subprocess
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: verify_qsps_compile.py <combined.qsps>")
    sys.exit(2)

qsps_path = Path(sys.argv[1])
text = qsps_path.read_text(encoding="utf-8")
regex_names = [m.group(1) for m in re.finditer(r"^#(\S+)", text, re.M)]

node = r"""
const {readQsps}=require('C:/Users/SlavID/AppData/Roaming/npm/node_modules/@qsp/cli/node_modules/@qsp/converters/dist/index.cjs');
const fs=require('fs');
const parsed=readQsps(fs.readFileSync(process.argv[1],'utf8'));
console.log(JSON.stringify(parsed.map(l=>l.name)));
"""
parsed_names = json.loads(
    subprocess.check_output(["node", "-e", node, str(qsps_path)], text=True)
)
parsed_set = set(parsed_names)

if len(parsed_names) != len(regex_names):
    missing = [n for n in regex_names if n not in parsed_set]
    print(
        f"QSPS compile parse mismatch: headers={len(regex_names)} parsed={len(parsed_names)}"
    )
    if missing:
        print("First missing locations:")
        for name in missing[:20]:
            print(f" - {name}")
    sys.exit(1)

print(f"QSPS compile parse OK: {len(parsed_names)} locations")