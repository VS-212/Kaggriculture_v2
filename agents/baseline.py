"""Kaggriculture baseline v0.

Greedy wheat-farmer with a walking scheduler:
  * priority: HARVEST (at max yield) > WATER (daily) > DIG weed > PLANT > MOVE
  * task scan over owned tiles; wheat-only economy
  * market: sell shed wheat each turn, buy one seed when none left
No farm hands, no land purchase yet.
"""

from collections import defaultdict

CROP = "WHEAT"
MAX_YIELD_DAY = 4  # wheat

MOVES = {
    "NORTH": (0, -1),
    "SOUTH": (0, 1),
    "EAST": (1, 0),
    "WEST": (-1, 0),
}


def _tile_ready(tile, day):
    return tile["age"] >= MAX_YIELD_DAY


def _needs_water(tile):
    return not tile["watered_today"] and tile["kind"] == "PLANT"


def _scan_order(me):
    """Order of owned tiles to visit: NW quadrant first (row-major), later quadrants appended."""
    tiles = me["tiles"]
    n = len(tiles)
    owned = set(me["unlocked_quadrants"])
    qmap = {
        "NW": (0, 0),
        "NE": (n // 2, 0),
        "SW": (0, n // 2),
        "SE": (n // 2, n // 2),
    }
    order = []
    for q in ["NW", "NE", "SW", "SE"]:
        if q not in owned:
            continue
        ox, oy = qmap[q]
        for y in range(oy, oy + n // 2):
            for x in range(ox, ox + n // 2):
                order.append((x, y))
    return order


def _manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _step_toward(pos, target):
    dx = target[0] - pos[0]
    dy = target[1] - pos[1]
    if dx > 0:
        return ["EAST"]
    if dx < 0:
        return ["WEST"]
    if dy > 0:
        return ["SOUTH"]
    if dy < 0:
        return ["NORTH"]
    return ["PASS"]


def agent(obs):
    player = obs.get("player", 0)
    farms = obs.get("farms", [])
    private = obs.get("private", {}) or {}
    if not farms or player >= len(farms):
        return {"farmer": ["PASS"], "hands": [], "market": []}

    me = farms[player]
    day = obs.get("day", 0)
    seeds = private.get("seeds", {})
    shed = private.get("shed", {})
    tiles = me["tiles"]
    fx, fy = me["farmer"]
    tile = tiles[fy][fx]

    market = []
    # Sell all wheat sitting in the shed (bulk, single order).
    wheat_shed = shed.get(CROP, 0)
    if wheat_shed > 0:
        market.append(["SELL", CROP, wheat_shed])
    # Keep a seed pipeline: buy when we have none (cheap: $10).
    if seeds.get(CROP, 0) == 0 and me["money"] >= 10:
        market.append(["BUY_SEED", CROP, 1])

    # --- acting on the current tile first ---
    if isinstance(tile, dict):
        if tile.get("kind") == "PLANT" and tile.get("crop") == CROP:
            age = day - tile["planted_day"]
            if tile.get("yield_units", 0) > 0 and age >= MAX_YIELD_DAY:
                return {"farmer": ["HARVEST"], "hands": [], "market": market}
            if not tile["watered_today"]:
                return {"farmer": ["WATER"], "hands": [], "market": market}
        elif tile.get("kind") == "WEED":
            return {"farmer": ["DIG"], "hands": [], "market": market}
    elif tile is None and seeds.get(CROP, 0) > 0:
        return {"farmer": ["PLANT", CROP], "hands": [], "market": market}

    # --- otherwise pick the next task tile and walk there ---
    order = _scan_order(me)
    have_seed = seeds.get(CROP, 0) > 0

    def task_rank(pos):
        t = tiles[pos[1]][pos[0]]
        if isinstance(t, dict) and t.get("kind") == "PLANT":
            age = day - t["planted_day"]
            if not t["watered_today"] and age < MAX_YIELD_DAY:
                return 0  # water first (basic needs or the plant dies)
            if t.get("yield_units", 0) > 0 and age >= MAX_YIELD_DAY:
                return 1  # harvest ready
        if isinstance(t, dict) and t.get("kind") == "WEED":
            return 2 if have_seed else 1
        if t is None and have_seed:
            return 3  # plant
        return None

    best = None
    for pos in order:
        r = task_rank(pos)
        if r is None:
            continue
        if best is None or r < best[0]:
            best = (r, pos)
    if best is not None:
        return {"farmer": _step_toward((fx, fy), best[1]), "hands": [], "market": market}

    return {"farmer": ["PASS"], "hands": [], "market": market}
