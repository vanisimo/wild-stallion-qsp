# -*- coding: utf-8 -*-
"""Generate hall_missing_girl_text.qsps from prose-hall-missing-pack-v3.md + AGENT fillers."""
from pathlib import Path
import re

pack = Path(__file__).with_name("prose-hall-missing-pack-v3.md").read_text(encoding="utf-8")
out_path = Path(__file__).resolve().parents[1] / "modules/events/hall/hall_missing_girl_text.qsps"

# Map section title fragment -> scene id
SECTION_MAP = [
    (r"0\.1 Petting.*Аманда", "petting_amanda"),
    (r"0\.2 Petting.*Мелисса", "petting_melissa"),
    (r"0\.3 Petting.*Сандра", "petting_sandra"),
    (r"0\.4 Hand.*Аманда", "hand_amanda"),
    (r"0\.5 Hand.*Мелисса", "hand_melissa"),
    (r"0\.6 Hand.*Сандра", "hand_sandra"),
    (r"0\.7 Cuni.*Аманда", "cuni_amanda"),
    (r"0\.8 Cuni.*Мелисса", "cuni_melissa"),
    (r"0\.9 Cuni.*Сандра", "cuni_sandra"),
    (r"^A\. Аманда", "mouth_amanda_mid_spit"),
    (r"^B\. Мелисса", "mouth_melissa_mid_spit"),
    (r"^C\. Сандра", "mouth_sandra_mid_spit"),
    (r"^D\. Аманда", "mouth_amanda_late_show"),
    (r"^E\. Мелисса", "mouth_melissa_late_show"),
    (r"^F\. Сандра", "mouth_sandra_late_swallow"),
    (r"^G\. Аманда", "mouth_amanda_late_tongue"),
    (r"^H\. Мелисса", "mouth_melissa_late_throat"),
    (r"^I1 · Аманда", "mouth_amanda_late_tongue_swallow"),
    (r"^I2 · Аманда", "mouth_amanda_late_show_spit"),
    (r"^J\. Сандра · titjob · merchant", "titjob_sandra_merchant"),
    (r"^J2\. Сандра", "titjob_sandra_traveler"),
    (r"^K\. Аманда", "mouth_amanda_late_facial"),
    (r"Anilingus|anilingus", "anilingus_melissa"),
    (r"Mom-line · Аманда|Mom-line.*Аманда", "mouth_amanda_mom_craftsman"),
    (r"Mom-line · Мелисса|Mom-line.*Мелисса", "mouth_melissa_mom_craftsman"),
    (r"Under table|under_table|Под дальним", "mouth_amanda_under_table"),
]


def extract_pl_blocks(section_body: str):
    """Return (scene_lines, meet_lines) as lists of QSP string contents (without *pl)."""
    # normalize
    body = section_body
    # find peek_meet
    m = re.search(r"\*\*peek_meet\*\*|peek_meet", body, re.I)
    if m:
        scene_part = body[: m.start()]
        meet_part = body[m.end() :]
    else:
        scene_part = body
        meet_part = ""

    def plines(part: str):
        lines = []
        for raw in part.splitlines():
            s = raw.strip()
            if not s.startswith("*pl"):
                continue
            # *pl '...'
            mm = re.match(r"\*\*pl\s+'((?:\\'|[^'])*)'\s*$", s)
            if not mm:
                mm = re.match(r"\*pl\s+'((?:\\'|[^'])*)'\s*$", s)
            if mm:
                content = mm.group(1)
            else:
                # unclosed or broken — take after first quote
                if "'" not in s:
                    continue
                rest = s.split("'", 1)[1]
                if rest.endswith("'"):
                    rest = rest[:-1]
                content = rest
            # skip empty spacers from pack (*pl ' ' / *pl '')
            if content.strip() == "":
                continue
            lines.append(content)
        return lines

    return plines(scene_part), plines(meet_part)


