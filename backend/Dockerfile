FROM python:3.11-slim

WORKDIR /app

# Install wget for SOPS download
RUN apt-get update && apt-get install -y --no-install-recommends wget \
    && wget -qO /usr/local/bin/sops https://github.com/getsops/sops/releases/download/v3.9.4/sops-v3.9.4.linux.amd64 \
    && chmod +x /usr/local/bin/sops \
    && apt-get purge -y wget && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Copy SOPS entrypoint script
RUN mkdir -p /app/scripts
COPY --chmod=755 scripts/entrypoint-sops.sh /app/scripts/

# Health check using Python (no curl needed)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# SOPS entrypoint decrypts secrets, then runs CMD
ENTRYPOINT ["/app/scripts/entrypoint-sops.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
