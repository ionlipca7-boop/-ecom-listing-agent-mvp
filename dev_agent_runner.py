#!/usr/bin/env python3
"""Simple developer helper to run project commands and log outputs."""

from __future__ import annotations

import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List

LOG_DIR = Path("logs/dev_agent")


def ensure_log_dir() -> None:
    """Create logging directory if needed."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def build_log_path() -> Path:
    """Build a per-run log path, avoiding filename collisions within the same second."""
    base_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"log_{base_stamp}.txt"
    if not log_path.exists():
        return log_path

    suffix = 1
    while True:
        candidate = LOG_DIR / f"log_{base_stamp}_{suffix}.txt"
        if not candidate.exists():
            return candidate
        suffix += 1


def normalize_command(command: str) -> List[str]:
    """Normalize command input and prefer sys.executable for python commands."""
    parts = shlex.split(command)
    if not parts:
        raise ValueError("No command provided.")

    first = parts[0].lower()
    if first in {"python", "python3", "py"}:
        parts[0] = sys.executable

    return parts


def run_and_log(command: str) -> None:
    """Run command, print output, and save run details to a timestamped log file."""
    ensure_log_dir()
    log_path = build_log_path()

    try:
        cmd_parts = normalize_command(command)
        result = subprocess.run(cmd_parts, capture_output=True, text=True)

        output_chunks = []
        if result.stdout:
            output_chunks.append(result.stdout)
        if result.stderr:
            output_chunks.append(result.stderr)
        output_text = "\n".join(chunk.rstrip("\n") for chunk in output_chunks if chunk)

        if output_text:
            print(output_text)
        else:
            print("(No output)")

        with log_path.open("w", encoding="utf-8") as log_file:
            log_file.write(f"timestamp: {datetime.now().isoformat()}\n")
            log_file.write(f"command: {command}\n")
            log_file.write(f"return_code: {result.returncode}\n\n")
            log_file.write("output:\n")
            log_file.write(output_text if output_text else "(No output)")
            log_file.write("\n")

        print(f"\nLog saved: {log_path}")

    except (ValueError, FileNotFoundError) as exc:
        error_msg = f"Error: {exc}"
        print(error_msg)

        with log_path.open("w", encoding="utf-8") as log_file:
            log_file.write(f"timestamp: {datetime.now().isoformat()}\n")
            log_file.write(f"command: {command}\n")
            log_file.write("return_code: N/A\n\n")
            log_file.write("output:\n")
            log_file.write(error_msg + "\n")

        print(f"Log saved: {log_path}")


def display_menu() -> None:
    """Display the command menu and handle user selection."""
    while True:
        print("\n============================")
        print("DEV AGENT RUNNER")
        print("============================\n")
        print("1. Run listing pipeline")
        print("2. Inspect latest run")
        print("3. Export latest run")
        print("4. Run custom command")
        print("5. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            run_and_log(f"{sys.executable} run_listing_pipeline.py")
        elif choice == "2":
            run_and_log(f"{sys.executable} inspect_run.py")
        elif choice == "3":
            run_and_log(f"{sys.executable} export_run.py")
        elif choice == "4":
            custom_command = input("Enter command: ").strip()
            run_and_log(custom_command)
        elif choice == "5":
            print("Exiting Dev Agent Runner.")
            break
        else:
            print("Invalid option. Please select 1-5.")


if __name__ == "__main__":
    display_menu()