# Split pack into ## / # sections (level 1–2 headers)
chunks = re.split(r"\n#{1,2}\s+", pack)
sections = {}
for ch in chunks:
    title = ch.split("\n", 1)[0].strip()
    body = ch.split("\n", 1)[1] if "\n" in ch else ""
    # cut body at next accidental header residue
    body = re.split(r"\n#{1,2}\s+", body)[0]
    for pat, sid in SECTION_MAP:
        if re.search(pat, title):
            sc, mt = extract_pl_blocks(body)
            # cuni melissa: meet without **peek_meet** — last *pl is dialogue to Stefan
            if sid == "cuni_melissa" and not mt and sc:
                # last block after empty-ish: lines containing 'посмотрел' or 'Вечером'
                meet_idx = None
                for i, line in enumerate(sc):
                    if "посмотрел" in line or "Вечером зайдёшь ко мне скинуть" in line:
                        meet_idx = i
                        break
                if meet_idx is not None:
                    mt = sc[meet_idx:]
                    sc = sc[:meet_idx]
            # facial K: meet only first 2–4 lines after peek_meet (parser already split)
            if sid == "mouth_amanda_late_facial" and len(mt) > 6:
                mt = mt[:4]
            # under_table: no meet in pack
            if sid == "mouth_amanda_under_table" and not mt:
                mt = [
                    "— Ты… под столом… смотрел? — Аманда одёргивает подол, губы влажные. — Вечером зайдёшь? Под скатертью так… тесно, а мне всё равно хочется ещё.",
                ]
            # mom amanda: meet without header
            if sid == "mouth_amanda_mom_craftsman" and not mt and sc:
                meet_idx = None
                for i, line in enumerate(sc):
                    if "слышал и смотрел" in line or "Накончал и смылся" in line:
                        meet_idx = i
                        break
                if meet_idx is not None:
                    mt = sc[meet_idx:]
                    sc = sc[:meet_idx]
            sections[sid] = (sc, mt)
            break

print("parsed scenes:", sorted(sections.keys()))
for k, (a, b) in sections.items():
    print(f"  {k}: scene={len(a)} meet={len(b)}")


def qsp_escape(s: str) -> str:
    return s.replace("'", "''")


def emit_pl_block(lines_out: list, paragraphs: list):
    """One *pl per paragraph; single blank line between paragraphs only."""
    paras = [p for p in paragraphs if p is not None and str(p).strip() != ""]
    for i, s in enumerate(paras):
        lines_out.append(f"    *pl '{qsp_escape(s)}'")
        if i < len(paras) - 1:
            lines_out.append("    *pl ' '")


def emit_user_print_loc(sid: str, scene_lines, meet_lines) -> str:
    lines = []
    lines.append(f"! [USER] pack v3 scene: {sid}")
    lines.append(f"#HallMissingUserScene_{sid}")
    if not scene_lines:
        lines.append("    ! empty scene body")
    else:
        emit_pl_block(lines, scene_lines)
    lines.append("---")
    lines.append("")
    lines.append(f"! [USER] pack v3 peek_meet: {sid}")
    lines.append(f"#HallMissingUserMeet_{sid}")
    if not meet_lines:
        lines.append("    ! no peek_meet in pack for this id — AGENT may fill via HallMissingAgentMeet")
        lines.append("    gs 'HallMissingAgentMeet'")
    else:
        emit_pl_block(lines, meet_lines)
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


