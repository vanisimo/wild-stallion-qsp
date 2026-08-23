# Audit: локации день/ночь, открыто/закрыто, сундуки, апгрейды, древо, подслушивание

**Дата:** 2026-08  
**Скрипт-снимок:** `{SCRATCH}/location_props_audit.txt`  
**Канон арта:** люди/NPC **не** трогаем; фокус — места и объекты.

---

## 1. День / ночь (time → ключ файла)

`#ImageTimeKey` / `#GetLocationTimeSuffix`:

| `time` | Ключ |
|--------|------|
| 1 | morning |
| 2–3 | day |
| 4 | evening |
| 5 | night |

### Wired + assets OK

| Локация | Helper | Папка ассетов | morning/day/evening/night |
|---------|--------|---------------|---------------------------|
| Улица | `ShowLocationTimeImage` → `images/locations/street` | `street/` | **есть** |
| Зал | `ShowTavernHallImage` / TimeImage | `tavern/hall/` | **есть** |
| Кухня | `ShowTavernKitchenImage` | `tavern/kitchen/` (+ дубли `tavern/kitchen_*.png`) | **есть** |
| 2-й этаж | `ShowTavernSecondFloorImage` | `tavern/second_floor/` | **есть** |
| Рынок | TimeImage `market/market` | `market/market/` | **есть** |
| Площадь танцев | TimeImage `market/dance` | `market/dance/` | **есть** |
| Порт | ShowImage + time files | `port/general/` | **есть** |
| Комнаты A/M/S/player | `ShowLocationImage` (см. §1.1) | `rooms/{girl}/` | **файлы есть** |

### 1.1 Пути комнат

Вызов: `gs 'ShowLocationImage', 'sandra_room'` → `images/locations/sandra_room_{time}.png`  
**Файлы есть** на корне `images/locations/` (`sandra_room_day.png` и т.д.).  
Дубли также в `images/locations/rooms/sandra/{time}.png` (для TimeImage-стиля).  

Сундуки: `rooms/sandra/chest` → `…/rooms/sandra/chest_day.png` — **OK**.  
Аманда дверь: `amanda_room_door_closed` — отдельный ключ.

---

## 2. Открыто / закрыто

| Место | Код | Ассет closed | Статус |
|-------|-----|--------------|--------|
| Лавка Бекки | `ShowImage` becky/shop/closed | `becky/shop/closed.jpg/png` | **OK** |
| Ирма | closed | `irma/shop/closed.*` | **OK** |
| Вино | closed | `wine/shop/closed.*` | **OK** |
| Драупнир | closed + SceneShowVisual shop | `draupnir/shop/closed.*` + batch webp | **OK** |
| Сладости | closed | `market/sweets/closed.*` | **OK** |
| Пост стражи | closed / normal / talk | `guard/post/closed.*` + time | **OK** |
| Воскресные визиты | подслушка у **закрытых** лавок | closed shops + debug panel art | **OK** (текст); картинка = closed shop / SceneShowVisual |

---

## 3. Трактир с улучшениями (вывеска / фасад)

Код: `#ShowTavernExteriorImage`  
Путь: `images/locations/tavern/exterior/{time}_sign_{old|new}.jpg`  
Флаг: `TavernUpgradeSignDone` → `new`, иначе `old`.

| time × sign | jpg |
|-------------|-----|
| morning/day/evening/night × old/new | **все 8 jpg есть** |

Часть png-дублей отсутствует (day_sign_*.png) — не критично, helper просит **jpg**.

Другие апгрейды (кухня/бар/погреб/сцена…) — экономика в `tavern_upgrades.qsps`; **отдельных location plates под каждый апгрейд нет** (только фасад old/new + debug panel / Draupnir upgrades empty counter из batch-2).

---

## 4. Сундуки

| Сундук | Код | Ассет | Статус |
|--------|-----|-------|--------|
| Стефан | `#PlayerRoomChest` → `ShowLocationImage 'rooms/player/chest'` | `chest_{morning,day,evening,night}.png` | **OK** (+ night) |
| Сандра (письмо Лермонта) | `#SandraLermontLetterShowChestImage` → `rooms/sandra/chest` | `chest_*` + `ASSET-chest.txt` | **OK** (placeholder = копия player до финального арта) |
| Management | `tavern/management/chest.png` | один кадр | **OK** (не time-set) |
| Аманда / Мелисса | текст «сундук» в комнате | **отдельного chest_* нет** | только room plate |

**Тайник Сандры / «деревянный фалос»:**  
В `ASSET-chest.txt` канон: **намёк** (утолщённая боковая панель), **без** явного фаллоимитатора на кадре.  
Отдельного файла `*dildo* / *phallus*` в `images/` **нет** (MISS).  
В prose: «тайник не только бумага» (`sandra_lermont_letter_talk_text`) — объект подразумевается, **не** отдельный visual key.

---

## 5. Древо

| Ассет | Путь | Использование |
|-------|------|----------------|
| Обычное | `images/locations/tree/normal.jpg` | gift/dream helpers |
| Ancestral staff | `images/locations/tree/ancestral.jpg` | `#ShowDreamItemImage` / Irma–Inga dream (`gift_dream_images.qsps`) |

Отдельной walkable-локации `#Tree` как карты города **не найдено** — это **объект/картинка подарка**, не street hub.

---

## 6. Подслушивание

| Сцена | Visual сейчас | Статус |
|-------|---------------|--------|
| Церковь: окно / щель | `ShowImage 'church','window','ajar'` → `church/window/ajar.png` | **OK** (финальный арт, ASSET-ajar) |
| Church spy Becky (исповедальня) | prose в `church_spy_*`; **отдельного SceneShowVisual под spy-step** — проверить runtime (часто church interior / stub) | **частично** |
| Воскресенье у закрытых лавок (Becky/Sandra, Clarissa/Melissa, Irma/Inga) | closed shop image +/или SceneShowVisual debug | **closed OK**; dedicated «подслушка» plate — нет |
| Becky backroom peek | `becky/shop/backroom_peek.png` | **OK** |

---

## 7. Сводка gaps (объекты / места)

| # | Gap | Приоритет |
|---|-----|-----------|
| 1 | **Явный арт деревянного фалоса Сандры** — нет файла; канон chest = намёк only | P2 (если нужен close-up объекта — отдельный key) |
| 2 | Путь `ShowLocationImage 'sandra_room'` vs файлы `rooms/sandra/day` | P1 проверить в плеере / поправить маппинг |
| 3 | Апгрейды трактира кроме **вывески** — нет per-upgrade plates | P2 |
| 4 | Church spy steps — нет dedicated object plates (окно ajar есть) | P2 |
| 5 | Sunday eavesdrop — нет отдельного «ушко у двери» кадра | P3 |
| 6 | exterior day_sign `png` twins | P3 (jpg хватает) |

---

## 8. Что уже хорошо для «локации без людей»

- Полные **time-sets** street / hall / kitchen / 2F / market / dance / port / rooms  
- **Фасад** old/new × 4 времени  
- **Closed** магазины + guard  
- **Chests** player + sandra (time) + management  
- **Tree** normal + ancestral  
- **Spy window ajar**  
- Batch-2 empty desks/doors/crates (debug/supply/rats/upgrades)

---

*Не генерить лица NPC. Для фалоса — только если владелец закажет явный object close-up; иначе оставить намёк в сундуке.*
