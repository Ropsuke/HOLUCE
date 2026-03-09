import random
# 1. SINU ORIGINAALNE KAART (Sisu, mida sa ei taha muuta)
minu_poe_kaart = [
    ["g", "g", "g", "g", "g", "g", "g", "g", "g"],
    ["g", "g", "g", "g", "g", "g", "g", "g", "g"],
    ["g", "g", "g", "g", "g", "g", "g", "g", "g"],
    ["g", "g", "g", "g", "g", "g", "g", "S", "SS"],
    ["g", "g", "g", "g", "g", "g", "g", "g", "g"],
    ["g", "g", "g", "g", "g", "g", "g", "g", "g"],
    ["g", "g", "g", "g", "g", "g", "g", "g", "g"],
]

minu_muru_kaart = [
    ["E", "E", "E", "E", "E", "E", "E", "E","E", "E", "E", "E", "E", "E", "E", "E","E", "E", "E", "E", "E", "E", "E", "E","E", "E", "E", "E", "E", "E", "E", "E", "E", "E"],
    ["E", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "K", "K", "K", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "K", "D", "K", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "S", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "T", "T", "T", "T", "T", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "T", "T", "T", "T", "T", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "T", "T", "T", "T", "TT", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "T", "T", "T", "T", "T", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "T", "T", "T", "T", "T", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "g", "E"],
    ["E", "E", "E", "E", "E", "E", "E", "E","E", "E", "E", "E", "E", "E", "E", "E","E", "E", "E", "E", "E", "E", "E", "E","E", "E", "E", "E", "E", "E", "E", "E", "E", "E"]
]

# 2. TEEME RAAMI (20 ruutu igasse suunda)
raam = 20
laius = len(minu_muru_kaart[0]) + (raam * 2)

spawn_map = []
# Ülemine raam
for _ in range(raam):
    spawn_map.append(["E"] * laius)

# Keskmine osa (sinu kaart + külgmised raamid)
for rida in minu_muru_kaart:
    spawn_map.append((["E"] * raam) + rida + (["E"] * raam))

# Alumine raam
for _ in range(raam):
    spawn_map.append(["E"] * laius)

    
def koobas(kõrgus, laius):
    grid = []
    for y in range(kõrgus):
        rida = []
        for x in range(laius):
            rida.append("W")
        grid.append(rida)
    start_x = laius // 2
    start_y = kõrgus // 2
    x = start_x
    y = start_y
    grid[y][x] = "."
    samme_vaja = laius * kõrgus * 0.4
    samm_tehtud = 0
    suund = random.randint(1, 4)
    while samm_tehtud < samme_vaja:
        dx = 0
        dy = 0
        if random.random() <0.4:
            suund = random.randint(1, 4)
        if suund == 1:
            dy -= 1
        elif suund == 2:
            dy += 1
        elif suund == 3:
            dx -= 1
        elif suund == 4:
            dx += 1
        uus_x = x + dx
        uus_y = y + dy
        if uus_x < 1 or uus_x > laius - 2 or uus_y < 1 or uus_y > kõrgus - 2:
            continue
        x = uus_x
        y = uus_y
        if grid[y][x] == "W":
            grid[y][x] = "."
            samm_tehtud += 1
        elif grid[y][x] == ".":
            grid[y][x] = "."
            samm_tehtud += 1
    grid[start_y][start_x] = "S"
    grid[y][x] = "D"
    return grid