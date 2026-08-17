"""Kaggriculture local eval harness.

Runs matches between two agents (builtin names, file paths, or callables),
aggregates results (winrate, final money, margin), optionally dumps a replay.

Usage:
    .venv/bin/python eval.py --a agents/baseline.py --b starter --games 50
    .venv/bin/python eval.py --a agents/baseline.py --b random --games 20 --replay out.json
"""

import argparse
import importlib.util
import json
import statistics
import sys
from pathlib import Path

from kaggle_environments import make

HERE = Path(__file__).resolve().parent


def load_agent(spec):
    """Resolve 'builtin-name', '/path/to/file.py' or 'module.attr:function' into a callable or name."""
    if spec in {"pass", "random", "starter"}:
        return spec  # builtin names understood by kaggle-environments
    p = Path(spec)
    if p.exists():
        mod_name = "agent_" + p.stem.replace("-", "_")
        spec_ = importlib.util.spec_from_file_location(mod_name, p)
        mod = importlib.util.module_from_spec(spec_)
        sys.modules[mod_name] = mod
        spec_.loader.exec_module(mod)
        if not hasattr(mod, "agent"):
            raise SystemExit(f"{spec}: file must define agent(obs)")
        return mod.agent
    raise SystemExit(f"{spec}: not a builtin, file not found")


def run_match(agent_a, agent_b, seed, episode_steps=720, debug=False):
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": episode_steps, "seed": seed},
        debug=debug,
    )
    # Alternate first/second seat by seed parity to cancel first-mover effects.
    a_first = seed % 2 == 0
    order = [agent_a, agent_b] if a_first else [agent_b, agent_a]
    env.run(order)
    rewards = [float(s.reward) for s in env.steps[-1]]
    money_a = rewards[0] if a_first else rewards[1]
    money_b = rewards[1] if a_first else rewards[0]
    return money_a, money_b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--games", type=int, default=50)
    ap.add_argument("--start-seed", type=int, default=0)
    ap.add_argument("--steps", type=int, default=720)
    ap.add_argument("--replay", default=None, help="dump one game JSON to this path")
    args = ap.parse_args()

    agent_a = load_agent(args.a)
    agent_b = load_agent(args.b)

    wins_a = wins_b = ties = 0
    moneys_a, moneys_b, margins = [], [], []
    for i in range(args.games):
        seed = args.start_seed + i
        ma, mb = run_match(agent_a, agent_b, seed, args.steps)
        moneys_a.append(ma)
        moneys_b.append(mb)
        margins.append(ma - mb)
        if ma > mb:
            wins_a += 1
        elif mb > ma:
            wins_b += 1
        else:
            ties += 1
        if args.replay and i == 0:
            env = make("kaggriculture", configuration={"episodeSteps": args.steps, "seed": seed})
            a_first = seed % 2 == 0
            env.run([agent_a, agent_b] if a_first else [agent_b, agent_a])
            out = Path(args.replay)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(env.toJSON()))
            print(f"replay written to {args.replay}")

    print(f"=== {args.a}  vs  {args.b}  ({args.games} games, seeds {args.start_seed}..{args.start_seed + args.games - 1}) ===")
    print(f"A wins: {wins_a} ({wins_a / args.games:.0%})   B wins: {wins_b} ({wins_b / args.games:.0%})   ties: {ties}")
    print(f"A money: mean {statistics.mean(moneys_a):,.0f}  median {statistics.median(moneys_a):,.0f}")
    print(f"B money: mean {statistics.mean(moneys_b):,.0f}  median {statistics.median(moneys_b):,.0f}")
    print(f"A margin: mean {statistics.mean(margins):+,.0f}  median {statistics.median(margins):+,.0f}")


if __name__ == "__main__":
    main()
