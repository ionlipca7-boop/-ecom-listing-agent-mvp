import subprocess
import sys


def _print_menu():
    print("\n============================")
    print("ECOM LISTING AGENT — CONTROL ROOM")
    print("============================\n")
    print("1. Create new listing")
    print("2. View recent listings")
    print("3. Exit\n")


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


def main():
    while True:
        _print_menu()
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            _run_listing_pipeline()
        elif choice == "2":
            _view_recent_listings()
        elif choice == "3":
            print("Exiting Control Room.")
            break
        else:
            print("Invalid option. Press Enter to try again.")
            input()


if __name__ == "__main__":
    main()
