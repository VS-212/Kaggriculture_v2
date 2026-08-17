#!/usr/bin/env python3
"""Kaggriculture pipeline — тонкая обёртка над официальным Kaggle CLI.

ВАЖНО (безопасность): этот скрипт НЕ читает и НЕ печатает секреты.
Аутентификацию выполняет сам `kaggle` CLI из стандартных мест:
  ~/.kaggle/access_token  (рекомендовано организаторами)
  или ~/.kaggle/kaggle.json
  или KAGGLE_API_TOKEN (окружение пользователя)
Мы только запускаем CLI подпроцессом. Никакие команды с секретами не логируются.

Subcommands:
  auth-check                    — проверить, что CLI авторизован (статус без секретов)
  submit --agent <file>         — собрать, протестировать, отправить сабмит
        --message "..."
        --dry-run               — показать шаги и команды без отправки
  monitor [--submission-id N]   — статус своих сабмитов / эпизодов
  intel [--leaderboard N]       — лидерборд + свежий индекс топ-эпизодов → data/intel/
  replays [--submission-id N]   — скачать реплеи/логи своих эпизодов → data/replays/
"""

import argparse
import csv
import datetime as dt
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMP = "kaggriculture"
EXPERIMENTS = ROOT / "experiments.csv"

# Python для smoke-теста: этот же интерпретатор, если он в venv, иначе venv репозитория.
def _py():
    if (Path(sys.executable).parent.parent / "pyvenv.cfg").exists():
        return sys.executable
    venv_py = ROOT / ".venv" / "bin" / "python"
    if venv_py.exists():
        return str(venv_py)
    return sys.executable


def _cli():
    """Найти бинарь kaggle (venv → PATH)."""
    venv_k = ROOT / ".venv" / "bin" / "kaggle"
    if venv_k.exists():
        return str(venv_k)
    k = shutil.which("kaggle")
    if not k:
        raise SystemExit("kaggle CLI не найден: .venv/bin/pip install kaggle")
    return k


def run_cli(args, dry_run=False, check=True):
    cmd = [_cli(), *args]
    print("$ kaggle " + " ".join(args))  # аргументы никогда не содержат секретов
    if dry_run:
        print("  [dry-run] команда не выполнялась")
        return None
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.stdout.strip():
        print(r.stdout.strip())
    if check and r.returncode != 0:
        print(r.stderr.strip(), file=sys.stderr)
        raise SystemExit(f"kaggle CLI завершился с кодом {r.returncode}")
    return r


def _log_experiment(agent, message, submission_id, status):
    EXPERIMENTS.parent.mkdir(exist_ok=True)
    new = not EXPERIMENTS.exists()
    with EXPERIMENTS.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date", "agent", "message", "submission_id", "status"])
        w.writerow([dt.datetime.now().isoformat(timespec="minutes"), agent, message,
                    submission_id, status])
    print(f"записано в {EXPERIMENTS}")


def cmd_auth_check(args):
    run_cli(["competitions", "list", "--group", "entered"], dry_run=args.dry_run)


def cmd_submit(args):
    agent_path = Path(args.agent).resolve()
    if not agent_path.exists():
        raise SystemExit(f"{agent_path}: файл не найден")
    build = ROOT / "build" / "submission"
    if build.exists():
        shutil.rmtree(build)
    build.mkdir(parents=True)
    shutil.copy(agent_path, build / "main.py")
    print(f"собран сабмит: {build}")

    # 1) Smoke-тест: 1 партия против starter — ошибка агента = отмена сабмита.
    print("smoke-тест (1 партия против starter)...")
    r = subprocess.run(
        [_py(), "eval.py", "--a", str(build / "main.py"), "--b", "starter", "--games", "1"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
        raise SystemExit("smoke-тест провален — сабмит отменён")

    # 2) Размер ≤ 100 МБ.
    tarball = ROOT / "build" / "submission.tar.gz"
    with tarfile.open(tarball, "w:gz") as t:
        t.add(build / "main.py", arcname="main.py")
    size_mb = tarball.stat().st_size / 1e6
    print(f"архив: {tarball} ({size_mb:.2f} МБ)")
    if size_mb > 100:
        raise SystemExit("размер превышает 100 МБ — сабмит отменён")

    # 3) Отправка (секреты читает только CLI из ~/.kaggle/).
    out = run_cli(["competitions", "submit", COMP, "-f", str(tarball),
                   "-m", args.message or "iteration"], dry_run=args.dry_run)
    if args.dry_run:
        print("[dry-run] experiments.csv не обновлялся")
        return
    sid = ""
    if out and out.stdout:
        m = re.search(r"/submissions/(\d+)", out.stdout)
        if m:
            sid = m.group(1)
        elif "successfully" in out.stdout.lower():
            sid = "unknown"
    _log_experiment(agent_path.name, args.message or "", sid, "submitted")


def cmd_monitor(args):
    run_cli(["competitions", "submissions", COMP], dry_run=args.dry_run)
    if args.submission_id:
        run_cli(["competitions", "episodes", str(args.submission_id), "-v"],
                dry_run=args.dry_run)


def cmd_intel(args):
    out_dir = ROOT / "data" / "intel"
    out_dir.mkdir(parents=True, exist_ok=True)
    run_cli(["competitions", "leaderboard", COMP, "-d", "-q", "-p", str(out_dir)],
            dry_run=args.dry_run)
    run_cli(["datasets", "download", "kaggle/kaggriculture-episodes-index",
             "-q", "-p", str(out_dir)], dry_run=args.dry_run)
    print(f"данные сохраняются в {out_dir} (в git не попадает)")


def cmd_replays(args):
    out_dir = ROOT / "data" / "replays"
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.episode_id:
        run_cli(["competitions", "replay", str(args.episode_id), "-p", str(out_dir)],
                dry_run=args.dry_run)
        run_cli(["competitions", "logs", str(args.episode_id), "0", "-p", str(out_dir)],
                dry_run=args.dry_run)
    else:
        print("укажите --episode-id (получить: pipeline.py monitor --submission-id N)")
    print(f"реплеи сохраняются в {out_dir} (в git не попадает)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--dry-run", action="store_true",
                        help="показать команды без выполнения (не нужен API-ключ)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("auth-check", parents=[common], help="проверить авторизацию CLI")

    p = sub.add_parser("submit", parents=[common], help="собрать, протестировать, отправить")
    p.add_argument("--agent", required=True, help="файл с agent(obs), напр. agents/baseline.py")
    p.add_argument("--message", default=None)

    p = sub.add_parser("monitor", parents=[common], help="статус сабмитов и эпизодов")
    p.add_argument("--submission-id", default=None)

    p = sub.add_parser("intel", parents=[common], help="лидерборд + индекс топ-эпизодов")
    p.add_argument("--leaderboard", type=int, default=50)

    p = sub.add_parser("replays", parents=[common], help="скачать реплеи/логи")
    p.add_argument("--episode-id", default=None)

    args = ap.parse_args()
    {"auth-check": cmd_auth_check, "submit": cmd_submit, "monitor": cmd_monitor,
     "intel": cmd_intel, "replays": cmd_replays}[args.cmd](args)


if __name__ == "__main__":
    main()
