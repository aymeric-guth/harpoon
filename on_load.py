import sys
import os
import pathlib
from typing import Any
import json
import re


def on_load(cfg: dict[Any, Any]) -> Any:
    if cfg.get("projects") is None:
        return 1
    dev_dir = pathlib.Path(os.getenv("DEV"))
    if not dev_dir.exists():
        raise FileNotFoundError("DEV is undefined or not present on disk")
    patt = re.compile(f"^{dev_dir}/.*$")
    dev = str(dev_dir)
    projects = {"projects": {}, "global_settings": cfg.get("global_settings")}
    for k, v in cfg.items():
        s = k.replace("${" + "DEV" + "}", dev)
        s = s.replace("$(" + "DEV" + ")", dev)
        s = s.replace("$" + "DEV", dev)
        projects.update({s: v})
    sys.stdout.write(json.dumps(projects))
    return 0


def main(raw: str) -> int:
    try:
        cfg = json.loads(raw)
    except json.JSONDecodeError:
        return 1
    return on_load(cfg)


if __name__ == "__main__":
    sys.exit(main("".join(sys.stdin.readlines())))
