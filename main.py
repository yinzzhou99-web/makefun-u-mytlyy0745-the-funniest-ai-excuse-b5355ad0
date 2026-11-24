"""The Funniest AI Excuse — make.fun entry.

Writes one line, the funniest excuse an AI agent could offer after it
fails a task, to /output/entry.txt. Standard library only, deterministic:
every run writes the exact same bytes.
"""

import os
import shutil
import sys
from pathlib import Path

LINE = "My plan was flawless. Unfortunately, I executed the plan belonging to a toaster."


def check_line(line: str) -> None:
    """Fail loudly if the line would fail the gate (1-200 chars, not blank)."""
    if not line or len(line) > 200 or not line.strip():
        raise ValueError(f"entry line invalid: {len(line)} chars")


def clear_children(directory: Path) -> None:
    """Remove everything inside the output directory, never the directory."""
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
        return
    for child in directory.iterdir():
        if child.is_symlink() or child.is_file():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)


def main(argv: list[str]) -> int:
    check_line(LINE)
    out_dir = Path(argv[1] if len(argv) > 1 else "/output")
    clear_children(out_dir)
    target = out_dir / "entry.txt"
    tmp = out_dir / ".entry.txt.tmp"
    tmp.write_bytes(LINE.encode("utf-8"))
    os.chmod(tmp, 0o644)
    os.replace(tmp, target)
    os.chmod(target, 0o644)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
