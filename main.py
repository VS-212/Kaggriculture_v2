"""
Kaggriculture agent (v9).

Production is sized to the town's shop draw (observable, drawn with
replacement): animals (cow->milk, sheep->wool, goose->eggs) sized to our share
of milk/wool/egg demand, and crops (wheat for feed, plus strawberry and carrot
sold for cash) sized to crop demand. This diversification keeps the farm alive
even when the draw has no animal-product demand. Daily FEED + CARE +
COLLECT_FERTILIZER; HARVEST near cap. Wheat is grown and bought as a top-up.
Market orders are budgeted: hires first, then sells, then feed/seed/animals.
"""

CROPS = {
    "WHEAT":      {"seed": 10, "first_yield_day": 2, "max_yield_day": 4, "max_yield": 6},
    "CARROT":     {"seed": 20, "first_yield_day": 2, "max_yield_day": 3, "max_yield": 4},
    "TOMATO":     {"seed": 50, "first_yield_day": 8, "max_yield_day": 8, "max_yield": 4},
    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "max_yield": 4},
    "MELON":      {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "max_yield": 6},
}

ANIMALS = {
    "GOOSE": {"cost": 300, "structure": "COOP",    "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}

SHOP_PRODUCTS = {
    "BAKERY":         ["EGG", "WHEAT"],
    "PIZZA_SHOP":     ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT":    ["EGG", "WHEAT", "STRAWBERRY"],
    "YARN_STORE":     ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"],
    "PET_CAFE":       ["CARROT"],
    "SMOOTHIE_SHOP":  ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}

_N_TYPES = len(SHOP_PRODUCTS)
_MAX_SHOPS = 8
PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
            "EGG", "MILK", "WOOL", "FERTILIZER"]

# ---- tunables ------------------------------------------------------------
WHEAT_TILES = 12
STRAW_TILES = 6
CARROT_TILES = 10
FEED_RESERVE_DAYS = 3
ANIMAL_BUY_CUTOFF = 16
BUY_LAND_CUTOFF = 12
CASH_BUFFER = 400
DEMAND_SHARE = 0.5
MILK_SHARE = 0.6      # milk has 3 shops: can absorb more supply
WOOL_SHARE = 0.45     # wool has 1 shop: very fragile to oversupply
EGG_SHARE = 0.5
NUM_HANDS = 6
_RATE = {"COW": 1.5, "SHEEP": 4.0 / 3.0, "GOOSE": 2.0}


def _shed_adjacent(pos, board):
    half = board // 2
    return tuple(pos) in {(half - 1, half - 1), (half, half - 1),
                          (half - 1, half), (half, half)}


def _fib_cost(h):
    a, b = 1, 1
    for _ in range(h):
        a, b = b, a + b
    return a


def _expected_demand(shops, product):
    """Expected units/day of `product` consumed by the town by season end."""
    total = 0.0
    remaining = _MAX_SHOPS - len(shops)
    for sname, prods in SHOP_PRODUCTS.items():
        if product not in prods:
            continue
        rate = 12.0 if len(prods) == 1 else 6.0  # single-product shops eat 2x
        observed = sum(1 for s in shops if s == sname)
        total += (observed + remaining / float(_N_TYPES)) * rate
    return total + 1.0  # town center consumes one of everything per day


def agent(obs):
    player = obs["player"]
    me = obs["farms"][player]
    priv = obs["private"]
    tiles = me["tiles"]
    board = len(tiles)
    day = obs["day"]
    money = me["money"]
    shed = priv["shed"]
    seeds = priv["seeds"]
    inventories = priv["inventories"]
    prices = obs["market"]["prices"]
    shops = obs["town"]["unlocked_shops"]

    units = [tuple(me["farmer"])] + [tuple(h) for h in me["hands"]]
    n_units = len(units)

    animals = []
    plants = []
    weeds = []
    empty_tiles = []
    empty_structs = {"COOP": [], "PASTURE": []}
    for y in range(board):
        for x in range(board):
            t = tiles[y][x]
            if isinstance(t, dict):
                k = t.get("kind")
                if k == "PLANT":
                    plants.append((x, y, t))
                elif k == "WEED":
                    weeds.append((x, y, t))
                elif k in ("COOP", "PASTURE"):
                    if t.get("animal"):
                        animals.append((x, y, t))
                    else:
                        empty_structs[k].append((x, y))
            elif t is None:
                empty_tiles.append((x, y))

    n_animals = len(animals)
    unfed = sum(1 for a in animals if not a[2]["fed_today"])
    wheat_in_shed = shed.get("WHEAT", 0)

    def count_type(anim):
        n = sum(1 for a in animals if a[2]["animal"] == anim)
        n += shed.get(anim, 0)
        for inv in inventories:
            n += inv.get(anim, 0)
        return n

    n_cows = count_type("COW")
    n_sheep = count_type("SHEEP")
    n_goose = count_type("GOOSE")

    milk_d = _expected_demand(shops, "MILK")
    wool_d = _expected_demand(shops, "WOOL")
    egg_d = _expected_demand(shops, "EGG")
    target_cows = int(round(milk_d * MILK_SHARE / _RATE["COW"]))
    target_sheep = int(round(wool_d * WOOL_SHARE / _RATE["SHEEP"]))
    target_goose = int(round(egg_d * EGG_SHARE / _RATE["GOOSE"]))

    def count_plant(crop):
        return sum(1 for p in plants if p[2]["crop"] == crop)

    endgame = day >= 28

    # ================= MARKET =================
    market = []
    order_budget = 10

    def push(o):
        if len(market) < order_budget:
            market.append(o)

    wheat_tiles = count_plant("WHEAT")
    straw_tiles = count_plant("STRAWBERRY")
    carrot_tiles = count_plant("CARROT")
    reserve = n_animals * FEED_RESERVE_DAYS + 4
    if endgame:
        reserve = 0

    # 1) hires first
    hires_now = me["hires_today"]
    while hires_now < NUM_HANDS and len(market) < order_budget - 2:
        cost = _fib_cost(hires_now)
        if money < cost:
            break
        push(["HIRE"])
        hires_now += 1

    # 2) sells (revenue); most-contested first, then crops
    if endgame:
        sell_items = list(PRODUCTS)
    else:
        sell_items = ["MILK", "WOOL", "EGG", "FERTILIZER",
                      "STRAWBERRY", "CARROT", "TOMATO", "MELON"]
    for item in sell_items:
        q = shed.get(item, 0)
        if item == "WHEAT" and not endgame:
            q = max(0, q - reserve)
        if q > 0:
            push(["SELL", item, q])

    # 3) seeds (feed wheat first, then strawberry early, then carrot)
    if not endgame:
        want_wheat = max(0, WHEAT_TILES - wheat_tiles - seeds.get("WHEAT", 0))
        if want_wheat > 0 and money >= 10:
            push(["BUY_SEED", "WHEAT", min(5, want_wheat)])
        if day <= 10:
            want_straw = max(0, STRAW_TILES - straw_tiles - seeds.get("STRAWBERRY", 0))
            if want_straw > 0 and money >= 100:
                push(["BUY_SEED", "STRAWBERRY", min(3, want_straw)])
        want_carrot = max(0, CARROT_TILES - carrot_tiles - seeds.get("CARROT", 0))
        if want_carrot > 0 and money >= 20:
            push(["BUY_SEED", "CARROT", min(5, want_carrot)])

    # 4) wheat product (feed top-up)
    if not endgame:
        short = reserve - wheat_in_shed
        if short > 0 and money >= prices.get("WHEAT", 25):
            push(["BUY_PRODUCT", "WHEAT", min(6, short)])

    # 5) animals (buffer-gated)
    if not endgame and day <= ANIMAL_BUY_CUTOFF:
        buf = CASH_BUFFER
        if n_cows < 1 and money >= 420 + buf:
            push(["BUY_ANIMAL", "COW", 1])
        elif n_sheep < 4 and money >= 500 * (4 - n_sheep) + buf:
            push(["BUY_ANIMAL", "SHEEP", 4 - n_sheep])
        elif n_cows < target_cows and money >= 420 + buf:
            push(["BUY_ANIMAL", "COW", 1])
        elif n_sheep < target_sheep and money >= 520 + buf:
            push(["BUY_ANIMAL", "SHEEP", 1])
        elif n_goose < target_goose and money >= 320 + buf:
            push(["BUY_ANIMAL", "GOOSE", 1])

    # 6) land
    if not endgame and 4 <= day <= BUY_LAND_CUTOFF:
        if len(me["unlocked_quadrants"]) < 2 and money >= 1500:
            push(["BUY_LAND"])

    # ================= UNITS =================
    n_feeders = min(3, max(1, (n_animals + 5) // 6))
    plan = {"claimed": set(), "wheat_avail": wheat_in_shed}

    # plant preferences: (crop, priority)
    plant_pref = []
    if not endgame:
        if seeds.get("WHEAT", 0) > 0:
            plant_pref.append(("WHEAT", 935))
        if day <= 10 and seeds.get("STRAWBERRY", 0) > 0:
            plant_pref.append(("STRAWBERRY", 930))
        if seeds.get("CARROT", 0) > 0:
            plant_pref.append(("CARROT", 925))

    actions_out = []
    for i in range(n_units):
        pos = units[i]
        inv = inventories[i] if i < len(inventories) else {}
        act = _choose_action(i, pos, inv, board, day, tiles, shed, seeds,
                             animals, plants, weeds, empty_tiles, empty_structs,
                             plan, endgame, unfed, n_feeders, plant_pref)
        actions_out.append(act)

    return {"farmer": actions_out[0], "hands": actions_out[1:], "market": market}


def _choose_action(idx, pos, inv, board, day, tiles, shed, seeds,
                   animals, plants, weeds, empty_tiles, empty_structs,
                   plan, endgame, unfed, n_feeders, plant_pref):
    px, py = pos
    claimed = plan["claimed"]
    is_feeder = idx < n_feeders

    if is_feeder:
        my_wheat = inv.get("WHEAT", 0)
        if (my_wheat <= 0 and unfed > 0 and plan["wheat_avail"] > 0
                and _shed_adjacent(pos, board)):
            batch = min(unfed, plan["wheat_avail"], 20)
            plan["wheat_avail"] -= batch
            return ["PICKUP", "WHEAT", batch]
        if my_wheat > 0 and unfed > 0:
            best = None
            for (x, y, t) in animals:
                if t["fed_today"]:
                    continue
                key = (x, y, "FEED")
                if key in claimed:
                    continue
                d = abs(px - x) + abs(py - y)
                if best is None or d < best[0]:
                    best = (d, x, y, key)
            if best is not None:
                d, x, y, key = best
                claimed.add(key)
                if px == x and py == y:
                    return ["FEED"]
                return _step_toward(pos, x, y)

    carrying = [an for an in ANIMALS if inv.get(an, 0) > 0]
    if not carrying and _shed_adjacent(pos, board):
        for an in ["COW", "SHEEP", "GOOSE"]:
            if shed.get(an, 0) > 0 and empty_structs[ANIMALS[an]["structure"]]:
                return ["PICKUP", an, 1]

    best = None
    best_key = None

    def consider(priority, tx, ty, action):
        nonlocal best, best_key
        key = (tx, ty, action[0])
        if key in claimed:
            return
        d = abs(px - tx) + abs(py - ty)
        score = (priority, -d)
        if best is None or score > best[0]:
            best = (score, action, tx, ty)
            best_key = key

    for (x, y, t) in animals:
        if not t["fed_today"] and inv.get("WHEAT", 0) > 0:
            urg = 1000 if t["consecutive_unfed"] >= 1 else 985
            consider(urg, x, y, ["FEED"])

    for (x, y, t) in plants:
        if not t["watered_today"]:
            urg = 1000 if t["consecutive_unwatered"] >= 1 else 985
            consider(urg, x, y, ["WATER"])

    for (x, y, t) in animals:
        a = ANIMALS[t["animal"]]
        if 0 < t["yield_units"] >= a["max_held"] - 1:
            consider(950, x, y, ["HARVEST"])

    if carrying:
        an = carrying[0]
        for (x, y) in empty_structs[ANIMALS[an]["structure"]]:
            consider(945, x, y, ["PLACE", an])
    for an in ["COW", "SHEEP", "GOOSE"]:
        st = ANIMALS[an]["structure"]
        if (shed.get(an, 0) > 0 or inv.get(an, 0) > 0) and not empty_structs[st]:
            for (x, y) in empty_tiles:
                consider(940, x, y, ["BUILD_" + st])
            break
    for (crop, pr) in plant_pref:
        for (x, y) in empty_tiles:
            if seeds.get(crop, 0) > 0:
                consider(pr, x, y, ["PLANT", crop])

    for (x, y, t) in animals:
        if not t["cared_today"]:
            consider(930, x, y, ["CARE"])
        if t["fertilizer_available"]:
            consider(920, x, y, ["COLLECT_FERTILIZER"])

    for (x, y, t) in plants:
        crop = t["crop"]
        cd = CROPS[crop]
        age = day - t["planted_day"]
        if t["yield_units"] > 0 and age >= cd["first_yield_day"]:
            consider(900, x, y, ["HARVEST"])

    for (x, y, t) in weeds:
        consider(600, x, y, ["DIG"])

    if best is None:
        return ["PASS"]

    (score, action, tx, ty) = best
    if best_key is not None:
        claimed.add(best_key)

    if px == tx and py == ty:
        return action
    return _step_toward(pos, tx, ty)


def _step_toward(pos, tx, ty):
    px, py = pos
    if px < tx:
        return ["EAST"]
    if px > tx:
        return ["WEST"]
    if py < ty:
        return ["SOUTH"]
    if py > ty:
        return ["NORTH"]
    return ["PASS"]
