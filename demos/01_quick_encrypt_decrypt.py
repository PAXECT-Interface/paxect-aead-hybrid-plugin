#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
PAXECT AEAD Enterprise — Demo 01: Quick Encrypt → Decrypt → Verify
v1.0.1
Shows basic usage of paxect_aead_enterprise.py for developers.
Encrypts a small text file, decrypts it, and verifies integrity with SHA-256.
"""

import os
import sys
import time
import hashlib
import tempfile
import subprocess
from datetime import datetime, timezone

PLUGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "paxect_aead_enterprise.py"))
PASSWORD = "demo123"


def sha256(path: str) -> str:
    """Compute SHA-256 hash for a given file path."""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run(cmd, input_path=None, output_path=None):
    """Execute the AEAD plugin with optional input/output files."""
    with open(input_path, "rb") if input_path else subprocess.DEVNULL as fin, \
         open(output_path, "wb") if output_path else subprocess.DEVNULL as fout:
        p = subprocess.run(
            [sys.executable, PLUGIN] + cmd,
            stdin=fin,
            stdout=fout,
            stderr=subprocess.PIPE,
        )
    if p.returncode != 0:
        print(f"[Error] {p.stderr.decode().strip()}")
        sys.exit(2)


def main():
    print("=== PAXECT AEAD Demo 01 — Quick Encrypt/Decrypt ===")
    print(f"Local time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"UTC time   : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # Prepare temporary working directory
    tmpdir = tempfile.mkdtemp(prefix="paxect_demo01_")
    src = os.path.join(tmpdir, "input.txt")
    enc = os.path.join(tmpdir, "output.aead")
    dec = os.path.join(tmpdir, "decrypted.txt")

    # Write sample content
    with open(src, "w", encoding="utf-8") as f:
        f.write("PAXECT AEAD Demo 01 - Quick Encrypt/Decrypt\n")
        f.write("Hybrid AES-GCM + ChaCha20-Poly1305 test\n")
        f.write(f"Generated at: {datetime.now(timezone.utc).isoformat()}\n")

    print(f"[1] Source file  : {src}")

    # Encrypt
    print(f"[2] Encrypting → {enc}")
    run(["--mode", "encrypt", "--cipher", "auto", "--pass", PASSWORD],
        input_path=src, output_path=enc)

    # Decrypt
    print(f"[3] Decrypting → {dec}")
    run(["--mode", "decrypt", "--pass", PASSWORD],
        input_path=enc, output_path=dec)

    # Verify integrity
    h_src = sha256(src)
    h_dec = sha256(dec)
    print(f"[4] SHA-256 src : {h_src}")
    print(f"[5] SHA-256 dec : {h_dec}")

    if h_src == h_dec:
        print("✅  Integrity verified — AEAD stream round-trip successful")
    else:
        print("❌  Mismatch detected!")

    print(f"Temporary files stored in: {tmpdir}")
    print("=== Demo 01 completed successfully ===")


if __name__ == "__main__":
    main()

