#!/usr/bin/env python3
"""Fix broken QSP string concatenation after spintry migration."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "modules"

REPLACEMENTS = [
    ("+ ' + $FormatSpintry_", "+ $FormatSpintry_"),
    ("$FormatSpintry_money.'", "$FormatSpintry_money + '.'"),
    ("$FormatSpintry_BarWorkIncome.'", "$FormatSpintry_BarWorkIncome + '.'"),
    ("$FormatSpintry_TavernHallTips.'", "$FormatSpintry_TavernHallTips + '.'"),
    (
        "$FormatSpintry_DanceDressOrderPrice. У вас: ' + $FormatSpintry_money.'",
        "$FormatSpintry_DanceDressOrderPrice + '. У вас: ' + $FormatSpintry_money + '.'",
    ),
    (
        "$FormatSpintry_DraupnirUpgradeLineCost, ' + STR(DraupnirUpgradeLineDays) + ' дн.'",
        "$FormatSpintry_DraupnirUpgradeLineCost + ', ' + STR(DraupnirUpgradeLineDays) + ' дн.'",
    ),
    (
        "$FormatSpintry_TavernDailyCostBonus в день'",
        "$FormatSpintry_TavernDailyCostBonus + ' в день'",
    ),
    (
        "$FormatSpintry_ChurchDonateAmount в ящик у алтаря. Отец Герхард кивнул без лишних слов.'",
        "$FormatSpintry_ChurchDonateAmount + ' в ящик у алтаря. Отец Герхард кивнул без лишних слов.'",
    ),
    (
        "' + $FormatSpintry_TavernDayRepairCost___money</b>. Сейчас у вас ' + STR(money) + '.'",
        "' + $FormatSpintry_TavernDayRepairGap + '</b>. Сейчас у вас ' + $FormatSpintry_money + '.'",
    ),
    ("$FormatSpintry_TavernDayRepairCost</b>", "$FormatSpintry_TavernDayRepairCost + '</b>'"),
    ("$FormatSpintry_TavernDayRepairCost.", "$FormatSpintry_TavernDayRepairCost + '."),
    ("$FormatSpintry_GiftRegistryPrice</td>", "$FormatSpintry_GiftRegistryPrice + '</td>'"),
    ("$FormatSpintry_IngaGuardBribeCost)", "$FormatSpintry_IngaGuardBribeCost + ')'"),
    ("десяти мараведи", "десяти спинтарий"),
    ("тридцать мараведи", "тридцать спинтарий"),
    ("3 мараведи", "3 спинтарии"),
    ("4 мараведи", "4 спинтарии"),
    ("2 мараведи", "2 спинтарии"),
]


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.qsps")):
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            changed += 1
            print(path.relative_to(ROOT.parent))
    print(f"Fixed {changed} files")


if __name__ == "__main__":
    main()