# --- AGENT filler scenes (short multi-pl) ---
AGENT = {
    "tits_lick_amanda": (
        [
            "В подсобке Аманда прижата к бочке: лиф сдвинут, мастеровой жадно лижет и сосёт её маленькую грудь, пальцами мнёт сосок. Она дышит ртом, пальцы в его волосах, краснеет до ушей — но не отталкивает.",
            "— Тише… — почти стонет. — За дверью…",
            "Монета звякает на бочке. Аманда одёргивает лиф, вытирает влагу платком — в зал без следов.",
        ],
        [
            "— Ты же смотрел… Понравилось? Пока только… грудь. Вечером зайдёшь?",
        ],
    ),
    "tits_lick_melissa": (
        [
            "Мелисса у бочки, купец сдвигает ей лиф и лижет грудь уверенно, без спешки. Она выдыхает ровнее, чем хочется, одёргивает кучеряшку.",
            "— Серебро сначала, — тихо. — Потом смелее.",
            "Монета на бочке. Мелисса расправляет лиф, промакивает кожу — чисто.",
        ],
        [
            "— Смотрел. Пока руки и рот на груди. Вечером придёшь — посчитаем иначе.",
        ],
    ),
    "tits_lick_sandra": (
        [
            "В кладовой моряк сдвигает лиф Сандры, жадно целует и лижет тяжёлую грудь, мнёт полушария. Сандра держит его за плечи — не обнимает, но не убирает.",
            "— Тише. Не рычи на всю кухню.",
            "Монета на ящике. Сандра зашнуровывает лиф, вытирает кожу полотенцем.",
        ],
        [
            "— Насмотрелся? Грудь — не бесплатно. Вечером зайдёшь — мама объяснит тариф.",
        ],
    ),
    "pussy_touch_amanda": (
        [
            "Юбка Аманды задрана. Мастеровой трёт мокрую писечку пальцами, гладит клитор — пальцы блестят. Она вздрагивает, стонет тихо, колени подгибаются.",
            "— Господин… — сбивчиво. — Не… так громко…",
            "Он кончает ей на бедро или в платок; Аманда вытирает всё досуха и опускает подол.",
        ],
        [
            "— Ты видел?.. Руки… между ног. Вечером зайдёшь — проверим без платка?",
        ],
    ),
    "pussy_touch_melissa": (
        [
            "Мелисса разводит колени у ящика. Купец водит пальцами по мокрой щели, входит на фалангу. Она стонет сквозь зубы, смотрит сверху вниз — ещё она решает, сколько это стоит.",
            "— Довольно, — ровно. — Плати.",
            "Монета. Мелисса вытирает пальцы и промежность салфеткой — в зал чисто.",
        ],
        [
            "— Смотрел. Пальцы — не весь уговор. Вечером продолжим?",
        ],
    ),
    "pussy_touch_sandra": (
        [
            "Сандра у стены кладовой, юбка вверх. Купец трёт ей клитор, пальцы мокрые. Она дышит тяжело, ладони на его плечах.",
            "— Тише ты… В зале слышно.",
            "Кончает ей на бедро; Сандра вытирает полотенцем, опускает подол.",
        ],
        [
            "— Присматривал? Пальцы — разминка. Вечером мама доделает.",
        ],
    ),
    "cock_touch_amanda": (
        [
            "Аманда расстёгивает штаны мастеровому: в ладони — твёрдый ствол. Гладит, сжимает головку, краснеет. Он стонет, упирается лбом ей в плечо.",
            "— Только руками… — шепчет.",
            "Кончает ей в ладонь; она вытирает платок дочиста.",
        ],
        [
            "— Смотрел… Я… рукой. Вечером зайдёшь?",
        ],
    ),
    "cock_touch_melissa": (
        [
            "Мелисса ведёт кулаком по стволу купца уверенно, иногда сплюнув на ладонь. Вторая рука — на яйцах. Темп её.",
            "— Не торопись. Я сама.",
            "Кончает на ладонь; облизывает каплю, остальное — изнанка подола.",
        ],
        [
            "— Справилась руками. Дверь сама не открылась. Вечером зайдёшь?",
        ],
    ),
    "cock_touch_sandra": (
        [
            "Сандра на коленях у бочки, кулак по стволу. Иногда губы касаются головки — смачивает и снова рукой. Молча, ровно.",
            "Горожанин кончает в подставленную ладонь; Сандра вытирает фартук, кивок на дверь.",
        ],
        [
            "— Смотрел, чтобы маму не обидели? Вечером зайдёшь — потушим пожар.",
        ],
    ),
    "mouth_balls_amanda": (
        [
            "Аманда на коленях: сосёт ствол, потом лижет и посасывает яйца, снова головку — глубже. Купец держится за бочку.",
            "Кончает ей в рот; mid — сплёвывает в платок, вытирает губы. В зал без следов.",
        ],
        [
            "— Прости… старалась. Вечером зайдёшь?",
        ],
    ),
    "mouth_balls_melissa": (
        [
            "Мелисса работает ртом и яйцами без спешки: губы, язык, снова ствол. Мастеровой едва стоит.",
            "Сплёвывает в салфетку: — Глотать не обещала.",
        ],
        [
            "— Опять в щели? Внутри горит. Вечером зайдёшь?",
        ],
    ),
    "mouth_balls_sandra": (
        [
            "Сандра на кухне: глубокий рот, яйца в ладони. Молча. Кончает в рот — сплёвывает в ветошь, кивок на дверь.",
        ],
        [
            "— Меньше глазей. Клиент доволен. Деньги в кармане.",
        ],
    ),
    "deepthroat_amanda": (
        [
            "Аманда берёт до горла: всхлипы, слюна, слёзы. Купец трахает рот. Late — show, глоток, почисть. Вытирает лицо.",
        ],
        [
            "— Ты смотрел… Я была хороша? Вечером зайдёшь — зуд снимать?",
        ],
    ),
    "deepthroat_melissa": (
        [
            "Мелисса сама насаживается до паха, шея натягивается. Кончает в горло; она глотает, чистит, поправляет подол.",
        ],
        [
            "— Насмотрелся? Прямо в горло. Вечером — проверить глубину?",
        ],
    ),
    "deepthroat_sandra": (
        [
            "Сандра вбирает до паха на кухне, молча. Show + глоток + clean. Купец платит щедро.",
        ],
        [
            "— Глазей. Хозяйка показала, за что платят. Вечером зайдёшь.",
        ],
    ),
    # anilingus_melissa comes from USER pack when parsed
    "anilingus_amanda": (
        [
            "Аманда прогнулась у бочки, юбка вверх. Мастеровой лижет анус и мокрую щель. Она стонет вполголоса, краснеет — ей стыдно, что нравится.",
            "Кончает ей на попу; она вытирает ложбинку дочиста.",
        ],
        [
            "— Ты видел… там… Вечером зайдёшь?",
        ],
    ),
    "anilingus_sandra": (
        [
            "Сандра подаёт таз у кладовой. Купец лижет анус и письку. — Тише. В зале слышно.",
            "Кончает на ягодицы; Сандра сгребает подтёки, платок, подол вниз.",
        ],
        [
            "— Присматривал? Попа — не для сплетен. Вечером мама договорит.",
        ],
    ),
    "tease_generic": (
        [
            "Пока без секса: ладонь у пояса, шёпот, монета на виду. Обещание дороже дела — дверь на крючке.",
        ],
        [
            "— Смотрел? Пока только слова и руки. Вечером — если заплатишь иначе.",
        ],
    ),
}

