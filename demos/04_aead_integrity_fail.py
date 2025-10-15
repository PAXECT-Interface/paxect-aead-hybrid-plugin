#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
PAXECT AEAD Hybrid Plugin — Demo 04: AEAD Integrity Fail Test
v1.0.1
Demonstrates that any bit corruption in ciphertext causes authenticated decryption failure.
"""

import os
import subprocess
import sys
import tempfile
import hashlib

PLUGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "paxect_aead_enterprise.py"))
PASSWORD = "demo123"


def sha256(path: str) -> str:
    """Return SHA-256 hash of a file."""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    print("=== PAXECT AEAD Demo 04 — Integrity Fail Test ===")

    tmp = tempfile.mkdtemp(prefix="paxect_demo04_")
    src = os.path.join(tmp, "input.txt")
    enc = os.path.join(tmp, "output.aead")
    cor = os.path.join(tmp, "corrupted.aead")
    dec = os.path.join(tmp, "decrypted.txt")

    # 1️⃣ Create test file
    with open(src, "w", encoding="utf-8") as f:
        f.write("PAXECT AEAD Demo 04 - Integrity check\n")

    print(f"[1] Source file : {src}")

    # 2️⃣ Encrypt
    print(f"[2] Encrypting → {enc}")
    with open(src, "rb") as fin, open(enc, "wb") as fout:
        subprocess.run(
            [sys.executable, PLUGIN, "--mode", "encrypt", "--cipher", "auto", "--pass", PASSWORD],
            stdin=fin,
            stdout=fout,
            check=True,
        )

    # 3️⃣ Corrupt ciphertext (flip one byte)
    print(f"[3] Corrupting ciphertext → {cor}")
    data = bytearray(open(enc, "rb").read())
    if len(data) > 100:
        data[100] ^= 0xFF  # flip one byte at position 100
    else:
        data[-1] ^= 0x01   # flip last byte if shorter
    with open(cor, "wb") as f:
        f.write(data)

    # 4️⃣ Attempt to decrypt (expected to fail)
    print(f"[4] Attempting decryption of corrupted file → should fail")
    try:
        with open(cor, "rb") as fin, open(dec, "wb") as fout:
            subprocess.run(
                [sys.executable, PLUGIN, "--mode", "decrypt", "--pass", PASSWORD],
                stdin=fin,
                stdout=fout,
                check=True,
            )
        print("❌  ERROR: decryption succeeded unexpectedly!")
    except subprocess.CalledProcessError as e:
        print("✅  Integrity check triggered — decryption failed safely.")
        err = e.stderr.decode().strip() if e.stderr else "(no stderr output)"
        print(f"AEAD reported error:\n{err}")

    print(f"\nTemporary files stored in: {tmp}")
    print("=== Demo 04 completed ===")


if __name__ == "__main__":
    main()
