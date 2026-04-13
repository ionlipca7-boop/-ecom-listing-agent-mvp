#!/usr/bin/env python3
"""Simple developer helper to run project commands and log outputs."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

LOG_DIR = Path("logs/dev_agent")
PROJECT_ROOT = Path(__file__).resolve().parent
RUN_LISTING_PIPELINE_SCRIPT = PROJECT_ROOT / "run_listing_pipeline.py"
INSPECT_RUN_SCRIPT = PROJECT_ROOT / "inspect_run.py"
EXPORT_RUN_SCRIPT = PROJECT_ROOT / "export_run.py"


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


def safe_print(message: str) -> None:
    """Print text safely even when terminal encoding cannot represent all characters."""
    try:
        print(message)
    except UnicodeEncodeError:
        stdout_encoding = sys.stdout.encoding or "utf-8"
        sanitized = message.encode(stdout_encoding, errors="replace").decode(stdout_encoding, errors="replace")
        print(sanitized)


def build_utf8_env() -> Dict[str, str]:
    """Build a UTF-8-safe child process environment."""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def run_and_log(
    command: str,
    resolved_script_path: Optional[Path] = None,
    env: Optional[Dict[str, str]] = None,
    force_utf8_decode: bool = False,
) -> None:
    """Run command, print output, and save run details to a timestamped log file."""
    ensure_log_dir()
    log_path = build_log_path()
    run_cwd = str(PROJECT_ROOT)

    try:
        cmd_parts = normalize_command(command)

        if force_utf8_decode:
            result = subprocess.run(cmd_parts, capture_output=True, text=False, cwd=run_cwd, env=env)
            stdout_text = result.stdout.decode("utf-8", errors="replace").rstrip("\n") if result.stdout else ""
            stderr_text = result.stderr.decode("utf-8", errors="replace").rstrip("\n") if result.stderr else ""
        else:
            result = subprocess.run(cmd_parts, capture_output=True, text=True, cwd=run_cwd, env=env)
            stdout_text = result.stdout.rstrip("\n") if result.stdout else ""
            stderr_text = result.stderr.rstrip("\n") if result.stderr else ""

        output_text = "\n".join(chunk for chunk in [stdout_text, stderr_text] if chunk)

        if output_text:
            safe_print(output_text)
        else:
            safe_print("(No output)")

        with log_path.open("w", encoding="utf-8") as log_file:
            log_file.write(f"timestamp: {datetime.now().isoformat()}\n")
            log_file.write(f"command: {command}\n")
            log_file.write(f"cwd: {run_cwd}\n")
            if resolved_script_path is not None:
                log_file.write(f"resolved_script_path: {resolved_script_path}\n")
            if env is not None and "PYTHONIOENCODING" in env:
                log_file.write(f"PYTHONIOENCODING: {env['PYTHONIOENCODING']}\n")
            log_file.write(f"return_code: {result.returncode}\n\n")
            log_file.write("stdout:\n")
            log_file.write(stdout_text if stdout_text else "(No output)")
            log_file.write("\n\nstderr:\n")
            log_file.write(stderr_text if stderr_text else "(No output)")
            log_file.write("\n")

        safe_print(f"\nLog saved: {log_path}")

    except (ValueError, FileNotFoundError) as exc:
        error_msg = f"Error: {exc}"
        safe_print(error_msg)

        with log_path.open("w", encoding="utf-8") as log_file:
            log_file.write(f"timestamp: {datetime.now().isoformat()}\n")
            log_file.write(f"command: {command}\n")
            log_file.write(f"cwd: {run_cwd}\n")
            if resolved_script_path is not None:
                log_file.write(f"resolved_script_path: {resolved_script_path}\n")
            log_file.write("return_code: N/A\n\n")
            log_file.write("output:\n")
            log_file.write(error_msg + "\n")

        safe_print(f"Log saved: {log_path}")


def run_builtin_script(script_path: Path, *args: str) -> None:
    """Run a built-in script from project root with debug path output and existence checks."""
    resolved_script_path = script_path.resolve()
    safe_print(f"Resolved script path: {resolved_script_path}")

    if not resolved_script_path.exists():
        safe_print(f"Error: built-in script not found: {resolved_script_path}")
        return

    if not resolved_script_path.is_file():
        safe_print(f"Error: built-in script path is not a file: {resolved_script_path}")
        return

    cmd_parts = [sys.executable, str(resolved_script_path), *args]
    command = " ".join(shlex.quote(part) for part in cmd_parts)
    safe_print(f"Built-in command: {command}")
    safe_print(f"Built-in cwd: {PROJECT_ROOT}")
    run_and_log(
        command,
        resolved_script_path=resolved_script_path,
        env=build_utf8_env(),
        force_utf8_decode=True,
    )


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
            product_input = input("Enter product details: ").strip()
            if not product_input:
                print("No input provided. Returning to menu.")
                continue
            run_builtin_script(RUN_LISTING_PIPELINE_SCRIPT, product_input)
        elif choice == "2":
            run_builtin_script(INSPECT_RUN_SCRIPT)
        elif choice == "3":
            run_builtin_script(EXPORT_RUN_SCRIPT)
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
