# Правила модуля событий зала (`modules/events/hall/`)

Эти правила автоматически применяются при работе со сценами зала таверны (`hall_*`, `girl_policy_*`, `noble_attack*`, `tavern_hall_events.qsps`).

## 1. Завершённые и защищённые файлы (`USER-OWNED / ЗАВЕРШЕНО`)
- **`hall_missing_amanda_text.qsps`** и **`hall_missing_agent_melissa_text.qsps`** имеют статус **ЗАВЕРШЕНО**.
  - **Строго запрещено** вносить в них любые изменения (даже структурные или пакетные) без предварительного вопроса и явного разрешения пользователя.
- Остальные текстовые файлы с меткой `USER-OWNED TEXT` (`hall_missing_agent_sandra_text.qsps`, `hall_harassment_intro_text.qsps`, `hall_harassment_text.qsps`, `hall_family_reactions_text.qsps`, `hall_family_state_text.qsps`, `hall_choice_family_talk_text.qsps`, `hall_event_choice_thoughts_text.qsps`, `girl_policy_*_text.qsps`, `noble_attack_text.qsps`) редактировать только по логике (`if`/`end`), сохраняя авторские строки.

## 2. Визуал на каждом экране зала
- В сценах пропажи/поиска работниц (`hall_missing_*`) использовать хелпер `HallMissingGirlShowImage` с обязательной осмысленной подписью кадра.
- В сценах приставаний (`hall_harassment*`), выбора политики (`girl_policy_*`) и реакций семьи каждый экран после `*clr` обязан начинаться с `gs 'SceneShowVisual', 'images/...', 'короткая подпись'` **до** вывода текста `*pl`.
- Сверяться с реестром ассетов в `docs/ASSET-hall-events-visual.md` и картой экранов `docs/map-harass-screens.md`.

## 3. Характеры и голоса в зале
- **Аманда:** центральная героиня 1 акта; учитывать шкалы `AmandaTrustStefan`, `AmandaRebellion`, `AmandaPlayerPath`, `AmandaNpcPath` и лестницу отлучек (`docs/design-hall-missing-amanda-ladder.md`).
- **Мелисса:** ироничная «книжная всезнайка» (типаж Гермионы Грейнджер, см. `docs/design-npc-voices.md` §3). Не писать ей грубый «голос озлобленной шлюхи»; мужскую похоть воспринимает с насмешкой и иронией, берёт серебро на бумагу, книги и стихи.
- **Сандра:** прагматизм и моральный контроль (`docs/design-hall-missing-sandra-ladder.md`).
- Все выборы игрока в зале влияют на `FamilyTrust`, `FamilyTension`, `FamilyCorruptionStage` (0–5) и систему дней обиды (`modules/core/family/`).
