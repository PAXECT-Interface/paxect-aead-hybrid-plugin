#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
PAXECT AEAD Hybrid Plugin — Demo 05: Enterprise Integration
v1.0.0
Full end-to-end encryption/decryption workflow with logging and fail-safe guard.
"""

import os
import sys
import time
import json
import hashlib
import tempfile
import subprocess
from datetime import datetime, timezone, timedelta

PLUGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "paxect_aead_enterprise.py"))
PASSWORD = "demo123"
LOGFILE = os.path.join(tempfile.gettempdir(), "paxect_aead_demo05_log.jsonl")

FAILSAFE_LIMIT_SEC = 300  # 5-minute guard


def sha256(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def log_event(event_type: str, details: dict):
    """Append structured event to JSONL log."""
    entry = {
        "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "event": event_type,
        **details,
    }
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def run_step(step_name: str, cmd: list, input_path: str, output_path: str):
    """Run a subprocess step and log timing."""
    t0 = time.time()
    try:
        with open(input_path, "rb") as fin, open(output_path, "wb") as fout:
            subprocess.run([sys.executable, PLUGIN] + cmd, stdin=fin, stdout=fout, check=True)
        elapsed = round(time.time() - t0, 3)
        log_event(step_name, {"status": "ok", "duration_sec": elapsed})
        print(f"[{step_name}] ✅ completed in {elapsed}s")
    except subprocess.CalledProcessError as e:
        elapsed = round(time.time() - t0, 3)
        log_event(step_name, {"status": "error", "duration_sec": elapsed, "stderr": e.stderr.decode() if e.stderr else ""})
        print(f"[{step_name}] ❌ failed ({elapsed}s)")
        sys.exit(2)


def main():
    print("=== PAXECT AEAD Demo 05 — Enterprise Integration ===")
    log_event("start", {"plugin": PLUGIN})

    start_time = time.time()
    tmpdir = tempfile.mkdtemp(prefix="paxect_demo05_")
    src = os.path.join(tmpdir, "input.txt")
    enc = os.path.join(tmpdir, "output.aead")
    dec = os.path.join(tmpdir, "decrypted.txt")

    # 1️⃣ Create source file
    with open(src, "w", encoding="utf-8") as f:
        f.write("PAXECT AEAD Demo 05 — Enterprise integration pipeline\n")
        f.write(f"Timestamp: {datetime.utcnow().isoformat()}Z\n")
    print(f"[1] Source file  : {src}")

    # 2️⃣ Encrypt
    run_step("encrypt", ["--mode", "encrypt", "--cipher", "auto", "--pass", PASSWORD], src, enc)

    # 3️⃣ Decrypt
    run_step("decrypt", ["--mode", "decrypt", "--pass", PASSWORD], enc, dec)

    # 4️⃣ Verify integrity
    h_src = sha256(src)
    h_dec = sha256(dec)
    result = "match" if h_src == h_dec else "mismatch"
    log_event("verify", {"source_hash": h_src, "decrypted_hash": h_dec, "result": result})
    print(f"[4] SHA-256 match: {result.upper()}")

    # 5️⃣ Fail-safe guard
    elapsed_total = round(time.time() - start_time, 2)
    if elapsed_total > FAILSAFE_LIMIT_SEC:
        log_event("failsafe", {"status": "timeout", "elapsed_total": elapsed_total})
        print("❌  Fail-safe triggered: process exceeded time limit.")
        sys.exit(3)

    log_event("complete", {"elapsed_total": elapsed_total})
    print(f"✅  All steps finished successfully in {elapsed_total}s")
    print(f"Temporary directory: {tmpdir}")
    print(f"Log file: {LOGFILE}")
    print("=== Demo 05 completed ===")


if __name__ == "__main__":
    main()
