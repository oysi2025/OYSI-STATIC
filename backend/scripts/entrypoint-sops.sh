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

# Decrypt and export secrets
echo "[SOPS] Decrypting secrets..."
while IFS= read -r line; do
    # Skip empty lines and comments
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    # Split on first = only (preserves = in values like base64)
    key="${line%%=*}"
    value="${line#*=}"
    export "$key=$value"
done < <(sops -d --output-type dotenv /app/secrets/.env.enc.yaml)

echo "[SOPS] Secrets loaded successfully"

# Execute the main command
exec "$@"
