import os
import smtplib
import ssl
import time
from collections import defaultdict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI(title="OYSI Contact API")

# ============ SPAM-SCHUTZ KONFIGURATION ============
MIN_FORM_TIME_MS = 3000        # Mindestens 3 Sekunden zum Ausfüllen
MAX_REQUESTS_PER_IP = 3        # Max Anfragen pro IP
RATE_LIMIT_WINDOW_SEC = 600    # Zeitfenster: 10 Minuten

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
    email: EmailStr
    message: str
    website: Optional[str] = ""   # Honeypot-Feld
    form_time: Optional[int] = 0  # Zeitstempel (ms seit Epoch)


def is_rate_limited(ip: str) -> bool:
    """Prüft ob IP das Rate Limit überschritten hat."""
    now = time.time()
    # Alte Einträge entfernen
    request_log[ip] = [t for t in request_log[ip] if now - t < RATE_LIMIT_WINDOW_SEC]
    return len(request_log[ip]) >= MAX_REQUESTS_PER_IP


def log_request(ip: str):
    """Loggt einen Request für Rate Limiting."""
    request_log[ip].append(time.time())


@app.post("/contact")
async def send_contact(form: ContactForm, request: Request):
    """Empfängt Kontaktformular und sendet E-Mail."""

    # Client-IP ermitteln (hinter Proxy)
    client_ip = request.headers.get("X-Forwarded-For", request.client.host)
    if client_ip:
        client_ip = client_ip.split(",")[0].strip()

    # ===== SPAM-SCHUTZ PRÜFUNGEN =====

    # 1. Honeypot-Prüfung: Feld muss leer sein
    if form.website:
        print(f"[SPAM] Honeypot ausgefüllt von {client_ip}: {form.website}")
        # Fake-Erfolg zurückgeben (Bot denkt es hat funktioniert)
        return {"success": True, "message": "E-Mail erfolgreich gesendet"}

    # 2. Zeitprüfung: Formular muss mindestens X Sekunden offen gewesen sein
    if form.form_time:
        elapsed_ms = int(time.time() * 1000) - form.form_time
        if elapsed_ms < MIN_FORM_TIME_MS:
            print(f"[SPAM] Zu schnell ausgefüllt von {client_ip}: {elapsed_ms}ms")
            return {"success": True, "message": "E-Mail erfolgreich gesendet"}

    # 3. Rate Limiting
    if is_rate_limited(client_ip):
        print(f"[SPAM] Rate Limit erreicht für {client_ip}")
        raise HTTPException(status_code=429, detail="Zu viele Anfragen. Bitte später erneut versuchen.")

    # Request loggen
    log_request(client_ip)

    subject = f"Kontaktanfrage von {form.email}"

    html_content = f"""
    <!DOCTYPE html>
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
                    <span class="value"><a href="mailto:{form.email}">{form.email}</a></span></p>
                </div>

                <div class="message-box">
                    <p><span class="label">Nachricht:</span><br>
                    <span class="value">{form.message}</span></p>
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
    </html>
    """

    text_content = f"""
    OYSI GmbH - Neue Kontaktanfrage
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

        return {"success": True, "message": "E-Mail erfolgreich gesendet"}

    except Exception as e:
        print(f"E-Mail-Versand fehlgeschlagen: {e}")
        raise HTTPException(status_code=500, detail="E-Mail konnte nicht gesendet werden")


@app.get("/health")
async def health():
    return {"status": "ok"}
