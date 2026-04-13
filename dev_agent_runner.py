#!/usr/bin/env python3
"""Simple developer helper to run project commands and log outputs."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
import json
from ast import literal_eval
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

LOG_DIR = Path("logs/dev_agent")
PROJECT_ROOT = Path(__file__).resolve().parent
HISTORY_DIR = PROJECT_ROOT / "history"
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
) -> Dict[str, Any]:
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
        return {
            "return_code": result.returncode,
            "stdout_text": stdout_text,
            "stderr_text": stderr_text,
            "log_path": log_path,
        }

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
        return {
            "return_code": None,
            "stdout_text": "",
            "stderr_text": error_msg,
            "log_path": log_path,
        }


def extract_compact_listing_summary(stdout_text: str) -> Optional[Dict[str, str]]:
    """Extract compact pipeline summary fields from run_listing_pipeline output."""
    lines = stdout_text.splitlines()
    listing: Dict[str, Any] = {}
    summary: Dict[str, str] = {}

    for index, line in enumerate(lines):
        if line.strip() == "LISTING RESULT:" and index + 1 < len(lines):
            listing_line = lines[index + 1].strip()
            try:
                parsed_listing = literal_eval(listing_line)
                if isinstance(parsed_listing, dict):
                    listing = parsed_listing
            except (ValueError, SyntaxError):
                pass

        if line.startswith("- "):
            payload = line[2:]
            if ":" not in payload:
                continue
            key, value = payload.split(":", 1)
            summary[key.strip()] = value.strip()

    if not summary:
        return None

    title = str(listing.get("title") or "N/A")
    category = str(listing.get("category") or "N/A")
    price = listing.get("price")
    price_label = f"${price}" if isinstance(price, (int, float)) else str(price or "N/A")

    return {
        "Title": title,
        "Category": category,
        "Price": price_label,
        "Quality Score": summary.get("quality_score", "N/A"),
        "Publish Ready": summary.get("publish_ready", "N/A"),
        "Warnings count": summary.get("warnings_count", "N/A"),
        "Improvements count": summary.get("improvements_count", "N/A"),
        "Publish status": summary.get("publish_status", "N/A"),
        "History path": summary.get("history_path", "N/A"),
    }


def print_operator_summary(summary: Dict[str, str]) -> None:
    """Print compact control-room-style summary after successful pipeline run."""
    safe_print("\n--- MINI CONTROL ROOM SUMMARY ---")
    for label, value in summary.items():
        safe_print(f"{label}: {value}")
    safe_print("Export hint: run option 3 (Export latest run)")
    safe_print("---------------------------------\n")


def _history_sort_key(path: Path) -> datetime:
    """Sort history files using timestamp from filename when available."""
    stem = path.stem
    core = stem[4:] if stem.startswith("run_") else stem
    parts = core.split("_")
    if len(parts) >= 2:
        token = f"{parts[0]}_{parts[1]}"
        try:
            return datetime.strptime(token, "%Y%m%d_%H%M%S")
        except ValueError:
            pass
    return datetime.fromtimestamp(path.stat().st_mtime)


def _latest_history_file(history_dir: Path) -> Optional[Path]:
    files = [path for path in history_dir.glob("run_*.json") if path.is_file()]
    if not files:
        return None
    files.sort(key=_history_sort_key, reverse=True)
    return files[0]


def _collect_ai_summary(listing_result: Any) -> str:
    if not isinstance(listing_result, dict):
        return "N/A"

    ai_candidates: List[str] = []
    for key, value in listing_result.items():
        if "ai" in key.lower() and value is not None:
            ai_candidates.append(f"{key}={value}")

    final_bundle = listing_result.get("final_listing_bundle")
    if isinstance(final_bundle, dict):
        ai_summary = final_bundle.get("ai_summary")
        if ai_summary:
            ai_candidates.append(f"final_listing_bundle.ai_summary={ai_summary}")

    if not ai_candidates:
        return "N/A"

    first = ai_candidates[0]
    return first if len(first) <= 180 else f"{first[:177]}..."


def extract_compact_inspect_summary() -> Optional[Dict[str, str]]:
    """Extract compact inspect summary fields from latest history record."""
    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        return None

    run_path = _latest_history_file(HISTORY_DIR)
    if run_path is None:
        return None

    try:
        with run_path.open("r", encoding="utf-8") as history_file:
            record = json.load(history_file)
    except (OSError, json.JSONDecodeError):
        return None

    listing_result = record.get("listing_result") if isinstance(record, dict) else None
    pipeline_summary = record.get("pipeline_summary") if isinstance(record, dict) else None
    publish_result = record.get("publish_result") if isinstance(record, dict) else None

    title = "N/A"
    category = "N/A"
    price_value: Any = "N/A"
    if isinstance(listing_result, dict):
        title = str(listing_result.get("title") or "N/A")
        category = str(listing_result.get("category") or "N/A")
        price_value = listing_result.get("price", "N/A")

    price_label = f"${price_value}" if isinstance(price_value, (int, float)) else str(price_value)
    quality_score = "N/A"
    publish_ready = "N/A"
    warnings_count = "N/A"
    improvements_count = "N/A"
    if isinstance(pipeline_summary, dict):
        quality_score = str(pipeline_summary.get("quality_score", "N/A"))
        publish_ready = str(pipeline_summary.get("publish_ready", "N/A"))
        warnings_count = str(pipeline_summary.get("warnings_count", "N/A"))
        improvements_count = str(pipeline_summary.get("improvements_count", "N/A"))

    publish_status = "N/A"
    if isinstance(publish_result, dict):
        publish_status = str(publish_result.get("status", "N/A"))

    timestamp = str(record.get("timestamp") or run_path.stem) if isinstance(record, dict) else run_path.stem
    history_ref = str(run_path)

    return {
        "Title": title,
        "Category": category,
        "Price": price_label,
        "Quality Score": quality_score,
        "Publish Ready": publish_ready,
        "Publish Status": publish_status,
        "Timestamp": timestamp,
        "History / run file": history_ref,
        "AI Summary": _collect_ai_summary(listing_result),
        "Warnings count": warnings_count,
        "Improvements count": improvements_count,
    }


def print_inspect_review_block(summary: Dict[str, str]) -> None:
    """Print compact operator review block after inspect output."""
    safe_print("\n--- COMPACT INSPECT REVIEW ---")
    for label, value in summary.items():
        safe_print(f"{label}: {value}")
    safe_print("------------------------------\n")


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
    run_result = run_and_log(
        command,
        resolved_script_path=resolved_script_path,
        env=build_utf8_env(),
        force_utf8_decode=True,
    )
    if (
        resolved_script_path == RUN_LISTING_PIPELINE_SCRIPT.resolve()
        and run_result.get("return_code") == 0
    ):
        compact_summary = extract_compact_listing_summary(run_result.get("stdout_text", ""))
        if compact_summary is not None:
            print_operator_summary(compact_summary)
    if (
        resolved_script_path == INSPECT_RUN_SCRIPT.resolve()
        and run_result.get("return_code") == 0
    ):
        inspect_summary = extract_compact_inspect_summary()
        if inspect_summary is not None:
            print_inspect_review_block(inspect_summary)


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
