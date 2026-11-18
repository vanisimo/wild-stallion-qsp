#!/usr/bin/env python3
"""
Generate Russian narrative scenes, dialogues, and 18+ prose for Wild Stallion QSP
via the OpenRouter API, following project canon (AGENTS.md / GEMINI.md).

Usage examples:
  python scripts/generate_text.py --list-models
  python scripts/generate_text.py --live-models --filter deepseek
  python scripts/generate_text.py --mode nsfw --char amanda --corruption 3 --qsp --prompt "..."
  python scripts/generate_text.py --mode dialog --char melissa --brief-file promt/melissa_all_scenes_concept.txt --qsp
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"

MODEL_PRESETS = {
    "nsfw": {
        "default": "deepseek/deepseek-v4-pro",
        "env_var": "OPENROUTER_MODEL_NSFW",
        "temperature": 0.82,
        "top_p": 0.92,
        "max_tokens": 900,
        "alternatives": [
            ("deepseek/deepseek-v4-pro", "Лучший живой русский язык без английской кальки (используй с --reasoning off)"),
            ("deepseek/deepseek-v3.1-terminus", "Запасной вариант без цензуры, но чаще даёт шероховатости и кальку с английского"),
            ("deepseek/deepseek-v3.2", "Быстрее и дешевле на выходе, хорошо держит подробную прозу"),
            ("sao10k/l3.1-euryale-70b", "Специализированная 70B RP/18+ модель без цензуры"),
            ("anthracite-org/magnum-v4-72b", "Литературная 72B модель для откровенных сцен (дороже)"),
            ("thedrummer/skyfall-36b-v2", "Хороший баланс цены и раскованного RP/18+ стиля"),
            ("cognitivecomputations/dolphin-mistral-24b-venice-edition", "Бюджетная нецензурированная модель"),
            ("nousresearch/hermes-4-405b", "Крупная модель с сильным следованием инструкциям и минимальной цензурой"),
        ],
    },
    "dialog": {
        "default": "deepseek/deepseek-v4-pro",
        "env_var": "OPENROUTER_MODEL_DIALOG",
        "temperature": 0.72,
        "top_p": 0.9,
        "max_tokens": 900,
        "alternatives": [
            ("deepseek/deepseek-v4-pro", "Отлично передаёт живые русские диалоги, иронию и подтекст"),
            ("mistralai/mistral-large-4-0", "Сильный литературный слог и удержание характеров"),
            ("deepseek/deepseek-v3.2", "Бюджетный вариант для длинных бытовых диалогов"),
            ("anthropic/claude-fable-5.2", "Премиум-модель для художественной прозы (высокая цена)"),
        ],
    },
    "quest": {
        "default": "deepseek/deepseek-v4-pro",
        "env_var": "OPENROUTER_MODEL_DIALOG",
        "temperature": 0.65,
        "top_p": 0.9,
        "max_tokens": 1100,
        "alternatives": [
            ("deepseek/deepseek-v4-pro", "Хорошо держит логику квеста и ветвление"),
            ("mistralai/mistral-large-4-0", "Чёткая структура сцен и диалогов"),
            ("qwen/qwen4-max", "Уверенно работает со сложным контекстом и правилами мира"),
        ],
    },
    "fast": {
        "default": "deepseek/deepseek-v4.1-flash",
        "env_var": "OPENROUTER_MODEL_FAST",
        "temperature": 0.75,
        "top_p": 0.9,
        "max_tokens": 700,
        "alternatives": [
            ("deepseek/deepseek-v4.1-flash", "Сверхдешёвые и быстрые черновики"),
            ("qwen/qwen3.7-flash", "Альтернативный дешёвый вариант для набросков"),
        ],
    },
}

CHAR_PROFILES = {
    "stefan": (
        "Стефан Лонгкок (20 лет): молодой хозяин трактира «Дикий Жеребец», бывший раздолбай. "
        "Грубовато-шутливый, прямой, без рыцарского пафоса и канцелярита. В начале Act 1 ещё пробует границы "
        "(в голове пошлые мысли, но вслух часто сдержаннее или неловко шутит); со временем увереннее. "
        "Алкоголь только как фон прошлого, не тема сцен. Дружелюбен, но своё не отдаёт просто так. "
        "Повествование от лица/действий Стефана — строго на «ты» («Ты видишь», «Ты подходишь»)."
    ),
    "amanda": (
        "Аманда Лонгкок (младшая сестра, официантка): острая на язык, дерзкая, колет и дразнит, "
        "любит внимание состоятельных мужчин и яркие подарки. Сама не ревнивая, но не терпит контроля. "
        "Слаба на передок (долгие ласки и слова действуют сильнее грубого напора); тянется к Легаре и Лизетте."
    ),
    "melissa": (
        "Мелисса Лонгкок (средняя сестра): типаж книжной зазнайки (как Гермиона Грейнджер — но в фэнтези-мире), "
        "любит романы («Королева Элеонора»), стихи, музыку. Мужскую похоть считает смешной, предсказуемой и наивной: "
        "закатывает глаза, иронично высмеивает дешёвые эвфемизмы и торгуется с лёгкой усмешкой (не злая стерва), "
        "берёт спринтрии на книги, бумагу и издание. Внутри ревнива, к Стефану теплее по мере роста доверия."
    ),
    "sandra": (
        "Сандра Лонгкок (мать, кухня и быт): спокойная, прямая, держит себя в ежовых рукавицах, "
        "«волнорез» семьи и трактира. Смесь морали и прагматизма; может сухо подколоть Стефана как хозяина. "
        "Постепенно расслабляется и отходит на второй план, когда Стефан доказывает, что справляется."
    ),
    "gerhard": (
        "Отец Герхард (священник Ильматера): амбициозный интриган, сосланный из столицы и мечтающий вернуться с триумфом. "
        "На амвоне давит авторитетом, вкрадчиво продвигает заветы о плодовитости и скрещивании; наедине стремится "
        "оприходовать красивых горожанок, пользуясь безоговорочной верой паствы."
    ),
    "lizette": (
        "Лизетта: приезжает с кораблём из столицы, привозит экзотику и столичные привычки; "
        "для Аманды — окно в большой мир и зеркало искушения."
    ),
    "becky": (
        "Бекки Блэнкеншип: рыжая, зрелая, пышная вдова с крупной грудью и розовыми (не тёмными!) сосками, "
        "гладко выбрита порошком «Таро». Простая, тёплая и болтливая в речи («бэкки»), называет Стефана "
        "«Стефанчик», «милый», «жеребец». Телом очень отзывчивая («всегда немного мокрая»), но просит вести себя "
        "тише, чтобы дети за стенкой не услышали."
    ),
    "clarissa": (
        "Кларисса Легре (22 года): вторая жена купца Альбера Легре. Серебристо-пепельные волосы, "
        "ярко-фиолетовые глаза, стройная фигура, высокая упругая грудь, гладкая кожа от порошка «Таро». "
        "Характер: чувственная гордость, деловитая хозяйка лавки (не истеричка), ревность к мужу и тайное "
        "упоение близостью со Стефаном в подсобке среди винных бочек и мешков, пока Альбер или помощник рядом. "
        "Зависит от порога sluttiness: на низком сдержаннее, на >= 35 уверенная и манящая, на >= 50 раскованная и дерзкая."
    ),
    "legare": (
        "Легаре: состоятельный и влиятельный мужчина, привыкший получать желаемое; ранний соперник Стефана за внимание Аманды."
    ),
}

BASE_SYSTEM_PROMPT = """Ты — сценарист и литературный ассистент текстовой RPG/новеллы «Дикий Жеребец» (Wild Stallion QSP).
Пиши на живом, ёмком и динамичном русском языке.

