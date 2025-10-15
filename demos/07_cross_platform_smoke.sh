#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# PAXECT AEAD Hybrid Plugin — Demo 07: Cross-Platform Smoke Test
# v1.0.0
#
# Verifies deterministic encryption/decryption across OS environments.
# Works on Linux, macOS, Windows (Git Bash / WSL), Android (Termux), and iOS (Pyto).

set -euo pipefail

PLUGIN="./paxect_aead_enterprise.py"
PASS="demo123"
TMPDIR=$(mktemp -d -t paxect_demo07_XXXX)
SRC="$TMPDIR/input.txt"
ENC="$TMPDIR/output.aead"
DEC="$TMPDIR/decrypted.txt"

echo "=== PAXECT AEAD Demo 07 — Cross-Platform Smoke Test ==="
echo "Platform : $(uname -s) $(uname -m)"
echo "Python   : $(python3 --version)"
echo "Temp dir : $TMPDIR"
echo

# 1️⃣ Create test input
echo "[1] Generating input file..."
{
  echo "PAXECT AEAD Demo 07 - Cross-Platform Determinism Test"
  echo "UTC Timestamp : $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "Platform : $(uname -s) $(uname -m)"
} > "$SRC"

# 2️⃣ Encrypt
echo "[2] Encrypting → $ENC"
cat "$SRC" | python3 "$PLUGIN" --mode encrypt --cipher auto --pass "$PASS" > "$ENC"

# 3️⃣ Decrypt
echo "[3] Decrypting → $DEC"
cat "$ENC" | python3 "$PLUGIN" --mode decrypt --pass "$PASS" > "$DEC"

# 4️⃣ Verify hashes
SHA_SRC=$(sha256sum "$SRC" | awk '{print $1}')
SHA_DEC=$(sha256sum "$DEC" | awk '{print $1}')
echo "[4] SHA-256 source : $SHA_SRC"
echo "[4] SHA-256 decrypted : $SHA_DEC"

if [ "$SHA_SRC" = "$SHA_DEC" ]; then
  echo "✅  Deterministic match verified"
else
  echo "❌  Mismatch detected!"
  exit 2
fi

# 5️⃣ Log summary
echo
echo "[5] Environment summary:"
echo "    OS      : $(uname -s)"
echo "    Arch    : $(uname -m)"
echo "    Python  : $(python3 --version | awk '{print $2}')"
echo "    Date    : $(date -u)"
echo
echo "=== Demo 07 completed successfully ==="
