import pathlib, hashlib
root = pathlib.Path(r"D:/traktir/images/locations")

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

required = [
  "tavern/hall/day.jpg", "tavern/kitchen/day.jpg", "tavern/second_floor/day.jpg",
  "tavern/exterior/day_sign_old.jpg", "tavern/exterior/day_sign_new.jpg",
  "tavern/exterior/night_sign_new.jpg", "tavern/exterior/night_sign_old.jpg",
  "tavern/exterior/morning_sign_old.jpg", "tavern/exterior/morning_sign_new.jpg",
  "mayor/office/clerk.png", "mayor/office/clerk_money.png", "mayor/office/mayor.png",
  "becky/shop/normal.jpg", "becky/shop/closed.jpg", "irma/shop/normal.jpg",
  "wine/shop/normal.jpg", "clarissa/shop/closed.jpg", "inga/shop/closed.jpg",
  "player_room_morning.png", "player_room_day.png", "player_room_evening.png", "player_room_night.png",
  "street/day.jpg", "port/general/day.jpg",
]
missing = [p for p in required if not (root/p).exists() or (root/p).stat().st_size < 1000]
assert not missing, missing
print("PASS required assets", len(required))

# uniqueness
pairs = [
  ("clarissa/shop/closed.jpg", "wine/shop/closed.jpg"),
  ("inga/shop/closed.jpg", "becky/shop/closed.jpg"),
  ("tavern/exterior/night_sign_new.jpg", "tavern/exterior/day_sign_new.jpg"),
  ("player_room_morning.png", "player_room_night.png"),
  ("player_room_evening.png", "player_room_night.png"),
]
for a,b in pairs:
  ha, hb = md5(root/a), md5(root/b)
  assert ha != hb, (a,b,"identical")
  print("PASS distinct", a, "!=", b)

src = pathlib.Path(r"D:/traktir/modules/core/show_image/image_debug_random.qsps").read_text(encoding="utf-8")
assert "images/locations/tavern/second_floor" in src
assert "ShowTavernExteriorImage" in src
street = pathlib.Path(r"D:/traktir/modules/locations/town/street.qsps").read_text(encoding="utf-8")
# exterior must NOT auto-stack on every Street enter
assert "Осмотреть фасад трактира" in street
# count of ShowTavernExteriorImage in Street main flow: only inside act
assert street.count("gs 'ShowTavernExteriorImage'") == 1
print("PASS street exterior only on facade act")
print("ALL VERIFY PASS")
