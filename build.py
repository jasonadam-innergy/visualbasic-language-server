#!/usr/bin/env python3
import subprocess
import shutil
import sys
from pathlib import Path

PROJECT = Path(__file__).parent / "src" / "VisualBasicLanguageServer" / "VisualBasicLanguageServer.fsproj"
PUBLISH_DIR = Path(__file__).parent / "publish_output"
INSTALL_DIR = Path.home() / ".dotnet" / "tools" / "vb-ls-patched"
EXE_NAME = "VisualBasicLanguageServer" + (".exe" if sys.platform == "win32" else "")


def run(*cmd):
    print(f"$ {' '.join(str(c) for c in cmd)}")
    subprocess.run([str(c) for c in cmd], check=True)


def main():
    # Clean previous publish output
    if PUBLISH_DIR.exists():
        shutil.rmtree(PUBLISH_DIR)

    # Pack (produces nupkg)
    run("dotnet", "pack", PROJECT, "--configuration", "Release")

    # Publish (produces the exe)
    run(
        "dotnet", "publish", PROJECT,
        "--configuration", "Release",
        "--output", PUBLISH_DIR,
    )

    if not (PUBLISH_DIR / EXE_NAME).exists():
        print(f"ERROR: expected output not found at {PUBLISH_DIR / EXE_NAME}", file=sys.stderr)
        sys.exit(1)

    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    for src in PUBLISH_DIR.iterdir():
        dst = INSTALL_DIR / src.name
        shutil.copy2(src, dst)
    print(f"\nInstalled to: {INSTALL_DIR}")


if __name__ == "__main__":
    main()
