"""OYSI Contact API - Kontaktformular-Backend mit Spam-Schutz."""

import logging
import os
import smtplib
import ssl
import time
from collections import defaultdict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html import escape

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="OYSI Contact API")

# ============ SPAM-SCHUTZ KONFIGURATION ============
MIN_FORM_TIME_MS = 3000        # Mindestens 3 Sekunden zum Ausfüllen
MAX_REQUESTS_PER_IP = 3        # Max Anfragen pro IP
RATE_LIMIT_WINDOW_SEC = 600    # Zeitfenster: 10 Minuten
MAX_IPS_IN_MEMORY = 1000       # Max IPs im Speicher (Memory Leak Prevention)

# In-Memory Rate Limiting (IP -> Liste von Timestamps)
request_log: dict[str, list[float]] = defaultdict(list)

# CORS erlauben
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# SMTP-Konfiguration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.mail.ovh.net")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "info@oysi.tech")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "olivier.hoefer@oysi.gmbh")


class ContactForm(BaseModel):
    """Kontaktformular-Datenmodell mit Spam-Schutz-Feldern."""
    email: EmailStr
    message: str
    website: str = ""      # Honeypot-Feld
    form_time: int = 0     # Zeitstempel (ms seit Epoch)


def cleanup_old_entries() -> None:
    """Entfernt abgelaufene Rate-Limit-Einträge und begrenzt Speichernutzung."""
    now = time.time()

    # Alte Timestamps aus allen IPs entfernen
    empty_ips = []
    for ip, timestamps in request_log.items():
        request_log[ip] = [t for t in timestamps if now - t < RATE_LIMIT_WINDOW_SEC]
        if not request_log[ip]:
            empty_ips.append(ip)

    # Leere IP-Einträge entfernen
    for ip in empty_ips:
        del request_log[ip]

    # Falls immer noch zu viele IPs, älteste entfernen
    if len(request_log) > MAX_IPS_IN_MEMORY:
        # Sortiere nach ältestem Timestamp und entferne die ältesten
        sorted_ips = sorted(
            request_log.keys(),
            key=lambda ip: min(request_log[ip]) if request_log[ip] else 0
        )
        for ip in sorted_ips[:len(request_log) - MAX_IPS_IN_MEMORY]:
            del request_log[ip]


def is_rate_limited(ip: str) -> bool:
    """Prüft ob IP das Rate Limit überschritten hat."""
    cleanup_old_entries()
    return len(request_log[ip]) >= MAX_REQUESTS_PER_IP


def log_request(ip: str) -> None:
    """Loggt einen Request für Rate Limiting."""
    request_log[ip].append(time.time())


def get_client_ip(request: Request) -> str:
    """Ermittelt die Client-IP (auch hinter Proxy)."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@app.post("/contact")
async def send_contact(form: ContactForm, request: Request) -> dict[str, str | bool]:
    """Empfängt Kontaktformular und sendet E-Mail."""
    client_ip = get_client_ip(request)

    # ===== SPAM-SCHUTZ PRÜFUNGEN =====

    # 1. Honeypot-Prüfung: Feld muss leer sein
    if form.website:
        logger.warning("SPAM: Honeypot ausgefüllt von %s: %s", client_ip, form.website)
        return {"success": True, "message": "E-Mail erfolgreich gesendet"}

    # 2. Zeitprüfung: Formular muss mindestens X Sekunden offen gewesen sein
    if form.form_time:
        elapsed_ms = int(time.time() * 1000) - form.form_time
        if elapsed_ms < MIN_FORM_TIME_MS:
            logger.warning("SPAM: Zu schnell ausgefüllt von %s: %dms", client_ip, elapsed_ms)
            return {"success": True, "message": "E-Mail erfolgreich gesendet"}

    # 3. Rate Limiting
    if is_rate_limited(client_ip):
        logger.warning("SPAM: Rate Limit erreicht für %s", client_ip)
        raise HTTPException(status_code=429, detail="Zu viele Anfragen. Bitte später erneut versuchen.")

    log_request(client_ip)

    # HTML-Escape für User-Input (XSS-Schutz)
    safe_email = escape(form.email)
    safe_message = escape(form.message).replace("\n", "<br>")

    subject = f"Kontaktanfrage von {form.email}"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #111827; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #f8f9fa; padding: 30px; border: 1px solid #e5e7eb; }}
        .message-box {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2563eb; }}
        .label {{ color: #6b7280; font-size: 12px; text-transform: uppercase; }}
        .value {{ font-size: 16px; color: #1f2937; }}
        .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin:0;">OYSI GmbH</h1>
            <p style="margin:5px 0 0 0; opacity:0.8;">Neue Kontaktanfrage</p>
        </div>
        <div class="content">
            <h2>Neue Nachricht erhalten</h2>
            <div class="message-box">
                <p><span class="label">Absender:</span><br>
                <span class="value"><a href="mailto:{safe_email}">{safe_email}</a></span></p>
            </div>
            <div class="message-box">
                <p><span class="label">Nachricht:</span><br>
                <span class="value">{safe_message}</span></p>
            </div>
            <p style="color: #6b7280; font-size: 12px;">
                Um zu antworten, klicken Sie auf die E-Mail-Adresse oben oder antworten Sie direkt auf diese E-Mail.
            </p>
        </div>
        <div class="footer">
            <p>Diese E-Mail wurde automatisch von oysi.gmbh gesendet.</p>
        </div>
    </div>
</body>
</html>"""

    text_content = f"""OYSI GmbH - Neue Kontaktanfrage
================================

Absender: {form.email}

Nachricht:
{form.message}

---
Um zu antworten, schreiben Sie an: {form.email}
"""

    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"OYSI Website <{EMAIL_SENDER}>"
        message["To"] = EMAIL_RECIPIENT
        message["Reply-To"] = form.email

        message.attach(MIMEText(text_content, "plain"))
        message.attach(MIMEText(html_content, "html"))

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, message.as_string())

        logger.info("E-Mail gesendet von %s", form.email)
        return {"success": True, "message": "E-Mail erfolgreich gesendet"}

    except Exception as e:
        logger.error("E-Mail-Versand fehlgeschlagen: %s", e)
        raise HTTPException(status_code=500, detail="E-Mail konnte nicht gesendet werden")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health Check Endpoint."""
    return {"status": "ok"}
