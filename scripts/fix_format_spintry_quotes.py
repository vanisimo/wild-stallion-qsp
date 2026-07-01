import re
from pathlib import Path

pat = re.compile(r"(\$FormatSpintry_[A-Za-z0-9_]+)'")
fixed_files = []

for p in Path("modules").rglob("*.qsps"):
    text = p.read_text(encoding="utf-8")
    new, n = pat.subn(r"\1", text)
    if n:
        p.write_text(new, encoding="utf-8", newline="\n")
        fixed_files.append((str(p), n))

for fp, n in sorted(fixed_files):
    print(n, fp)
print("total fixes", sum(n for _, n in fixed_files))