header = r'''! ================================================
! FILE: modules/events/hall/hall_missing_girl_text.qsps
! MODULE: events/hall
! USER-OWNED TEXT — художественная проза missing (v3 wire)
!
! МЕТКИ:
!   [USER]  — из docs/prose-hall-missing-pack-v3.md (владелец; правь свободно)
!   [AGENT] — дописано агентом, где в pack не хватало; владелец просмотрит и поправит
!   [LOGIC] — выбор сцены / каркас (багфиксы ок)
!
! Печать: multi-*pl в #HallMissingUserScene_* / #HallMissingAgentScene_*
! Выбор: #HallMissingResolveSceneKey → $HallMissingSceneKey
! ================================================

! --------------------------------
! [LOGIC] Диспетчер
! --------------------------------
#HallMissingGirlPrintText
    $HallMissingPrintTextId = LCASE($ARGS[0])

    if $HallMissingPrintTextId = 'intro':
        $HallMissingSceneKey = ''
        gs 'HallMissingPrintIntro'
    elseif $HallMissingPrintTextId = 'ignore_after':
        gs 'HallMissingPrintIgnoreAfter'
    elseif $HallMissingPrintTextId = 'peek_scene':
        $HallMissingSceneKey = ''
        gs 'HallMissingResolveSceneKey'
        gs 'HallMissingPrintPeekScene'
    elseif $HallMissingPrintTextId = 'peek_meet':
        if $HallMissingSceneKey = '':
            gs 'HallMissingResolveSceneKey'
        end
        gs 'HallMissingPrintPeekMeet'
    elseif $HallMissingPrintTextId = 'interrupt_scene':
        gs 'HallMissingPrintInterrupt'
    elseif $HallMissingPrintTextId = 'thoughts':
        ! пусто — thoughts через HallEventChoiceThoughtsPrint
    end

    ! conflict mood (лёгкий AGENT-хвост, если ссора)
    if $HallMissingPrintTextId = 'intro' or $HallMissingPrintTextId = 'peek_meet' or $HallMissingPrintTextId = 'interrupt_scene' or $HallMissingPrintTextId = 'ignore_after':
        gs 'HallMissingConflictMoodText', $HallMissingPrintTextId
        if $HallMissingConflictMoodText <> '':
            *pl ' '
            *pl $HallMissingConflictMoodText
        end
    end

    killvar '$HallMissingPrintTextId'
---

! --------------------------------
! [LOGIC] Имя + клиент bits
! --------------------------------
#HallMissingEnsurePrintContext
    gs 'HallMissingGirlNormalizeKey', $HallMissingGirl
    $HallMissingGirl = $HallMissingGirlKey

    if $HallMissingGirl = '':
        $HallMissingGirl = 'amanda'
    end

    if $RealName[$HallMissingGirl] = '':
        gs 'HallMissingGirlEnsureName', $HallMissingGirl
    end

    if $HallMissingClient = '':
        $HallMissingClient = 'rich_merchant'
    end
    $HallLewdClient = $HallMissingClient
    if LOC('HallLewdFillClientBits') = 1:
        gs 'HallLewdFillClientBits'
    else
        $HallLewdClientWho = 'гость'
        $HallLewdClientWhoA = 'гостя'
        $HallLewdClientCoin = 'монету'
        $HallLewdClientManner = 'нагло'
    end
---

! --------------------------------
! [LOGIC] band: 1 early / 2 mid / 3 late (как PickPrivateAct)
! --------------------------------
#HallMissingGetActBand
    HallMissingActBand = 1
    if HallMissingGirlStage >= 4 and (HallMissingGirlPrivateCount[$HallMissingGirl] >= 2 or GirlHallLewdStage[$HallMissingGirl] >= 3):
        HallMissingActBand = 3
    elseif HallMissingGirlStage >= 4 or HallMissingGirlPrivateCount[$HallMissingGirl] >= 1:
        HallMissingActBand = 2
    end
---

! --------------------------------
! [LOGIC] $HallMissingSceneKey
! --------------------------------
#HallMissingResolveSceneKey
    gs 'HallMissingEnsurePrintContext'
    gs 'HallMissingGetActBand'

    if $HallMissingSceneKey <> '':
        exit
    end

    $act = LCASE($HallMissingPrivateAct)
    $g = $HallMissingGirl
    $c = LCASE($HallMissingClient)

    if $act = 'client_mouth':
        $act = 'cuni'
    end
    if $act = 'touch':
        $act = 'pussy_touch'
    end

    ! under_table + mouth → USER §5
    if $HallMissingPlace = 'under_table' and ($act = 'mouth' or $act = 'deepthroat' or $act = 'mouth_balls'):
        if $g = 'amanda':
            $HallMissingSceneKey = 'mouth_amanda_under_table'
        elseif $g = 'melissa':
            $HallMissingSceneKey = 'mouth_melissa_mid_spit'
        else
            $HallMissingSceneKey = 'mouth_sandra_mid_spit'
        end
        killvar '$act'
        killvar '$g'
        killvar '$c'
        exit
    end

    if $act = 'petting':
        $HallMissingSceneKey = 'petting_' + $g
    elseif $act = 'hand':
        $HallMissingSceneKey = 'hand_' + $g
    elseif $act = 'cuni':
        $HallMissingSceneKey = 'cuni_' + $g
    elseif $act = 'tits_lick':
        $HallMissingSceneKey = 'tits_lick_' + $g
    elseif $act = 'pussy_touch':
        $HallMissingSceneKey = 'pussy_touch_' + $g
    elseif $act = 'cock_touch':
        $HallMissingSceneKey = 'cock_touch_' + $g
    elseif $act = 'titjob':
        if $c = 'traveler':
            $HallMissingSceneKey = 'titjob_sandra_traveler'
        else
            $HallMissingSceneKey = 'titjob_sandra_merchant'
        end
        if $g <> 'sandra':
            $HallMissingSceneKey = 'hand_' + $g
        end
    elseif $act = 'anilingus':
        if $g = 'melissa':
            $HallMissingSceneKey = 'anilingus_melissa'
        else
            $HallMissingSceneKey = 'anilingus_' + $g
        end
    elseif $act = 'tease' or $act = 'talk' or $act = 'room_invite':
        $HallMissingSceneKey = 'tease_generic'
    elseif $act = 'mouth' or $act = 'mouth_balls' or $act = 'deepthroat':
        ! mid vs late + mom-line craftsman
        if HallMissingActBand >= 3 or $act = 'deepthroat' or $act = 'mouth_balls':
            if $g = 'amanda':
                if $c = 'craftsman' and RAND(1, 100) <= 40:
                    $HallMissingSceneKey = 'mouth_amanda_mom_craftsman'
                elseif $c = 'traveler' and RAND(1, 100) <= 35:
                    if RAND(1, 2) = 1:
                        $HallMissingSceneKey = 'mouth_amanda_late_tongue'
                    else
                        $HallMissingSceneKey = 'mouth_amanda_late_facial'
                    end
                elseif RAND(1, 100) <= 25:
                    $HallMissingSceneKey = 'mouth_amanda_late_show_spit'
                elseif RAND(1, 100) <= 40:
                    $HallMissingSceneKey = 'mouth_amanda_late_tongue_swallow'
                else
                    $HallMissingSceneKey = 'mouth_amanda_late_show'
                end
            elseif $g = 'melissa':
                if $c = 'craftsman' and RAND(1, 100) <= 35:
                    $HallMissingSceneKey = 'mouth_melissa_mom_craftsman'
                elseif RAND(1, 100) <= 45:
                    $HallMissingSceneKey = 'mouth_melissa_late_throat'
                else
                    $HallMissingSceneKey = 'mouth_melissa_late_show'
                end
            else
                $HallMissingSceneKey = 'mouth_sandra_late_swallow'
            end
        else
            ! mid spit
            if $g = 'amanda':
                if $c = 'craftsman' and RAND(1, 100) <= 30:
                    $HallMissingSceneKey = 'mouth_amanda_mom_craftsman'
                else
                    $HallMissingSceneKey = 'mouth_amanda_mid_spit'
                end
            elseif $g = 'melissa':
                if $c = 'craftsman' and RAND(1, 100) <= 35:
                    $HallMissingSceneKey = 'mouth_melissa_mom_craftsman'
                else
                    $HallMissingSceneKey = 'mouth_melissa_mid_spit'
                end
            else
                $HallMissingSceneKey = 'mouth_sandra_mid_spit'
            end
        end
    else
        $HallMissingSceneKey = 'petting_' + $g
    end

    killvar '$act'
    killvar '$g'
    killvar '$c'
---

! --------------------------------
! [LOGIC] print peek scene / meet by key
! --------------------------------
#HallMissingPrintPeekScene
    if $HallMissingSceneKey = '':
        gs 'HallMissingResolveSceneKey'
    end

    $k = $HallMissingSceneKey

'''

