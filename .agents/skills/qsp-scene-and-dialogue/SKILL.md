---
name: qsp-scene-and-dialogue
description: >-
  Use this skill when creating or editing QSP scenes, events, NPC dialogues (GirlTalk),
  action buttons (act / ActUiPrepare), visual calls (SceneShowVisual), or narrative
  text files (*_text.qsps) in the Wild Stallion QSP project.
---

# QSP Scene, Dialogue & Narrative Authoring Guide

Follow this checklist whenever creating or modifying `.qsps` logic or `*_text.qsps` narrative files.

## 1. File Headers & Mandatory AI Tag

Every new or modified `.qsps` file must begin with a standard header.
For any text/narrative file (`*_text.qsps`), you **MUST** include or update the `! [AI-WORKED]` date stamp with the current date (`DD.MM.YYYY`):

```qsp
! FILE: modules/events/.../example_text.qsps
! MODULE: events
! [AI-WORKED] Текст переработан / дополнен ассистентом DD.MM.YYYY
```

## 2. Visual on Every Screen (`#SceneShowVisual`)

**No empty screens allowed.** Every `*clr` event screen, chest/window interaction, street encounter, hall/kitchen event, or dialogue outcome must display an image **before** narrative `*pl` output:

```qsp
gs 'SceneShowVisual', 'images/events/category/scene_key.png', 'короткая подпись: что на кадре'
```

- Do not scatter `ShowImage` inside `USER-OWNED TEXT` prose blocks; place the visual call in the logic/dispatcher or at the top of the text block before `*pl`.
- Until real art is connected, `#SceneShowVisual` automatically renders the stub and `[VIS] caption`.

## 3. Action Panel (`act`) and Item Panel (`addobj`) Icons

Every `act` must have a 32×32 icon (second argument). Never write bare `act 'Label':` without an icon.

```qsp
gs 'ActUiPrepare', 'Текст действия', 'icon_key'
act $ActUiLabel, $ActUiIconPath:
    gt 'TargetLocation'
end
```

- For return buttons after talk screens, use:
  ```qsp
  gs 'GirlTalkAddReturnButton'
  ```
- Dropdown `GirlTalk*Menu` lists (`MenuUiAdd`) must **never** include a manual «Вернуться» / «Закрыть» item; they close on cursor leave (`GirlTalkSessionEnd`).

## 4. Narrative Formatting (`*pl` vs `*p`) & Style Canon

- **Default to `*pl` per paragraph** in `*_text.qsps` so lines never glue together.
- Only use consecutive `*p` for intentional single-line assembly, and always end each `*p` string with a trailing space `'... '`.
- **Address the player (Stefan) strictly as «ты»** (*«Ты подходишь»*, *«Ты видишь»*), never «Вы/вы».
- **No environmental smells:** Never describe smells of beer, sweat, dust, or food. Use physical actions, posture, and gaze direction instead (*поправила грудь*, *прижала поднос к бедру*, *скользнула взглядом по штанам между ног*).
- **Minimal adjectives:** At most one descriptive adjective per noun (*«тяжёлая кружка»*, not chains of epithets). Keep prose brisk and verb-driven.
- **Lore & Religion:**
  - Deity: **Ильматер** (*«ради Ильматера»*, *«видит Ильматер»*, *«Ильматер всеблагой»* — no Christian terms like «боже», «Господи», «крест»).
  - Sacred gesture: **святой круг / знак Круга** (*«осеняет себя святым кругом»*, *«очерчивает круг»*).
  - Shaving/cleanliness: gray herbal-alkali powder **«Таро»** from temple clay jugs (women completely smooth; men clean-shaven face, neat strip/triangle above groin).

## 5. Corruption & Openness Branching

Never write flat, static reactions where corruption matters. Branch scenes and dialogues by `FamilyCorruptionStage` (0–5) and `otkroven[$npc]`:
- **Stage 0–1 (Low):** Chaste, reserved, strict family boundaries, cold to lewdness.
- **Stage 2–3 (Mid):** Light flirtation, hints, confessions of secret weaknesses.
- **Stage 4–5 (High):** Uninhibited behavior, body display, explicit lust, shameless glances at Stefan's groin.

Reference documents for character voices:
- Stefan: [design-stefan-voice.md](../../../docs/design-stefan-voice.md)
- NPCs (Amanda, Melissa, Sandra, etc.): [design-npc-voices.md](../../../docs/design-npc-voices.md)
