import re
import os
import collections

root = os.path.join(os.path.dirname(__file__), '..', 'modules')
pat = re.compile(r"act\s+'([^']*)':")
pat2 = re.compile(r'act\s+"([^"]*)":')
counts = collections.Counter()

for dp, _, fns in os.walk(root):
    if 'archive' in dp.replace('\\', '/').split('/'):
        continue
    for fn in fns:
        if not fn.endswith('.qsps'):
            continue
        path = os.path.join(dp, fn)
        with open(path, encoding='utf-8') as f:
            text = f.read()
        for m in pat.finditer(text):
            counts[m.group(1)] += 1
        for m in pat2.finditer(text):
            counts[m.group(1)] += 1

print('unique labels:', len(counts))
print('total acts:', sum(counts.values()))
for label, c in counts.most_common(120):
    print(f'{c:4d}  {label[:100]}')