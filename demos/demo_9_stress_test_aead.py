#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Demo 9 — AEAD One-Minute Stress Test
------------------------------------
Goal
-----
Run continuous encrypt → decrypt cycles for 60 s to verify stability,
detect errors, and confirm deterministic operation of AEAD engine.

Requirements
------------
- paxect_aead_enterprise.py (v1.1.0)
- cryptography package
"""

import os, subprocess, time, shutil
from pathlib import Path

BASE = Path("/tmp/paxect_demo9")
ENC = BASE / "enc"
DEC = BASE / "dec"
SRC = BASE / "src.txt"
LOG = BASE / "stress_log.jsonl"
PASS = "enterprise-demo-key"

shutil.rmtree(BASE, ignore_errors=True)
BASE.mkdir(parents=True)
ENC.mkdir()
DEC.mkdir()
LOG.write_text("")

def run_encrypt_decrypt(i: int) -> bool:
    """Encrypt → decrypt roundtrip. Return True if success, False if error."""
    src = SRC
    enc = ENC / f"file_{i}.enc"
    dec = DEC / f"file_{i}.out"
    src.write_text(f"cycle={i} paxect aead test\n", encoding="utf-8")

    # Encrypt
    with open(src, "rb") as fin, open(enc, "wb") as fout:
        r1 = subprocess.run(
            ["python3", "paxect_aead_enterprise.py",
             "--mode", "encrypt", "--cipher", "auto", "--pass", PASS],
            stdin=fin, stdout=fout,
            stderr=subprocess.PIPE, text=True)
    if r1.returncode != 0:
        LOG.write_text(LOG.read_text() + f'{{"cycle":{i},"phase":"encrypt","error":"{r1.stderr.strip()}"}}\n')
        return False

    # Decrypt
    with open(enc, "rb") as fin, open(dec, "wb") as fout:
        r2 = subprocess.run(
            ["python3", "paxect_aead_enterprise.py",
             "--mode", "decrypt", "--pass", PASS],
            stdin=fin, stdout=fout,
            stderr=subprocess.PIPE, text=True)
    if r2.returncode != 0:
        LOG.write_text(LOG.read_text() + f'{{"cycle":{i},"phase":"decrypt","error":"{r2.stderr.strip()}"}}\n')
        return False

    # Verify equality
    ok = SRC.read_text() == dec.read_text()
    if not ok:
        LOG.write_text(LOG.read_text() + f'{{"cycle":{i},"phase":"verify","error":"mismatch"}}\n')
    return ok

print("=== Demo 9 — AEAD One-Minute Stress Test ===")
print("[*] Running continuous encrypt→decrypt cycles for 60 seconds...")

start = time.time()
cycles = 0
errors = 0
while time.time() - start < 60:
    cycles += 1
    ok = run_encrypt_decrypt(cycles)
    if not ok:
        errors += 1

print(f"\nCompleted cycles: {cycles}")
print(f"Errors detected : {errors}")
if cycles > 0:
    print(f"Reliability     : {(1 - errors / cycles) * 100:.4f}%")
else:
    print("No cycles executed.")
print(f"\nDetailed log: {LOG}")

if errors == 0:
    print("✅ AEAD engine passed 1-minute stress test without errors.")
else:
    print("⚠️ AEAD engine detected recoverable errors; see log for details.")
