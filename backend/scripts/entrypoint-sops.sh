#!/bin/bash
# SOPS Entrypoint for OYSI Static Backend
# Decrypts secrets at runtime and exports as environment variables

set -euo pipefail

# Check for required files
if [ ! -f "/run/secrets/sops-key" ]; then
    echo "[SOPS] ERROR: age key not found at /run/secrets/sops-key" >&2
    exit 1
fi

if [ ! -f "/app/secrets/.env.enc.yaml" ]; then
    echo "[SOPS] ERROR: Encrypted secrets not found at /app/secrets/.env.enc.yaml" >&2
    exit 1
fi

# Set SOPS key file
export SOPS_AGE_KEY_FILE="/run/secrets/sops-key"

# Decrypt into a variable first so sops exits cleanly before exec replaces this shell.
# Process substitution < <(sops ...) leaves sops as a zombie because exec never waits on it.
echo "[SOPS] Decrypting secrets..."
SOPS_OUTPUT="$(sops -d --output-type dotenv /app/secrets/.env.enc.yaml)"

while IFS= read -r line; do
    # Skip empty lines and comments
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    # Split on first = only (preserves = in values like base64)
    key="${line%%=*}"
    value="${line#*=}"
    export "$key=$value"
done <<< "$SOPS_OUTPUT"
unset SOPS_OUTPUT

echo "[SOPS] Secrets loaded successfully"

# Execute the main command
exec "$@"
