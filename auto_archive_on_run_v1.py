import subprocess


def run(cmd):
    print(f"\nRUNNING: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"ERROR running: {cmd}")
        exit(1)


def main():
    print("AUTO ARCHIVE PIPELINE START\n")

    run("python archive_control_room_run_v1.py")
    run("python history_index_v1.py")
    run("python history_inspector_v1.py")

    print("\nAUTO ARCHIVE PIPELINE DONE")


if __name__ == "__main__":
    main()