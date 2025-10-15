#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
PAXECT AEAD Hybrid Plugin — Demo 03: Scrypt Parameter Tuning
v1.0.2
Benchmarks different Scrypt (N, r, p) configurations to balance
security strength vs. performance for the key-derivation phase.
"""

import os
import sys
import time
import json
import tempfile
import subprocess
from datetime import datetime, timezone

PLUGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "paxect_aead_enterprise.py"))
PASSWORD = "demo123"

# Scrypt parameter sets to benchmark
PARAM_SETS = [
    (14, 8, 1),
    (15, 8, 1),
    (16, 8, 1),
    (14, 16, 2),
]


def run_encrypt_decrypt(n_log2, r, p):
    """Encrypt and decrypt using given Scrypt parameters; return (enc_time, dec_time, ok)."""
    tmp = tempfile.mkdtemp(prefix="paxect_demo03_")
    src = os.path.join(tmp, "input.bin")
    enc = os.path.join(tmp, "output.aead")
    dec = os.path.join(tmp, "decrypted.bin")

    # Create 2 MiB of random test data
    with open(src, "wb") as f:
        f.write(b"PAXECT AEAD Demo 03 - Scrypt tuning test\n")
        f.write(os.urandom(2 * 1024 * 1024))

    # Encrypt
    t0 = time.perf_counter()
    with open(src, "rb") as fin, open(enc, "wb") as fout:
        subprocess.run(
            [
                sys.executable, PLUGIN,
                "--mode", "encrypt", "--cipher", "auto",
                "--pass", PASSWORD,
                "--scrypt-n-log2", str(n_log2),
                "--scrypt-r", str(r),
                "--scrypt-p", str(p),
            ],
            stdin=fin, stdout=fout, check=True, stderr=subprocess.DEVNULL,
        )
    t1 = time.perf_counter()

    # Decrypt
    with open(enc, "rb") as fin, open(dec, "wb") as fout:
        subprocess.run(
            [sys.executable, PLUGIN, "--mode", "decrypt", "--pass", PASSWORD],
            stdin=fin, stdout=fout, check=True, stderr=subprocess.DEVNULL,
        )
    t2 = time.perf_counter()

    # Compare plaintexts
    ok = open(src, "rb").read() == open(dec, "rb").read()
    return round(t1 - t0, 3), round(t2 - t1, 3), ok


def main():
    print("=== PAXECT AEAD Demo 03 — Scrypt Parameter Tuning ===")
    print(f"Local time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"UTC time   : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("\n N_log2   r   p |  Enc(s)  Dec(s) | Result")
    print("----------------------------------------")

    results = []
    for n_log2, r, p in PARAM_SETS:
        try:
            enc_t, dec_t, ok = run_encrypt_decrypt(n_log2, r, p)
            status = "✅ OK" if ok else "❌ FAIL"
            print(f"{n_log2:7d} {r:3d} {p:3d} | {enc_t:7.3f} {dec_t:7.3f} | {status}")
            results.append({
                "N_log2": n_log2, "r": r, "p": p,
                "enc_time": enc_t, "dec_time": dec_t, "ok": ok,
            })
        except Exception as e:
            print(f"{n_log2:7d} {r:3d} {p:3d} |   error   | {e}")
            results.append({"N_log2": n_log2, "r": r, "p": p, "error": str(e)})

    # Save benchmark results
    log_path = os.path.join(tempfile.gettempdir(), "paxect_demo03_results.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {log_path}")
    print("=== Demo 03 completed successfully ===")


if __name__ == "__main__":
    main()

