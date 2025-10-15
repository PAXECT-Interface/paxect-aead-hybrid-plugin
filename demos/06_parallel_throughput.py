#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
PAXECT AEAD Hybrid Plugin — Demo 06: Parallel Throughput Benchmark
v1.0.0
Measures encryption throughput for AES-GCM and ChaCha20-Poly1305 in parallel jobs.
"""

import os
import sys
import time
import hashlib
import tempfile
import subprocess
import concurrent.futures
from datetime import datetime, timezone

PLUGIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "paxect_aead_enterprise.py"))
PASSWORD = "demo123"
PARALLEL_JOBS = 4
DATA_SIZE_MB = 8  # per job


def make_random_file(path: str, size_mb: int):
    with open(path, "wb") as f:
        f.write(os.urandom(size_mb * 1024 * 1024))


def sha256(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run_cycle(cipher: str, job_id: int):
    """Encrypt and decrypt one file and measure total time."""
    tmp = tempfile.mkdtemp(prefix=f"paxect_demo06_{cipher}_{job_id}_")
    src = os.path.join(tmp, "input.bin")
    enc = os.path.join(tmp, "output.aead")
    dec = os.path.join(tmp, "decrypted.bin")

    make_random_file(src, DATA_SIZE_MB)
    t0 = time.time()

    subprocess.run(
        [sys.executable, PLUGIN, "--mode", "encrypt", "--cipher", cipher, "--pass", PASSWORD],
        stdin=open(src, "rb"),
        stdout=open(enc, "wb"),
        check=True,
    )

    subprocess.run(
        [sys.executable, PLUGIN, "--mode", "decrypt", "--pass", PASSWORD],
        stdin=open(enc, "rb"),
        stdout=open(dec, "wb"),
        check=True,
    )

    elapsed = time.time() - t0
    match = sha256(src) == sha256(dec)
    return (cipher, job_id, elapsed, match)


def run_benchmark(cipher: str):
    print(f"\n=== Benchmark: {cipher.upper()} ({PARALLEL_JOBS} parallel jobs × {DATA_SIZE_MB} MB each) ===")
    t_start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=PARALLEL_JOBS) as ex:
        futures = [ex.submit(run_cycle, cipher, i) for i in range(PARALLEL_JOBS)]
        results = [f.result() for f in futures]

    t_total = time.time() - t_start
    total_bytes = PARALLEL_JOBS * DATA_SIZE_MB * 1024 * 1024
    throughput = total_bytes / t_total / (1024 * 1024)

    ok = all(r[3] for r in results)
    print(f"All integrity checks: {'✅ OK' if ok else '❌ FAIL'}")
    print(f"Total elapsed: {t_total:.3f}s — aggregate throughput: {throughput:.1f} MB/s\n")
    return (cipher, t_total, throughput, ok)


def main():
    print("=== PAXECT AEAD Demo 06 — Parallel Throughput Benchmark ===")
    print(f"Local time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"UTC time   : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")

    results = []
    for cipher in ["aes", "chacha", "auto"]:
        results.append(run_benchmark(cipher))

    print("=== Summary ===")
    print(f"{'Cipher':<8} {'Time(s)':>8} {'Throughput(MB/s)':>20} {'Status':>10}")
    print("-" * 50)
    for c, t, thr, ok in results:
        print(f"{c:<8} {t:8.2f} {thr:20.1f} {'✅' if ok else '❌'}")
    print("\n=== Demo 06 completed successfully ===")


if __name__ == "__main__":
    main()