ОБЯЗАТЕЛЬНЫЙ КАНОН МИРА И СТИЛЯ:
1. Обращение к ГГ (Стефану) в описании его действий и мыслей — строго на «ты» («Ты подходишь», «Ты замечаешь»). Никакого «Вы/вы».
2. Религия и лексика: верховное божество — Ильматер. Запрещены слова «боже», «ради бога», «Господи», «о боги» — заменяй на «Ильматер», «ради Ильматера», «видит Ильматер». Вместо креста/креститься — «знак Круга», «осенить себя святым кругом».
3. Чистота тела: вместо бритв используют храмовый серый порошок «Таро» (травяной, щёлочь). Женщины убирают волосы полностью, мужчины оставляют аккуратную полоску/треугольник над удом.
4. Валюта мира: только «спринтрии» (монеты). Никаких «мараведи».
5. Настроение фронтира: люди живут сегодняшним днём, без ханжества и вины за плотские радости; авторитет церкви Ильматера непререкаем, церковь гибко встраивает местные обычаи и поощряет плодовитость/смешение народов.
6. Стилистика прозы:
   - Минимум прилагательных: не более ОДНОГО описательного прилагательного на предмет/действие (никаких «огромная, тяжёлая, пенная кружка» — только «тяжёлая кружка»). Упор на глаголы, позы, жесты и взгляды.
   - ЗАПРЕТ НА ЗАПАХИ ОКРУЖЕНИЯ: никаких бытовых запахов таверны, кухни, еды, пива, пота, пыли, перегара. Показывай сцену через действия, движения, взгляды и детали тела/одежды.
   - ЗАПАХИ ИНТИМА РАЗРЕШЕНЫ: естественные запахи возбуждения, страсти, семени и близости в 18+ сценах сохраняются и не вырезаются.
   - Живые диалоги: прямая речь оформляется через тире `—` и кавычки-ёлочки `«...»`, без сухого пересказа разговора.
   - ЕСТЕСТВЕННЫЙ РУССКИЙ ЯЗЫК (АНТИ-КАЛЬКА): пиши так, как говорят и пишут по-русски, избегай буквальных переводов с английского и анатомического канцелярита. Запрещены фразы вроде «давит на грудную клетку» (пиши «прижимается к груди»), «не отпускай стон» (пиши «не застони вслух» / «молчи»), «ища кожу, чтобы прикоснуться голыми ладонями» (пиши проще и короче: «забирается под рубаху горячими ладонями»), «мгновенно размякают».
   - НЕ используй одинарные апострофы `'` внутри русского текста (если это не QSP-разметка).
