# План комплексной ревизии и расширения квестов Мелиссы (Melissa)

## Текущий статус работы: Ветка `main`

---

### **Этап 1: Домашняя лестница сближения (`melissa_home_chain`) — [ЗАВЕРШЕНО]**
- **Файлы:**
  - `modules/events/melissa/melissa_home_chain.qsps`
  - `modules/events/melissa/melissa_home_chain_text.qsps`
  - `modules/locations/rooms/melissa_room.qsps`
- **Что сделано:**
  - Устранены все формы вежливого обращения «вы / вам / вас» при описании действий Стефана $\rightarrow$ переведено на каноничное «ты».
  - Исправлены синтаксические ошибки оператора `else:` без двоеточия.
  - Усилен книжный образ Мелиссы (трактаты Корнелия, сравнения с «Королевой Элеонорой»).

---

### **Этап 2: Пятничные танцы и платье от Ирмы (`melissa_dance`) — [ЗАВЕРШЕНО]**
- **Файлы:**
  - `modules/events/melissa/melissa_dance.qsps`
  - `modules/events/melissa/melissa_dance_text.qsps`
- **Что сделано:**
  - Заменена устаревшая валюта («спинтарии» $\rightarrow$ «спринтрии»).
  - Добавлена трёхступенчатая вариативность реакций Мелиссы в зависимости от коррупции (`FamilyCorruptionStage`) и откровения (`otkroven['melissa']`):
    - *Stage 0–1:* сдержанность, страх привлечь взгляды матушки и зевак, дистанция брата и сестры.
    - *Stage 2–3:* жаркий отклик на ласки талии и шеи, смущённое согласие.
    - *Stage 4–5:* вызывающий ответный поцелуй с языком на глазах у площади, прижимание всем телом, отказ от грязной подворотни с приглашением сразу в спальню.

---

### **Этап 3: Арка менестреля, фургона и сцены (`melissa_musician_arc`) — [ЗАВЕРШЕНО]**
- **Файлы:**
  - `modules/events/melissa/melissa_musician_arc.qsps`
  - `modules/events/melissa/melissa_musician_arc_text.qsps`
  - `modules/events/melissa/melissa_minstrel_wagon.qsps`
  - `modules/events/melissa/melissa_minstrel_wagon_text.qsps`
  - `modules/events/melissa/melissa_minstrel_backroom.qsps`
  - `modules/events/melissa/melissa_minstrel_backroom_text.qsps`
  - `modules/events/melissa/melissa_music_stage.qsps`
  - `modules/events/melissa/melissa_music_stage_text.qsps`
  - `modules/actions/dialogs/girl_talk_sandra_text.qsps`
  - `modules/actions/dialogs/girl_talk_amanda_text.qsps`
  - `modules/actions/dialogs/girl_talk_melissa_text.qsps`
  - `modules/core/time/next_day.qsps`
  - `modules/core/girls/girl_intim_session.qsps`
- **Что сделано:**
  - **Дефлорация:** строго зафиксирована в повозке на 4-й стадии (`MelissaMinstrelWagonStage = 4`). До завершения лесенки миссинг в спальне недоступен.
  - **Регулярный луп в повозке (`MelissaMinstrelWagonLoop`):** после лесенки доступен строго по пятницам вечером на танцах; 3 экрана с прелюдией, развилкой на анал (по гейту) и вариацией коррупции (реплика о детях и другой дырочке на высокой коррупции).
  - **Сцена в спальне Мелиссы на 2-м этаже (`melissa_minstrel_backroom`):**
    - Действие происходит вечером во время работы таверны (`week = 4, time = 4`), Мелисса в форменном платье и фартуке.
    - 3 ступени коррупции (у шкафа $\rightarrow$ на кровати $\rightarrow$ расширенный пул поз, включая раком и обратную наездницу в анал).
    - Развёрнутые чувственные описания женских оргазмов Мелиссы на всех трёх ступенях.
    - **Реакции на прерывание Стефаном (`interrupt`):**
      - *Низкая:* испуг, поправляет фартук, бард сбегает.
      - *Средняя:* голова барда под юбкой, барахтается и сбегает; Мелисса с сожалением сжимает бёдра и дуется на Стефана (`GirlOffenseDays += 1`).
      - *Высокая:* Мелисса не отпускает барда, требуя не мешать; при выдворении барда Мелисса требует от Стефана прийти ночью в её спальню («иначе вовек не прощу»). Если Стефан не приходит — утром упрёк в сводке дня и штраф обиды.
  - **Реакции семьи на роман Мелиссы:**
    - Сандра: по канону «дети — радость Ильматера» (на низкой — забота о солидном женихе вместо бродяги; на высокой — радость за расцветшую девку и полные кошельки таверны).
    - Аманда: подначивает старшую сестру (на высокой — «ноги сами врозь расходятся от звуков его голоса»).
    - Мелисса просит снять запрет на менестреля при высокой коррупции, обещая отблагодарить Стефана наедине.
  - **Тройничок заблокирован** флагом `MelissaMinstrelThreesomeEventUnlocked = 0` до отдельного сюжетного квеста.
  - **Аудит запахов:** вычищены бытовые запахи трактира (мясо, хлеб, эль). Валюта приведена к спринтриям.

---

### **Следующие этапы плана (для продолжения на другой машине):**

#### **Этап 4: События в тёмном переулке (`melissa_dark_alley`)**
- **Файлы:**
  - `modules/events/melissa/melissa_dark_alley.qsps`
  - `modules/events/melissa/melissa_dark_alley_text.qsps`
- **Задачи:**
  - Проверить обращения («ты» вместо «вы»).
  - Проверить баланс запахов и валюты.
  - Проверить и углубить ветвление по коррупции, поведению сестры и защите Стефана.

#### **Этап 5: Обучение сестёр и домашний анал (`melissa_home_anal` / `amanda_melissa_training`)**
- **Файлы:**
  - `modules/events/melissa/melissa_home_anal.qsps`
  - `modules/events/melissa/melissa_home_anal_text.qsps`
  - `modules/events/amanda/neighbor_boys/amanda_melissa_training.qsps`
  - `modules/events/amanda/neighbor_boys/amanda_melissa_training_text.qsps`
  - `modules/actions/sex/sex_scene_text_melissa.qsps`
- **Задачи:**
  - Ревизия анальной лестницы Мелиссы (разговор о сокровенном, применение масел, первый анальный опыт).
  - Сцена ночных растяжек и подготовки сестёр (Мелисса и Аманда).
  - Проверка интеграции в общую систему `SexSceneTextMelissa`.

#### **Этап 6: Воскресные диалоги и городские связи**
- **Файлы:**
  - `modules/events/visits/sunday_clarissa_melissa_talk_pick.qsps`
  - `modules/events/visits/sunday_clarissa_melissa_text.qsps`
  - `modules/events/hall/hall_missing_agent_melissa_text.qsps` (*USER-OWNED* — не переписывать прозу без прямого запроса пользователя).
- **Задачи:**
  - Проверка диалогов с Клариссой о книгах, поэзии и таверне.
  - Аудит гейтов и переходов.
