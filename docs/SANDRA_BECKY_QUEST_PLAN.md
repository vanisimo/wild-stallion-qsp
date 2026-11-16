# План комплексной ревизии и расширения веток Сандры и Бекки (Sandra & Becky)

## Текущий статус работы: Ветка `main`

---

### **Этап 1: Интимные сцены (`SexScene`) Сандры и Бекки — [ЗАВЕРШЕНО]**
- **Файлы:**
  - `modules/actions/sex/sex_scene_text_sister.qsps` (индивидуальный модуль Сандры)
  - `modules/actions/sex/sex_scene_text_becky.qsps` (индивидуальный модуль Бекки)
  - `modules/actions/sex/sex_scene_text.qsps` (финалы и общие хуки)
- **Задачи:**
  - Переработка и расширение `sex_scene_text_sister.qsps` под характер Сандры: зрелая, статная, строгая мать и кухарка с вязкой чувственностью и постепенным падением барьеров.
  - Добавление вариативности по `FamilyCorruptionStage` / `sluttiness['sandra']` (от сдержанной борьбы со стыдом на 0–1 до зрелого, уверенного желания на 4–5).
  - Полное покрытие всех действий в `SexSceneTextSister`: `intro`, `look`, `kiss`, `grope`/`caress`, `breast_caress`, `undress_her`, `undress_gg`, `cuni`, `blowjob`, `deepthroat`, `rim`, `rimjob`, `vaginal`, `anal`, `pose_change`, `girl_finish`, `player_finish_good`, `player_finish_bad`, `player_out`, `rest`, оргазмы.
  - Вычитка и дополнение `sex_scene_text_becky.qsps`: исправление опечатки (`вы остаёшься` $\rightarrow$ `вы остаётесь`), добавление недостающих обработчиков (`deepthroat`, `anal`, `rim`, `rimjob`), вычитка заголовка.
  - Расширение финалов и реакций Сандры в `sex_scene_text.qsps` с учётом `sluttiness['sandra']` и анала.

---

### **Этап 2: Ревизия кухни и событий Сандры — [ЗАВЕРШЕНО]**
- **Файлы:**
  - `modules/events/kitchen/kitchen_customer_event_text.qsps`
  - `modules/events/kitchen/sandra_kitchen_hook_text.qsps`
  - `modules/events/sandra/sandra_home_chain.qsps` и `_text.qsps`
  - `modules/events/sandra/sandra_draupnir_friday.qsps` и `_text.qsps`
  - `modules/events/sandra/sandra_becky_conflict.qsps` и `_text.qsps`
  - `modules/events/sandra/sandra_lermont_letter_text.qsps`
  - `modules/actions/dialogs/girl_talk_sandra_memories_text.qsps` и `girl_talk_sandra_text.qsps`
  - Сверка с `docs/1111.md` (уговоры Сандры на кухне в `hall_missing_bargain_text.qsps`)
- **Задачи:**
  - Устранение всех обращений к Стефану на «вы / вас / вам» (в т.ч. смешанных «ты + делаете»).
  - Замена устаревшей валюты («спинтарий» $\rightarrow$ «спринтрий»).
  - Очистка бытовых запахов таверны/кухни/перегара (с сохранением допустимых интимных запахов).
  - Приведение вывода к канону `*pl` (без склейки и устаревших `*p $Text` с `<br>`).
  - Проверка вариативности по `FamilyCorruptionStage` и лора Ильматера / «Таро».

---

### **Этап 3: Ревизия ветки Бекки и совместных сцен — [ЗАВЕРШЕНО]**
- **Файлы:**
  - `modules/events/becky/becky_dance.qsps` и `_text.qsps`
  - `modules/events/becky/becky_home_chain.qsps` и `_text.qsps`
  - `modules/events/becky/becky_dinner_text.qsps`
  - `modules/events/becky/becky_events.qsps`
  - `modules/events/church/church_spy_becky.qsps` и `_text.qsps`
  - `modules/events/visits/sunday_becky_sandra_text.qsps`
  - `modules/locations/shops/becky_shop.qsps`, `becky_shop_buy.qsps`, `becky_house.qsps`
  - `modules/actions/dialogs/girl_talk_becky_text.qsps`
- **Задачи:**
  - Перевод повествования со старого «вы» на каноничное «ты» (`becky_dance_text.qsps`, `becky_home_chain_text.qsps`, `church_spy_becky_text.qsps` и др.).
  - Перевод вывода на построчный `*pl` вместо `*p $Text`.
  - Аудит и удаление бытовых запахов окружения (лавки, еды, улицы).
  - Гармонизация валюты, иконок и визуальных вызовов `#SceneShowVisual`.