# build dispatch if/elseif for user and agent keys
# AGENT only for keys not provided by USER pack
all_user = list(sections.keys())
all_agent = [k for k in AGENT.keys() if k not in sections]
print("AGENT only:", all_agent)

disp_scene = []
disp_meet = []
first = True
for sid in all_user + all_agent:
    loc_u = f"HallMissingUserScene_{sid}" if sid in sections else f"HallMissingAgentScene_{sid}"
    loc_m = f"HallMissingUserMeet_{sid}" if sid in sections else f"HallMissingAgentMeet_{sid}"
    if first:
        disp_scene.append(f"    if $k = '{sid}':")
        first = False
    else:
        disp_scene.append(f"    elseif $k = '{sid}':")
    disp_scene.append(f"        gs '{loc_u}'")

disp_scene.append("    else:")
disp_scene.append("        ! fallback AGENT")
disp_scene.append("        gs 'HallMissingAgentScene_tease_generic'")
disp_scene.append("    end")
disp_scene.append("    killvar '$k'")
disp_scene.append("---")
disp_scene.append("")

first = True
disp_meet.append("#HallMissingPrintPeekMeet")
disp_meet.append("    if $HallMissingSceneKey = '':")
disp_meet.append("        gs 'HallMissingResolveSceneKey'")
disp_meet.append("    end")
disp_meet.append("    $k = $HallMissingSceneKey")
disp_meet.append("")
for sid in all_user + all_agent:
    loc_m = f"HallMissingUserMeet_{sid}" if sid in sections else f"HallMissingAgentMeet_{sid}"
    if first:
        disp_meet.append(f"    if $k = '{sid}':")
        first = False
    else:
        disp_meet.append(f"    elseif $k = '{sid}':")
    disp_meet.append(f"        gs '{loc_m}'")
