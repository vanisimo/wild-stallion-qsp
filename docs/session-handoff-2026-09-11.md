# Session Handoff — 2026-09-11: Amanda Dark Alley Overhaul, Home Intimacy Engine Repairs & Georgette Compatibility

**Дата**: 2026-09-11  
**Ветка**: `main`  
**Репозиторий**: `vanisimo/wild-stallion-qsp`  
**Основной фокус**:
1. Полная переработка сцены подворотни Аманды на пятничных танцах: удаление стороннего наблюдателя (MMF), внедрение разветвлённых стадий ласк, оральных и полных интимных сцен (выбор у стены / у телеги, вариации завершения), механика свидетелей (соседские парни).
2. Завершение подворотни: трата всех очков танцев (`FridayDancesCount = 5`), отправка Аманды спать в свою комнату (`AmandaDanceSleep = 1`, `$GirlLocation['amanda'] = 'AmandaRoom'`), автоматическое возвращение домой в `TavernMain`.
3. Исправление и стабилизация домашней системы интима Аманды и Стефана: устранение синтаксической ошибки оператора сравнения в `sex_scene_core.qsps`, исправление бага передачи `$ReturnLoc = 'main'`, синхронизация гейтов времени и флагов отдыха.

---

## 1. Что было сделано

### 1.1. Переработка сцены подворотни на танцах
- **`modules/events/dance/amanda_dark_alley.qsps` & `amanda_dark_alley_text.qsps`**:
  - **Удалена сцена с третьим участником (MMF)**: ветка с чужаком полностью вырезана из логики и текстов.
  - **Стадии развития сцены**:
    - Ласки под платьем и разогрев с проверкой разврата и отношений.
    - Оральный блок: 3 последовательных экрана с проверками глубокого заглота, механики ATM и бесшовного перехода к полному контакту.
    - Полный контакт: выбор позиции (у стены переулка / на тюках у телеги), развилки вагинального и анального вариантов с гейтами опыта.
    - Варианты завершения: 4 финала (внутрь, на тело/бедра, на лицо, в рот с проверкой согласия на ATM).
  - **Свидетели**: механика соседских парней, подглядывающих из темноты за углом при высоком скандале/разврате (10 очков внимания, рост слухов).
  - **Завершение и возврат домой (`#AmandaDanceAlleyEnd`)**:
    - Списываются все раунды пятницы (`FridayDancesCount = 5`).
    - Аманда помечается спящей у себя в комнате (`AmandaDanceSleep = 1`, `SexUsedToday['amanda'] = 1`, `$GirlLocation['amanda'] = 'AmandaRoom'`).
    - Устанавливается `AmandaHomeUnlocked = 1`, исключая блокировку домашней лестницы.
    - Переход осуществляется сразу домой (`gt 'TavernMain'`).

---

### 1.2. Ремонт домашней интимной системы и устранение конфликтов
- **`modules/actions/sex/sex_scene_core.qsps`**:
  - Исправлена критическая ошибка синтаксиса в строках 1292 и 1333: заменено `if $SexGirl ! 'georgett':` на валидный QSP-оператор `if $SexGirl <> 'georgett':` (в QSP символ `!` начинает строчный комментарий, из-за чего строка обрезалась до `if $SexGirl`, ломая ветвление поцелуев и ласк).
  - В процедуру `SexSceneStart` добавлена валидация входного аргумента возврата: если переданная локация не существует в проекте (`LOC($SexReturnLoc) = 0`), fallback автоматически перенаправляет игрока в `TavernMain`.
- **`modules/core/girls/girl_room_presence.qsps` & `modules/actions/dialogs/girl_talk_session.qsps`**:
  - Исправлен сдвиг аргументов при вызове ссылки интима: ранее передавался `'main'`, из-за чего `$SexReturnLoc` получал несуществующую локацию `'main'` и вызывал вылет по завершении сцены.
  - Скорректировано отображение статуса отдыха Аманды в комнате (`amanda_room.qsps`): убран преждевременный сброс переменной `AmandaHomeRestingAfterIntim` внутри геттера подписи.
- **`modules/menu/npc/npc_clickable_link.qsps`**:
  - Процедура `NpcMenuIntimOpenIconLink` усилена для корректного приёма как 3, так и 4 аргументов с валидацией `$ReturnLoc`.
- **`modules/core/girls/girl_intim_session.qsps`**:
  - Смягчён порог времени для повторяемого домашнего интима с `time = 5` до `time >= 3` (вечер и ночь, синхронно с Мелиссой).
- **`modules/actions/sex/sex_daily_flags.qsps`**:
  - Добавлен сброс суточных флагов `SexUsedToday['georgett'] = 0` и `SexUsedToday['lizette'] = 0`.
- **`modules/events/family/amanda_home_first_sex.qsps`**:
  - Добавлена регистрация суточного использования `SexUsedToday['amanda'] = 1` и вызов `gs 'RegisterPlayerCum'`.

---

## 2. Результаты верификации

1. **`scripts/check.ps1`**:
   - Проверено 446 файлов, 3107 локаций.
   - Ошибок синтаксиса: **0**.
2. **`scripts/build.ps1 -Profile dev`**:
   - Полная компиляция `game.qsps` -> `game.qsp` завершена успешно без ошибок.

---

## 3. Список изменённых и добавленных файлов

### Изменённые файлы:
- `modules/actions/dialogs/girl_talk_session.qsps`
- `modules/actions/sex/sex_daily_flags.qsps`
- `modules/actions/sex/sex_scene_core.qsps`
- `modules/core/girls/girl_intim_session.qsps`
- `modules/core/girls/girl_room_presence.qsps`
- `modules/core/time/next_day.qsps`
- `modules/events/dance/amanda_dark_alley.qsps`
- `modules/events/dance/amanda_dark_alley_text.qsps`
- `modules/events/family/amanda_home_chain.qsps`
- `modules/events/family/amanda_home_first_sex.qsps`
- `modules/menu/npc/npc_clickable_link.qsps`
- `docs/handoff.md`

### Документация:
- `docs/session-handoff-2026-09-11.md` (текущий файл)

---

## 4. План на следующую сессию (Next Steps)

1. **Утренние последствия и реакция Аманды**:
   - Утренний диалог в субботу после событий в подворотне (стыд / гордость / проверка на слухи).
   - Реакция соседей/парней в городе, если были свидетели (`AmandaNeighborBoysWitnessed`).
2. **Система подарков и обиды**:
   - Переработка механизмов `offense_days` и `FamilyTension`.
   - Покупка подарков в лавке Ирмы / на пристани и их вручение через меню взаимодействия.
3. **Развитие линии отца Герхарда в соборе**:
   - Сцена в келье Герхарда при накоплении грехов Аманды (`GerhardTargetsAmanda = 1`).
4. **Унификация диалогов ключевых NPC**:
   - Стандартизация роутеров `TalkWith*` для Бекки, Ирмы, Клариссы, Инги и Легаре.
