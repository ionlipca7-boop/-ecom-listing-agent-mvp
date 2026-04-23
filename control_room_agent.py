import time, json, pathlib, subprocess, traceback

BASE = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP")
INBOX = BASE / "control_room_inbox.json"
OUTBOX = BASE / "control_room_outbox.json"
ARCHIVE_DIR = BASE / "storage" / "memory" / "archive" / "agent_feedback"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


def ts():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def archive_event(data):
    safe_name = f"agent_event_{int(time.time())}.json"
    write_json(ARCHIVE_DIR / safe_name, data)


def build_result(action, stage, status="OK", extra=None):
    d = {
        "status": status,
        "timestamp": ts(),
        "action": action,
        "stage": stage,
        "agent": "control_room_agent",
        "feedback_protocol": "AGENT_FEEDBACK_ARCHIVE_PROTOCOL_V1"
    }
    if extra:
        d.update(extra)
    return d


def process_action(data):
    action = data.get("action", "NO_ACTION")
    received = build_result(action, "received", extra={"input": data})
    write_json(OUTBOX, received)
    archive_event(received)

    if action == "run_control_room":
        started = build_result(action, "execution_started")
        write_json(OUTBOX, started)
        archive_event(started)

        proc = subprocess.run(["py", "run_control_room.py"], capture_output=True, text=True)
        finished = build_result(action, "execution_finished", extra={
            "returncode": proc.returncode,
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-4000:]
        })
        write_json(OUTBOX, finished)
        archive_event(finished)
        return

    if action == "finalize_and_lock_runtime":
        finished = build_result(action, "execution_finished", extra={
            "result": "runtime_finalization_acknowledged",
            "note": "agent_received_finalize_signal"
        })
        write_json(OUTBOX, finished)
        archive_event(finished)
        return

    finished = build_result(action, "execution_finished", extra={
        "note": "unknown_or_not_yet_mapped_action"
    })
    write_json(OUTBOX, finished)
    archive_event(finished)


def main():
    print("CONTROL_ROOM_AGENT_STARTED")
    print("WATCHING_INBOX=control_room_inbox.json")
    print("FEEDBACK_PROTOCOL=AGENT_FEEDBACK_ARCHIVE_PROTOCOL_V1")
    while True:
        try:
            if INBOX.exists():
                raw = INBOX.read_text(encoding="utf-8")
                data = json.loads(raw)
                INBOX.unlink()
                process_action(data)
        except Exception as e:
            err = build_result("AGENT_RUNTIME", "error", status="ERROR", extra={
                "error": str(e),
                "traceback": traceback.format_exc()[-4000:]
            })
            write_json(OUTBOX, err)
            archive_event(err)
        time.sleep(2)


if __name__ == "__main__":
    main()
