# Design: единый паттерн сцен зала (harassment / lewd / missing)

**Статус:** код v1 (2026-07) — кнопки и policy приведены к канону §0c.  
**Связь:** `docs/economy.md` §0c, `docs/design-hall-harassment.md`

---

## Три слоя (не путать)

| Слой | Смысл | Когда |
|------|--------|--------|
| **Сцена** | что происходит сейчас | осмотр зала / rare roll |
| **Кнопки сцены** | реакция Стефана | menu в событии |
| **Policy** | правило на будущее | **после** сцены |

---

## Слои сцен (что это)

| Система | Файл | Смысл | Гейт |
|---------|------|--------|------|
| **Harassment** | `hall_harassment.qsps` | Клиент лезет, девушка **против / терпит** | всегда (рабочий зал) |
| **Lewd** | `hall_lewd_behavior.qsps` | Девушка **сама играет** вниманием | `FamilyLiberationGateOpen` + готовность |
| **Missing** | `hall_missing_girl.qsps` | Ушла с клиентом / пропала | liberation + stage ≥3 + готовность |

Кухня: `kitchen_harassment` — те же **кнопки**, area=`kitchen`.

---

## Кнопки сцены (канон)

| UI | Код | Harassment | Lewd (legacy) | Missing (legacy) |
|----|-----|------------|---------------|------------------|
| **Защитить** | `protect_hard` | protect_hard | stop | interrupt |
| **Наблюдать** | `watch` | watch | watch | peek |
| **Отвернуться** | `ignore` | ignore | encourage | ignore |

- **До ужина** (`FamilyLiberationGateOpen = 0`): только **Защитить**.  
- **После ужина**: все три.  
- Отдельной кнопки «ради выгоды» **нет** (выгода = watch/ignore).

---

## Policy после сцены (канон)

| UI | Value |
|----|-------|
| Вести себя сдержанно | 1 |
| Решать самой | 2 |
| Вести себя расковано | 3 |

Источник меню: `#HallHarassmentBuildPolicyMenu` + `#HallHarassmentPolicyChoose`  
(после lewd/missing: `$HallScenePolicySource = 'lewd'|'missing'`).

**До ужина** policy >1 режется в `GirlWorkPolicyTalkAfterHarassApply`.

OffenseDays: hook в AfterHarassApply (policy mismatch K=3).

---

## Готовность к lewd / missing (не только policy=3)

Недостаточно приказать «раскованнее», если девушка **refuse**:

- low slut + low npc_path → **не** кандидат  
- policy=3 + agreement ≤1 + low slut → **не** кандидат (это harassment-территория)

Score stage: без петли `GirlHallLewdStage*20` и без двойных Amanda-статов.

---

## Поток UI (единый)

```
intro (сцена + thoughts §0c)
  → menu: Защитить / [Наблюдать / Отвернуться]
  → resolve (картинка + текст исхода)
  → after_harass_intro + policy menu (1/2/3)
  → reaction на правило + Вернуться
```

**Не** печатать полный refuse policy-текста **до** выбора игрока (ломало intro).

---

## Диспетчер / rare look

| Источник | Порядок |
|----------|---------|
| `TavernHallActivityLook` | story → harassment → rare (missing/lewd) → kitchen noise |
| `TavernEventDispatcher` | missing / lewd **через CanStart**, не blind Start |

---

## Что ещё можно унифицировать (позже)

1. Общий `#HallSceneBuildChoiceMenu` + `#HallSceneAfterPolicy` (сейчас harassment-меню переиспользуется).  
2. Общий stage helper на базе lewd score.  
3. OffenseDays hooks для lewd/missing choices (сейчас в основном harassment + policy).  
4. Художественные intro lewd/missing (USER-OWNED pass).  
5. Кухня customer event — те же подписи кнопок.