disp_meet.append("    else:")
disp_meet.append("        gs 'HallMissingAgentMeet_tease_generic'")
disp_meet.append("    end")
disp_meet.append("    killvar '$k'")
disp_meet.append("---")
disp_meet.append("")

# AGENT intro / ignore / interrupt / conflict
agent_frames = r'''
! --------------------------------
! [AGENT] intro / ignore / interrupt / conflict — дописано агентом
! --------------------------------
#HallMissingPrintIntro
    gs 'HallMissingEnsurePrintContext'

    *pl '══════════════════════════════════════════════'
    if $HallMissingPlace = 'kitchen':
        *pl ' ДЕВУШКА ПРОПАЛА С КУХНИ'
    else
        *pl ' ДЕВУШКА ПРОПАЛА ИЗ ЗАЛА'
    end
    *pl '══════════════════════════════════════════════'
    *pl ' '

    if HallMissingFromPlay = 1:
        ! [AGENT]
        *pl 'Только что ' + $RealName[$HallMissingGirl] + ' ещё подыгрывала ' + $HallLewdClientWhoA + ' — и вот её уже нет на месте.'
        *pl ' '
    end

    if $HallMissingPlace = 'under_table':
        ! [AGENT]
        *pl 'У дальнего стола ' + $HallLewdClientWho + ' слишком доволен. Под скатертью — шорох и приглушённый всхлип: ' + $RealName[$HallMissingGirl] + ' пропала вниз.'
    elseif $HallMissingPlace = 'kitchen':
        ! [AGENT]
        *pl $RealName[$HallMissingGirl] + ' ушла на кухню с ' + $HallLewdClientWhoA + '. За дверью слишком тихо для жалобы на еду: дыхание, звон ' + $HallLewdClientCoin + '.'
    elseif $HallMissingPlace = 'stairs':
        ! [AGENT]
        *pl $RealName[$HallMissingGirl] + ' пропала у лестницы. ' + $HallLewdClientWho + ' шептал про ' + $HallLewdClientCoin + ' — теперь под ступенями тишина.'
    elseif $HallMissingPlace = 'second_floor':
        ! [AGENT]
        *pl $RealName[$HallMissingGirl] + ' ушла наверх с ' + $HallLewdClientWhoA + '. Скрип двери, шорох одежды — не «показать комнату».'
    else
        ! [AGENT] storage
        *pl $RealName[$HallMissingGirl] + ' исчезла у подсобки. ' + $HallLewdClientWho + ' держал её за талию — дверь щёлкнула. Изнутри — глухой стон.'
    end
---

#HallMissingPrintIgnoreAfter
    gs 'HallMissingEnsurePrintContext'
    ! [AGENT]
    if HallMissingGirlStage >= 4:
        *pl $RealName[$HallMissingGirl] + ' возвращается через несколько минут. Одежда чуть сбита, губы припухшие; ' + $HallLewdClientWho + ' щедрее обычного. Зал делает вид, что не понял.'
    else
        *pl $RealName[$HallMissingGirl] + ' возвращается позже. Щёки горят, глаза отводит; ' + $HallLewdClientWho + ' слишком доволен. Ещё пара раз — и слухи сами найдут дорогу.'
    end
---

#HallMissingPrintInterrupt
    gs 'HallMissingEnsurePrintContext'
    ! [AGENT]
    if GirlWorkPolicy[$HallMissingGirl] = 3:
        *pl 'Вы врываетесь. ' + $HallLewdClientWho + ' орёт, ' + $RealName[$HallMissingGirl] + ' зло одёргивает одежду: «Ты же сам велел удерживать клиентов. Теперь что — святой?»'
    elseif HallMissingGirlStage >= 4:
        *pl 'Вы обрываете сцену. ' + $HallLewdClientWho + ' матерится; ' + $RealName[$HallMissingGirl] + ' отступает без благодарности — скорее злость, что сорвали игру.'
    else
        *pl 'Вы входите резко. ' + $HallLewdClientWho + ' понимает: не его вечер. ' + $RealName[$HallMissingGirl] + ' у стены, сбитая, юбка смята.'
    end
---

#HallMissingConflictMoodText
    $HallMissingConflictMoodText = ''
    $HallMissingConflictMoodId = LCASE($ARGS[0])

    if GirlConflictUntilDay[$HallMissingGirl] < day:
        exit
    end

    ! [AGENT] короткий хвост при активной ссоре
    if $HallMissingGirl = 'amanda':
        $HallMissingConflictMoodText = 'После ссоры Аманда почти не ищет вашего взгляда: в исчезновении есть и обида, и желание самой решить, что ей можно.'
    elseif $HallMissingGirl = 'melissa':
        $HallMissingConflictMoodText = 'Мелисса пропадает не растерянно. После ссоры она не обязана докладывать каждый шаг хозяину, который путается в приказах.'
    elseif $HallMissingGirl = 'sandra':
        $HallMissingConflictMoodText = 'Сандра исчезает без суеты. После конфликта она сама выбирает, где терпеть, а где ставить точку — без вашего полувзгляда.'
    end

    killvar '$HallMissingConflictMoodId'
---

! Совместимость: старые вызовы PrivateAct/Reaction/Text — пустые (вся проза через PrintText)
#HallMissingGirlPrivateActText
    $HallMissingPrivateActText = ''
    killvar '$HallMissingPrivateActTextId'
---

#HallMissingGirlReaction
    $HallMissingGirlReactionText = ''
    killvar '$HallMissingReactionId'
---

#HallMissingGirlText
    $HallMissingGirlText = ''
    killvar '$HallMissingTextId'
---

#HallMissingAgentMeet
    ! generic agent meet fallback
    gs 'HallMissingAgentMeet_tease_generic'
---

'''

# emit user locs
user_locs = []
for sid, (sc, mt) in sections.items():
    user_locs.append(emit_user_print_loc(sid, sc, mt))

# emit agent locs
agent_locs = []
for sid, (sc, mt) in AGENT.items():
    if sid in sections:
        continue
    agent_locs.append(f"! [AGENT] filler scene: {sid}")
    agent_locs.append(f"#HallMissingAgentScene_{sid}")
    emit_pl_block(agent_locs, sc)
    agent_locs.append("---")
    agent_locs.append("")
    agent_locs.append(f"! [AGENT] filler meet: {sid}")
    agent_locs.append(f"#HallMissingAgentMeet_{sid}")
    emit_pl_block(agent_locs, mt)
    agent_locs.append("---")
    agent_locs.append("")

# complete header dispatch
header_full = header + "\n".join(disp_scene) + "\n" + "\n".join(disp_meet) + agent_frames

final = header_full + "\n".join(user_locs) + "\n".join(agent_locs)
out_path.write_text(final, encoding="utf-8")
print("wrote", out_path, "chars", len(final), "lines", final.count("\n")+1)
print("USER scenes", len(sections), "AGENT", len(AGENT))
