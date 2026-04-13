import subprocess
import sys
from pathlib import Path


HISTORY_DIR = Path("history")


def _print_menu():
    print("\n============================")
    print("ECOM LISTING AGENT — CONTROL ROOM")
    print("============================\n")
    print("1. Create new listing")
    print("2. View recent listings")
    print("3. Inspect latest run")
    print("4. Inspect run by file path")
    print("5. Export latest run")
    print("6. Export run by file path")
    print("7. Exit\n")


def _run_listing_pipeline():
    product_input = input("Enter product details: ").strip()

    if not product_input:
        print("No input provided. Returning to menu.")
        return

    print("\n--- Running listing pipeline ---")
    result = subprocess.run([sys.executable, "run_listing_pipeline.py", product_input])
    if result.returncode != 0:
        print(f"Pipeline exited with code {result.returncode}.")
    print("--- Pipeline finished ---\n")


def _view_recent_listings():
    print("\n--- Opening listing history ---")
    result = subprocess.run([sys.executable, "view_history.py"])
    if result.returncode != 0:
        print(f"History viewer exited with code {result.returncode}.")
    print("--- History viewer finished ---\n")


def _inspect_latest_run():
    print("\n--- Inspecting latest run ---")
    result = subprocess.run([sys.executable, "inspect_run.py"])
    if result.returncode != 0:
        print(f"Run inspector exited with code {result.returncode}.")
    print("--- Run inspector finished ---\n")


def _inspect_run_by_path():
    print("\n--- Inspecting run by path ---")

    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        print("No history found. The 'history/' folder does not exist yet.")
        print("--- Run inspector finished ---\n")
        return

    run_path = input("Enter run file path (e.g. history/run_YYYYMMDD_HHMMSS.json): ").strip()
    if not run_path:
        print("No file path provided. Returning to menu.")
        print("--- Run inspector finished ---\n")
        return

    result = subprocess.run([sys.executable, "inspect_run.py", run_path])
    if result.returncode != 0:
        print(f"Run inspector exited with code {result.returncode}.")
    print("--- Run inspector finished ---\n")


def _export_latest_run():
    print("\n--- Exporting latest run ---")
    result = subprocess.run([sys.executable, "export_run.py"])
    if result.returncode != 0:
        print(f"Run export exited with code {result.returncode}.")
    print("--- Run export finished ---\n")


def _export_run_by_path():
    print("\n--- Exporting run by path ---")

    run_path = input("Enter run file path (e.g. history/run_YYYYMMDD_HHMMSS.json): ").strip()
    if not run_path:
        print("No file path provided. Returning to menu.")
        print("--- Run export finished ---\n")
        return

    result = subprocess.run([sys.executable, "export_run.py", run_path])
    if result.returncode != 0:
        print(f"Run export exited with code {result.returncode}.")
    print("--- Run export finished ---\n")


def main():
    while True:
        _print_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            _run_listing_pipeline()
        elif choice == "2":
            _view_recent_listings()
        elif choice == "3":
            _inspect_latest_run()
        elif choice == "4":
            _inspect_run_by_path()
        elif choice == "5":
            _export_latest_run()
        elif choice == "6":
            _export_run_by_path()
        elif choice == "7":
            print("Exiting Control Room.")
            break
        else:
            print("Invalid option. Press Enter to try again.")
            input()


if __name__ == "__main__":
    main()
