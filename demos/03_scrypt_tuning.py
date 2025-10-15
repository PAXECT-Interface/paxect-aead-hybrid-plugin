#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
PAXECT AEAD Hybrid Plugin — Demo 03: Scrypt Parameter Tuning
v1.0.1
Measures encryption performance using different Scrypt KDF parameters.
"""

import os, subprocess, sys, tempfile, time, hashlib

PLUGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "paxect_aead_enterprise.py"))
PASSWORD = "demo123"

# Create 2 MiB of random test data
DATA = ("PAXECT AEAD Demo 03 - Scrypt tuning test\n").encode("utf-8") + os.urandom(2 * 1024 * 1024)

# Test settings: (N_log2, r, p)
SETTINGS = [
    (14, 8, 1),
    (15, 8, 1),
    (16, 8, 1),
    (14, 16, 2),
]

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def run_encrypt_decrypt(n_log2, r, p):
    """Run one full encrypt/decrypt cycle and measure time."""
    with tempfile.TemporaryDirectory(prefix="paxect_demo03_") as tmp:
        src = os.path.join(tmp, "input.bin")
        enc = os.path.join(tmp, "output.aead")
        dec = os.path.join(tmp, "decrypted.bin")

        with open(src, "wb") as f:
            f.write(DATA)

        # Encrypt
        t0 = time.time()
        subprocess.run(
            [
                sys.executable, PLUGIN,
                "--mode", "encrypt",
                "--cipher", "auto",
                "--pass", PASSWORD,
                "--scrypt-n-log2", str(n_log2),
                "--scrypt-r", str(r),
                "--scrypt-p", str(p),
            ],
            stdin=open(src, "rb"),
            stdout=open(enc, "wb"),
            check=True,
        )
        t_enc = time.time() - t0

        # Decrypt
        t1 = time.time()
        subprocess.run(
            [
                sys.executable, PLUGIN,
                "--mode", "decrypt",
                "--pass", PASSWORD,
            ],
            stdin=open(enc, "rb"),
            stdout=open(dec, "wb"),
            check=True,
        )
        t_dec = time.time() - t1

        # Verify
        h1 = sha256(open(src, "rb").read())
        h2 = sha256(open(dec, "rb").read())
        return (n_log2, r, p, round(t_enc, 3), round(t_dec, 3), h1 == h2)

def main():
    print("=== PAXECT AEAD Demo 03 — Scrypt Parameter Tuning ===\n")
    print(f"{'N_log2':>7} {'r':>3} {'p':>3} | {'Enc(s)':>7} {'Dec(s)':>7} | Result")
    print("-" * 40)
    for n_log2, r, p in SETTINGS:
        n, r_, p_, te, td, ok = run_encrypt_decrypt(n_log2, r, p)
        print(f"{n:7d} {r_:3d} {p_:3d} | {te:7.3f} {td:7.3f} | {'✅ OK' if ok else '❌ FAIL'}")
    print("\n=== Demo 03 completed successfully ===")

if __name__ == "__main__":
    main()
