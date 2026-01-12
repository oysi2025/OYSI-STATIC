# OYSI Static Website

Statische Unternehmens-Landingpage für die OYSI GmbH (https://oysi.gmbh) mit Kontaktformular-Backend.

## Commands

### Installation & Start

```bash
# Docker-Netzwerk erstellen (falls noch nicht vorhanden)
docker network create oysi-net

# Container starten
docker-compose up -d

# Container mit Rebuild starten
docker-compose up -d --build

# Logs anzeigen
docker-compose logs -f

# Container stoppen
docker-compose down
```

### Lokale Backend-Entwicklung

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Health Check

```bash
curl http://localhost:8090/api/health
```

## Code Style & Architecture

### Sprachen & Frameworks

- **Frontend**: Vanilla HTML/CSS/JavaScript (keine Build-Tools)
- **Backend**: Python 3.11 mit FastAPI + Pydantic
- **Server**: nginx (Alpine) als Reverse Proxy
- **Deployment**: Docker Compose

### Projektstruktur

```
oysi-static/
├── public/              # Statische Dateien (von nginx ausgeliefert)
│   └── index.html       # Single-Page Landingpage (DE/FR)
├── backend/             # FastAPI Kontaktformular-API
│   ├── main.py          # API-Endpunkte (/contact, /health)
│   ├── requirements.txt # Python-Abhängigkeiten
│   └── Dockerfile       # Python 3.11-slim Image
├── nginx.conf           # Reverse Proxy Config (/ -> static, /api/ -> backend)
├── docker-compose.yml   # Service-Orchestrierung
└── .env                 # SMTP-Zugangsdaten (nicht committen!)
```

### Conventions

- **CSS**: CSS Custom Properties (`:root` Variablen) für Farbpalette
- **API**: RESTful mit JSON-Responses, Pydantic-Validierung
- **Kommentare**: Deutsch im Frontend, Deutsch im Backend
- **CORS**: Offen (`*`) - da same-origin via nginx-Proxy

### Wichtige Patterns

- **Sprachumschaltung**: Client-seitig via JavaScript (`setLang()`)
- **Formular**: Fetch API mit async/await, Status-Feedback inline
- **E-Mail-Versand**: SMTP_SSL mit MIMEMultipart (HTML + Text Fallback)

## Context

### Was macht das Projekt?

Eine "In Vorbereitung"-Landingpage für die OYSI GmbH mit:
- Zweisprachige Anzeige (Deutsch/Französisch)
- Kontaktformular das E-Mails an `olivier.hoefer@oysi.gmbh` sendet
- Impressum mit vollständigen Firmendaten (HRB 109351, Saarbrücken)

### Kritische Aspekte

1. **Umgebungsvariablen** (`.env`):
   - `EMAIL_PASSWORD` - SMTP-Passwort (erforderlich für E-Mail-Versand)
   - `SMTP_SERVER` - Default: `smtp.mail.ovh.net`
   - `EMAIL_SENDER` - Default: `info@oysi.tech`
   - `EMAIL_RECIPIENT` - Default: `olivier.hoefer@oysi.gmbh`

2. **Netzwerk**: Container nutzen externes Docker-Netzwerk `oysi-net`

3. **Port-Binding**: nginx auf `127.0.0.1:8090` (nur localhost, typisch hinter Reverse Proxy)

4. **Keine Tests**: Projekt hat keine Test-Suite

### API-Endpunkte

| Methode | Pfad           | Beschreibung              |
|---------|----------------|---------------------------|
| POST    | `/api/contact` | Kontaktformular absenden  |
| GET     | `/api/health`  | Health Check              |

### Kontaktformular-Payload

```json
{
  "email": "absender@example.com",
  "message": "Nachrichtentext"
}
```
