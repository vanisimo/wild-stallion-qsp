#!/usr/bin/env python3
"""Migrate iconless act buttons to ActUiPrepare + act $ActUiLabel, $ActUiIconPath."""

import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), '..', 'modules')

ACT_SOLO = re.compile(r"^(\s*)act\s+'((?:[^']|'')*)':\s*$")
ACT_INLINE = re.compile(r"^(\s*)act\s+'((?:[^']|'')*)':\s+(.+)$")
ACT_WITH_ICON = re.compile(r"^\s*act\s+'(?:[^']|'')*',\s*'")

BOLD_RE = re.compile(r'<b>(.+?)</b>', re.I)


def strip_bold(label: str) -> str:
    m = BOLD_RE.search(label)
    return m.group(1) if m else label


def escape_qsp(s: str) -> str:
    return s.replace("'", "''")


def resolve_icon_key(plain: str) -> str:
    l = plain.lower()

    if 'debug' in l or l.startswith('тест:'):
        return 'debug'
    if l == 'back':
        return 'return'

    if re.search(
        r'вернуться|назад|выйти из|выйти в|выйти на|остаться в|остаться рядом|'
        r'спуститься|пока не|пока хватит|передумать|отказаться|уйти|незаметно|'
        r'отмена|закончить$|остановиться$|не вмешиваться|остаться$',
        l,
    ):
        return 'return'

    if re.search(r'церков|исповед|священ|круг чистых', l):
        return 'church'
    if re.search(r'танец|танцам|танцы', l):
        return 'dance'
    if re.search(r'интим|близост|поцеловать|ласк|разрядк|нежн|довести её', l):
        return 'intim'
    if re.search(r'флирт|комплимент|намёк', l):
        return 'flirt'
    if re.search(r'подарить|подарок', l):
        return 'gift'
    if re.search(r'купить|мараведи|лавк', l):
        return 'shop'
    if re.search(r'порт|корабл|караван|пристан', l):
        return 'port'
    if re.search(r'мэри|мэр|налог|приём|клерк', l):
        return 'mayor'
    if re.search(r'страж|охран|инг', l):
        return 'guard'
    if re.search(r'ремеслен|мастер|плотник', l):
        return 'craftsmen'
    if re.search(r'рынок|фестиваль|паломник|крыс|ливень|бочк|кладов', l):
        return 'market'
    if re.search(r'стойк|работ', l):
        return 'work'
    if re.search(r'спать|лечь спать', l):
        return 'sleep'
    if re.search(r'этаж|коридор', l):
        return 'floor'
    if re.search(r'кухн', l):
        return 'kitchen'
    if re.search(r'правил|политик|профиль', l):
        return 'policy'
    if re.search(r'трактир|главный зал', l):
        return 'tavern'
    if re.search(r'улиц|трипербан', l):
        return 'street'
    if re.search(r'слушать|смотреть|наблюдать|осмотреть|прочитать|заглянуть', l):
        return 'look'
    if re.search(
        r'поговорить|спросить|признать|объяснить|сказать|требовать|дать правило|провести вечер',
        l,
    ):
        return 'talk'

    return 'generic'


def convert_act(indent: str, raw_label: str, inline_tail: str | None = None) -> str:
    label = raw_label.replace("''", "'")
    if '$' in label or re.search(r"'\s*\+\s*'|'\s*\+\s*\$|\$\s*\+\s*'", label):
        if inline_tail is None:
            return f"{indent}act '{raw_label}':"
        return f"{indent}act '{raw_label}': {inline_tail}"

    plain = strip_bold(label)
    key = resolve_icon_key(plain)
    escaped = escape_qsp(plain)
    lines = [
        f"{indent}gs 'ActUiPrepare', '{escaped}', '{key}'",
        f"{indent}act $ActUiLabel, $ActUiIconPath:",
    ]
    if inline_tail is not None:
        lines[-1] = f"{lines[-1]} {inline_tail}"
    return '\n'.join(lines)


def process_file(path: str) -> int:
    with open(path, encoding='utf-8') as f:
        text = f.read()

    lines = text.splitlines(keepends=True)
    out: list[str] = []
    count = 0

    for line in lines:
        body = line.rstrip('\r\n')
        ending = line[len(body):]

        if ACT_WITH_ICON.match(body):
            out.append(line)
            continue

        m_inline = ACT_INLINE.match(body)
        if m_inline:
            indent, raw_label, tail = m_inline.groups()
            new_body = convert_act(indent, raw_label, tail)
            if new_body != f"{indent}act '{raw_label}': {tail}":
                count += 1
            out.append(new_body + ending)
            continue

        m_solo = ACT_SOLO.match(body)
        if m_solo:
            indent, raw_label = m_solo.groups()
            new_body = convert_act(indent, raw_label)
            if new_body != f"{indent}act '{raw_label}':":
                count += 1
            out.append(new_body + ending)
            continue

        out.append(line)

    if count > 0:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.writelines(out)

    return count


def main() -> int:
    total_acts = 0
    total_files = 0

    for dp, dns, fns in os.walk(ROOT):
        if 'archive' in dp.replace('\\', '/').split('/'):
            continue
        for fn in fns:
            if not fn.endswith('.qsps'):
                continue
            path = os.path.join(dp, fn)
            n = process_file(path)
            if n > 0:
                total_acts += n
                total_files += 1
                print(f'{n:4d}  {os.path.relpath(path, ROOT)}')

    print(f'\nMigrated {total_acts} act buttons in {total_files} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())