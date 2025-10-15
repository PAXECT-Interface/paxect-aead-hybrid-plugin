#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
PAXECT AEAD Hybrid Plugin — Demo 05: Enterprise Integration
v1.0.2
Demonstrates end-to-end AEAD encryption/decryption with timing,
integrity verification, and structured JSONL logging for enterprise use.
"""

import os
import sys
import time
import json
import tempfile
import hashlib
import subprocess
from datetime import datetime, timezone

PLUGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "paxect_aead_enterprise.py"))
PASSWORD = "demo123"
LOG_PATH = os.path.join(tempfile.gettempdir(), "paxect_aead_demo05_log.jsonl")


def sha256(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def log_event(event: dict):
    """Append JSONL event to the enterprise log."""
    event["datetime_utc"] = datetime.now(timezone.utc).isoformat()
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def run_stage(label: str, cmd: list, src: str, dst: str):
    """Run plugin command and record timing + result."""
    t0 = time.perf_counter()
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        subprocess.run([sys.executable, PLUGIN] + cmd, stdin=fin, stdout=fout, check=True)
    elapsed = round(time.perf_counter() - t0, 3)
    log_event({"stage": label, "elapsed_sec": elapsed, "src": src, "dst": dst})
    print(f"[{label}] ✅ completed in {elapsed:.3f}s")
    return elapsed


def main():
    print("=== PAXECT AEAD Demo 05 — Enterprise Integration ===")
    print(f"Local time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"UTC time   : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")

    tmpdir = tempfile.mkdtemp(prefix="paxect_demo05_")
    src = os.path.join(tmpdir, "input.txt")
    enc = os.path.join(tmpdir, "output.aead")
    dec = os.path.join(tmpdir, "decrypted.txt")

    # Create source file
    with open(src, "w", encoding="utf-8") as f:
        f.write("PAXECT AEAD Demo 05 - Enterprise integration test\n")
        f.write(f"Timestamp (UTC): {datetime.now(timezone.utc).isoformat()}\n")

    print(f"[1] Source file  : {src}")

    try:
        # Encrypt and decrypt
        t_enc = run_stage("encrypt", ["--mode", "encrypt", "--cipher", "auto", "--pass", PASSWORD], src, enc)
        t_dec = run_stage("decrypt", ["--mode", "decrypt", "--pass", PASSWORD], enc, dec)

        # Verify SHA-256 integrity
        sha_src, sha_dec = sha256(src), sha256(dec)
        print(f"[4] SHA-256 match: {'MATCH' if sha_src == sha_dec else 'MISMATCH'}")

        # Log final status
        log_event({
            "stage": "verify",
            "sha_src": sha_src,
            "sha_dec": sha_dec,
            "match": sha_src == sha_dec,
            "encrypt_time": t_enc,
            "decrypt_time": t_dec,
        })

        total = round(t_enc + t_dec, 3)
        if sha_src == sha_dec:
            print(f"✅  All steps finished successfully in {total:.2f}s")
        else:
            print("❌  Integrity mismatch detected!")

    except subprocess.CalledProcessError as e:
        print(f"❌  AEAD error: {e}")
        log_event({"stage": "error", "message": str(e), "returncode": e.returncode})
        sys.exit(2)

    print(f"Temporary directory: {tmpdir}")
    print(f"Log file: {LOG_PATH}")
    print("=== Demo 05 completed successfully ===")


if __name__ == "__main__":
    main()

