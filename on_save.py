import sys
import os
import pathlib
from typing import Any
import json
import re


def on_save(cfg: dict[Any, Any]) -> Any:
    if cfg.get("projects") is None:
        return 1
    dev_dir = pathlib.Path(os.getenv("DEV"))
    if not dev_dir.exists():
        raise FileNotFoundError("DEV is undefined or not present on disk")
    dev = str(dev_dir)
    patt = re.compile(f"^{dev_dir}/.*$")
    projects = {"projects": {}, "global_settings": cfg.get("global_settings")}
    for k, v in cfg.get("projects").items():
        if patt.match(k):
            projects.update({f"$DEV{k[len(str(dev)) :]}": v})
    sys.stdout.write(json.dumps(projects))
    return 0


def main(raw: str) -> int:
    try:
        cfg = json.loads(raw)
    except json.JSONDecodeError:
        return 1
    return on_save(cfg)


if __name__ == "__main__":
    sys.exit(main("".join(sys.stdin.readlines())))
