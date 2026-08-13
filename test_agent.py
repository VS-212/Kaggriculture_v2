"""Local benchmark harness: run main.agent against built-in agents."""
import sys
import json
import time
from kaggle_environments import make

import main


def run_match(agentA, agentB, steps=720, seed=None, debug=False):
    cfg = {"episodeSteps": steps}
    if seed is not None:
        cfg["seed"] = seed
    env = make("kaggriculture", configuration=cfg, debug=debug)
    env.run([agentA, agentB])
    final = env.steps[-1]
    r = [s.reward for s in final]
    return r[0], r[1], env


def bench(agent, opp, n=5):
    wins = 0
    totals = []
    t0 = time.time()
    for i in range(n):
        a, b, env = run_match(agent, opp, seed=1000 + i)
        totals.append((a, b))
        if a > b:
            wins += 1
    dt = time.time() - t0
    print(f"{agent} vs {opp}: wins {wins}/{n}  "
          f"avg A={sum(a for a, b in totals)/n:.0f} B={sum(b for a, b in totals)/n:.0f}  "
          f"({dt:.1f}s)")
    return totals


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "starter"):
        bench(main.agent, "starter")
    if which in ("all", "random"):
        bench(main.agent, "random")
    if which in ("all", "self"):
        bench(main.agent, main.agent)
    if which in ("all", "pass"):
        bench(main.agent, "pass")
