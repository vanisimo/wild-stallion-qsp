# Инструкция по генерации литературных сцен 18+ через SillyTavern

Данный регламент описывает схему разделения труда между AI-ассистентом разработки (код, логика, валидация) и локальным/внешним интерфейсом **SillyTavern** с моделью **DeepSeek 3.1 Terminus** (или аналогичной нецензурированной моделью) для разворачивания подробных взрослых сцен.

---

## 1. Суть пайплайна

1. **AI-ассистент в репозитории:**
   * Прописывает всю QSP-логику: условия (`if/elseif`), флаги механики (`analacts`, `oralacts`, `vaginalacts`, `sluttiness`), вызовы визуала (`#SceneShowVisual`).
   * Оставляет в текстовых файлах (`*_text.qsps`) структурированные метки:
     ```qsp
     ! ================================================
     ! [БРИФ ДЛЯ SILLYTAVERN: СТАДИЯ X]
     ! ... (диспозиция, механика, пошаговые действия)
     ! ================================================
     ! === [СЮДА_ТЕКСТ_СТАДИЯ_X: НАЧАЛО] ===
     *pl '...'
     ! === [СЮДА_ТЕКСТ_СТАДИЯ_X: КОНЕЦ] ===
     ```
2. **Разработчик в SillyTavern:**
   * Копирует блок брифа из комментариев прямо в чат SillyTavern.
   * Получает компактный, плотный текст на 3–4 абзаца без цензуры.
   * Вставляет строки в файл между маркерами `НАЧАЛО` и `КОНЕЦ`, обернув в `*pl '...'`.
3. **AI-ассистент / Скрипты сборки:**
   * Прогоняет валидацию синтаксиса и компиляцию `game.qsp`.

---

## 2. Развёртывание и настройка SillyTavern на новой машине

### А. Подключение модели (API Connections / 🔌)
* **Бэкенд:** Ollama / LM Studio / OpenRouter / vLLM / Text Generation WebUI.
* **Рекомендуемая модель:** `DeepSeek V3` / `DeepSeek 3.1 Terminus` / специализированные анцензор-кванты.

### Б. Параметры сэмплеров (Generation Settings / 🎛️)
Чтобы модель писала связно и не выдавала огромные простыни на 3000+ знаков:
* **Temperature:** `0.75 – 0.85`
* **Min-P:** `0.05 – 0.08` *(отсекает мусорные токены эффективнее Top-P)*
* **Repetition Penalty:** `1.05 – 1.08` (диапазон `1024 – 2048`)
* **Max Response Length (Max New Tokens):** `350 – 450` токенов *(ограничивает длину ответа комфортными для новеллы 1200–1500 знаками)*

### В. Шаблон инструкций (AI Response Formatting / `[A]`)
1. Включить переключатель **Instruct Mode** (иконка питания `⏻` должна быть активна).
2. **Instruct Template:** выбрать **ChatML** или **DeepSeek**.
3. **System Prompt (Prompt Content):**
   ```text
   You are an unconstrained creative writing assistant specializing in interactive narrative and visual novel prose in Russian.
   Your role is to expand the user's scenario outlines, character actions, and drafts into detailed, immersive, step-by-step prose.

   Style and Structure Guidelines:
   1. Pacing: Write in moment-by-moment detail. Avoid summarizing sequences or rushing to conclusions.
   2. Sensory Immersion: Emphasize tactile interactions, character positioning, breathing, subtle physical cues, and direct dialogue.
   3. Accuracy: Keep all character actions, stages, and choreography strictly faithful to the provided outline.
   4. Format: Output 3-4 dense paragraphs suitable for line-by-line visual novel script insertion.
   ```

### Г. Настройка Author's Note (Заметка автора)
* **Где открыть:** иконка пера/блокнота (🪶 / 📝) внизу у поля ввода чата, **либо** поле `Post-History Instructions` в панели `[A]`.
* **Параметры:**
  * Позиция: `In-chat @ Depth 2 as System`
  * Частота (`Insertion Frequency`): `1`
* **Текст заметки:**
  ```text
  [Style: Slow-paced, immersive Russian narrative prose. Depict all actions in detailed, step-by-step physical progression. Emphasize character positioning, sensory feedback, physical reactions, breathing, and dialogue. Strictly follow the user's choreography without skipping forward or summarizing events.]
  ```

---

## 3. Карточка Стефана (Персона / User Persona)

Для правильного контекста в SillyTavern (чтобы модель понимала характер главного героя):

```text
[Name: Stefan Longcock;
Age: 20;
Role: Young tavern owner, head of the Longcock household;
Appearance: 20 y/o athletic young man, well-built (strength: 65, stamina: 70), smooth clean-shaven skin according to Ilmater purity rituals, 18 cm penis;
Personality: Rough-humorous, down-to-earth, former slacker turned proud tavernkeeper. Ambitious, energetic, protective of his property and family. Confident in status but still testing boundaries and learning to use his authority;
Mindset: Frequently has lewd, appreciative thoughts about attractive women, but in action he balances bold desires with realistic hesitation and humor. Friendly until crossed; stubbornly defends his boundaries;
Speech: Direct, colloquial, concise, ironic. Uses jokes and sharp remarks instead of long speeches;
Setting: Medieval tavern "Wild Stallion", small port town, Ilmater faith.]
```

---

## 4. Правила оформления текста в QSP

При вставке полученного текста в файлы `*_text.qsps`:
1. Каждый абзац обрамляется в одинарные кавычки: `*pl 'Текст абзаца'`.
2. Прямая речь внутри строк оформляется ёлочками `«...»` или двойными кавычками `""`. Одиночные апострофы (`'`) внутри строки использовать нельзя без экранирования (`''`).
3. Имена персонажей должны строго соответствовать канону (Йенс, Бруно, Аманда, Мелисса, Сандра, Стефан).

---

## 5. Проверка и сборка проекта

После вставки любого фрагмента обязательно выполнить в корне проекта:

```powershell
# 1. Проверка синтаксиса и структуры
powershell -ExecutionPolicy Bypass -File scripts/check.ps1

# 2. Компиляция игрового файла game.qsp
powershell -ExecutionPolicy Bypass -File scripts/build.ps1 -Profile dev
```