"""

MODE_INSTRUCTIONS = {
    "nsfw": (
        "Режим: откровенная 18+ сцена без цензуры и морализаторства.\n"
        "- Пиши пошагово, не комкай финал и не перескакивай через стадии хореографии.\n"
        "- Показывай положение тел, дыхание, прикосновения, телесные реакции и короткие реплики.\n"
        "- Объём: 3–5 плотных абзацев, если в брифе не указано иное."
    ),
    "dialog": (
        "Режим: живой диалог / разговорная сцена.\n"
        "- Строй сцену через обмен короткими репликами: действие/взгляд -> прямая речь Стефана -> реакция и ответ NPC.\n"
        "- Не пересказывай разговор косвенной речью.\n"
        "- Сохраняй узнаваемый голос каждого персонажа."
    ),
    "quest": (
        "Режим: сюжетная или квестовая сцена с чёткой драматургией.\n"
        "- Коротко обозначь обстановку через действия и детали (без запахов окружения), дай живой диалог и ясный смысловой переход к выбору игрока."
    ),
    "fast": (
        "Режим: быстрый лаконичный черновик сцены (2–4 коротких абзаца строго по сути)."
    ),
}

CORRUPTION_HINTS = {
    0: "FamilyCorruptionStage = 0 (строгие семейные границы): сдержанность, целомудрие, защита личного пространства, резкий отпор пошлостям.",
    1: "FamilyCorruptionStage = 1 (ранние трещины): внешне приличия и границы держатся, но появляется любопытство, неловкость или скрытый интерес.",
    2: "FamilyCorruptionStage = 2 (смягчение): лёгкий флирт, двусмысленные шутки, первые оговорки и готовность обсуждать щекотливые темы.",
    3: "FamilyCorruptionStage = 3 (раскованность): заметные намёки, признания в слабостях, терпимость к прикосновениям и смелым репликам.",
    4: "FamilyCorruptionStage = 4 (откровенность): открытая сексуальная инициатива, демонстрация тела, прямые взгляды на пах и отсутствие прежнего стыда.",
    5: "FamilyCorruptionStage = 5 (полное снятие границ): откровенный разврат, раскрепощённость и естественное принятие интима.",
}


def load_env_file(env_path: Path) -> None:
    if not env_path.is_file():
        return
    for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def format_qsp_paragraphs(text: str) -> str:
    lines: list[str] = []
    for raw in text.splitlines():
        clean = raw.strip()
        if not clean:
            continue
        # Strip accidental surrounding *pl '...' if the model already added it
        m = re.match(r"^\*pl\s+'(.*)'$", clean)
        if m:
            clean = m.group(1)
        escaped = clean.replace("'", "''")
        lines.append(f"*pl '{escaped}'")
    return "\n".join(lines)


def canon_warnings(text: str) -> list[str]:
    warnings: list[str] = []
    checks = [
        (r"\bбоже\b|\bради бога\b|\bгосподи\b|\bо боги\b", "Найдена христианская/языческая лексика вместо «Ильматер»."),
        (r"\bмараведи\b", "Найдено «мараведи» вместо «спринтрии»."),
        (r"\bперекрестил\w*|\bкрестн\w* знамен", "Найдено упоминание креста вместо «знака Круга / святого круга»."),
        (r"\bВы\s+(?:подход|вид|говор|дела|смотр|бер|клад|ид)", "Возможное обращение к ГГ на «Вы» вместо «ты»."),
    ]
    for pattern, msg in checks:
        if re.search(pattern, text, flags=re.IGNORECASE):
            warnings.append(msg)
    return warnings


def list_curated_models() -> None:
    print("=== Рекомендуемые пресеты OpenRouter для проекта «Дикий Жеребец» ===\n")
    for mode, cfg in MODEL_PRESETS.items():
        print(f"[{mode}] По умолчанию: {cfg['default']} (ENV: {cfg['env_var']})")
        for model_id, desc in cfg["alternatives"]:
            print(f"  - {model_id}: {desc}")
        print()


def list_live_models(filter_text: str | None) -> None:
    req = urllib.request.Request(
        OPENROUTER_MODELS_URL,
        headers={"User-Agent": "WildStallionQSP/1.0"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))["data"]
    needle = (filter_text or "").lower().strip()
    count = 0
    for m in sorted(data, key=lambda x: x["id"]):
        mid = m["id"]
        if ":batch" in mid:
            continue
        if needle and needle not in mid.lower() and needle not in m.get("name", "").lower():
            continue
        pricing = m.get("pricing") or {}
        pin = float(pricing.get("prompt") or 0) * 1_000_000
        pout = float(pricing.get("completion") or 0) * 1_000_000
        ctx = m.get("context_length") or "?"
        print(f"{mid} | ctx={ctx} | in=${pin:.2f}/M | out=${pout:.2f}/M")
        count += 1
    print(f"\nНайдено моделей: {count}")


def call_openrouter(
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    top_p: float,
    max_tokens: int,
    reasoning: str = "off",
) -> tuple[str, dict]:
    payload: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
    }
    if reasoning == "off":
        payload["reasoning"] = {"enabled": False}
    elif reasoning in ("low", "medium", "high"):
        payload["reasoning"] = {"effort": reasoning}
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/vanisimo/wild-stallion-qsp",
        "X-Title": "Wild Stallion QSP Text Generator",
    }
    req = urllib.request.Request(
        OPENROUTER_CHAT_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenRouter HTTP {exc.code}: {err_body}") from exc

    choices = body.get("choices") or []
    if not choices:
        raise RuntimeError(f"Пустой ответ OpenRouter: {json.dumps(body, ensure_ascii=False)}")
    msg = choices[0].get("message") or {}
    content = msg.get("content")
    if not content:
        refusal = msg.get("refusal")
        finish_reason = choices[0].get("finish_reason")
        raise RuntimeError(
            f"Модель {model} не вернула текст (finish_reason={finish_reason}, refusal={refusal}). "
            "Попробуйте увеличить --max-tokens или сменить модель через --model."
        )
    usage = body.get("usage") or {}
    return content.strip(), usage


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    load_env_file(REPO_ROOT / ".env")

    parser = argparse.ArgumentParser(
        description="Генератор сцен и диалогов для Wild Stallion QSP через OpenRouter API"
    )
    parser.add_argument("--list-models", action="store_true", help="Показать проверенные пресеты моделей")
    parser.add_argument("--live-models", action="store_true", help="Запросить актуальный каталог моделей с OpenRouter")
    parser.add_argument("--filter", type=str, default="", help="Фильтр для --live-models (например: deepseek, hermes, mistral)")
    parser.add_argument("--mode", choices=sorted(MODEL_PRESETS.keys()), default="nsfw", help="Режим генерации")
    parser.add_argument("--model", type=str, default="", help="Явный ID модели OpenRouter (перекрывает пресет)")
    parser.add_argument("--char", nargs="*", default=[], help=f"Профили персонажей ({', '.join(CHAR_PROFILES.keys())})")
    parser.add_argument("--corruption", type=int, choices=range(0, 6), default=None, help="Уровень FamilyCorruptionStage (0..5)")
    parser.add_argument("--prompt", type=str, default="", help="Текстовый бриф / задание на сцену")
    parser.add_argument("--brief-file", type=str, default="", help="Путь к файлу с брифом (например promt/...)")
    parser.add_argument("--qsp", action="store_true", help="Отформатировать абзацы в строки *pl '...'")
    parser.add_argument("--temp", type=float, default=None, help="Переопределить temperature")
    parser.add_argument("--max-tokens", type=int, default=None, help="Переопределить max_tokens")
    parser.add_argument("--reasoning", choices=["off", "low", "medium", "high"], default="off", help="Режим рассуждений для thinking-моделей (по умолчанию off)")
    parser.add_argument("--out", type=str, default="", help="Сохранить результат в файл (вместо только вывода в консоль)")

    args = parser.parse_args()

    if args.list_models:
        list_curated_models()
        return 0

    if args.live_models:
        list_live_models(args.filter)
        return 0

    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key or api_key == "sk-or-v1-your-key-here":
        print(
            "[ERROR] Не задан OPENROUTER_API_KEY.\n"
            "Скопируйте .env.example в .env и впишите свой ключ с https://openrouter.ai/keys",
            file=sys.stderr,
        )
        return 1

    user_prompt = args.prompt.strip()
    if args.brief_file:
        brief_path = Path(args.brief_file)
        if not brief_path.is_absolute():
            brief_path = REPO_ROOT / brief_path
        if not brief_path.is_file():
            print(f"[ERROR] Файл брифа не найден: {brief_path}", file=sys.stderr)
            return 1
        file_text = brief_path.read_text(encoding="utf-8")
        user_prompt = f"{user_prompt}\n\n{file_text}".strip() if user_prompt else file_text.strip()

    if not user_prompt:
        print("[ERROR] Укажите --prompt \"...\" или --brief-file <путь>", file=sys.stderr)
        return 1

    preset = MODEL_PRESETS[args.mode]
    model = args.model.strip() or os.environ.get(preset["env_var"], "").strip() or preset["default"]
    temperature = args.temp if args.temp is not None else preset["temperature"]
    max_tokens = args.max_tokens if args.max_tokens is not None else preset["max_tokens"]

    sys_parts = [BASE_SYSTEM_PROMPT, MODE_INSTRUCTIONS[args.mode]]
    if args.char:
        char_lines = ["ПЕРСОНАЖИ В СЦЕНЕ:"]
        for c in args.char:
            key = c.lower()
            if key in CHAR_PROFILES:
                char_lines.append(f"- {CHAR_PROFILES[key]}")
            else:
                char_lines.append(f"- {c}")
        sys_parts.append("\n".join(char_lines))
    if args.corruption is not None:
        sys_parts.append(f"КОРРУПЦИЯ СЕМЬИ:\n- {CORRUPTION_HINTS[args.corruption]}")

    system_prompt = "\n\n".join(sys_parts)

    print(f"[OpenRouter] model={model} mode={args.mode} temp={temperature}", file=sys.stderr)
    raw_text, usage = call_openrouter(
        api_key=api_key,
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=temperature,
        top_p=preset["top_p"],
        max_tokens=max_tokens,
        reasoning=args.reasoning,
    )

    output_text = format_qsp_paragraphs(raw_text) if args.qsp else raw_text

    warnings = canon_warnings(raw_text)
    for w in warnings:
        print(f"[CANON WARNING] {w}", file=sys.stderr)

    if usage:
        pt = usage.get("prompt_tokens", "?")
        ct = usage.get("completion_tokens", "?")
        print(f"[Usage] prompt_tokens={pt}, completion_tokens={ct}", file=sys.stderr)

    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = REPO_ROOT / out_path
        if out_path.is_file() and "USER-OWNED TEXT" in out_path.read_text(encoding="utf-8", errors="ignore")[:1000]:
            print(f"[ERROR] Отказ: {out_path} помечен как USER-OWNED TEXT. Сохраняйте черновик в отдельный файл.", file=sys.stderr)
            return 1
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_text + "\n", encoding="utf-8")
        print(f"[Saved] {out_path}", file=sys.stderr)
    else:
        print(output_text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
