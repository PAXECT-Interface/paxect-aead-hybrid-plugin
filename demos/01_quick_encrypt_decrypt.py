#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
PAXECT AEAD Enterprise — Demo 01: Quick Encrypt → Decrypt → Verify
v1.0.0
Shows basic usage of paxect_aead_enterprise.py for developers.
Encrypts a small text file, decrypts it, and verifies integrity with SHA-256.
"""

import os, hashlib, subprocess, sys, tempfile, time

SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "paxect_aead_enterprise.py"))
PASSWORD = "demo123"

def sha256(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def run(cmd, input_path=None, output_path=None):
    """Run a shell pipeline with optional input/output files."""
    with open(input_path, "rb") if input_path else subprocess.DEVNULL as fin, \
         open(output_path, "wb") if output_path else subprocess.DEVNULL as fout:
        p = subprocess.run(
            [sys.executable, SCRIPT] + cmd,
            stdin=fin,
            stdout=fout,
            stderr=subprocess.PIPE,
        )
    if p.returncode != 0:
        print(f"[Error] {p.stderr.decode().strip()}")
        sys.exit(2)

def main():
    print("=== PAXECT AEAD Demo 01 — Quick Encrypt/Decrypt ===")

    # Prepare temporary files
    tmpdir = tempfile.mkdtemp(prefix="paxect_demo01_")
    src = os.path.join(tmpdir, "input.txt")
    enc = os.path.join(tmpdir, "output.aead")
    dec = os.path.join(tmpdir, "decrypted.txt")

    # Write sample content
    with open(src, "w", encoding="utf-8") as f:
        f.write("PAXECT AEAD Demo 01\n")
        f.write("Hybrid AES-GCM + ChaCha20-Poly1305 test\n")
        f.write(f"Generated at: {time.ctime()}\n")

    print(f"[1] Source file  : {src}")
    print(f"[2] Encrypting → {enc}")

    run(["--mode", "encrypt", "--cipher", "auto", "--pass", PASSWORD],
        input_path=src, output_path=enc)

    print(f"[3] Decrypting → {dec}")
    run(["--mode", "decrypt", "--pass", PASSWORD],
        input_path=enc, output_path=dec)

    # Verify integrity
    h_src, h_dec = sha256(src), sha256(dec)
    print(f"[4] SHA-256 src : {h_src}")
    print(f"[5] SHA-256 dec : {h_dec}")

    if h_src == h_dec:
        print("✅  Integrity verified — AEAD stream round-trip successful")
    else:
        print("❌  Mismatch detected!")

    print(f"Temporary files stored in: {tmpdir}")

if __name__ == "__main__":
    main()
