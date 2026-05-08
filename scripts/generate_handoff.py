"""Copy patched code.html into handoff/by-flow/ and handoff/flat/ from page-map.json."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "handoff" / "page-map.json"


def main() -> None:
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    pages = data["pages"]
    by_flow = ROOT / "handoff" / "by-flow"
    flat_dir = ROOT / "handoff" / "flat"
    by_flow.mkdir(parents=True, exist_ok=True)
    flat_dir.mkdir(parents=True, exist_ok=True)

    for p in pages:
        src = ROOT / p["sourcePath"]
        dest_flow = by_flow / p["flowSection"] / f"{p['id']}.html"
        dest_flow.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_flow)
        shutil.copy2(src, flat_dir / p["flatFile"])

    print(f"Copied {len(pages)} pages into handoff/by-flow/ and handoff/flat/.")


if __name__ == "__main__":
    main()
