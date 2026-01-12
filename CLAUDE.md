# OYSI Static Website

Statische Unternehmens-Landingpage für die OYSI GmbH (https://oysi.gmbh) mit Kontaktformular-Backend.

**Repository**: https://github.com/oysi2025/OYSI-STATIC

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

### Git / Deployment

```bash
# Änderungen committen und pushen
git add .
git commit -m "Beschreibung der Änderung"
git push

# Auf Server deployen (nach Push)
docker-compose up -d --build
```

### Spam-Logs prüfen

```bash
docker-compose logs -f backend | grep SPAM
```

## Code Style & Architecture

### Sprachen & Frameworks

- **Frontend**: Vanilla HTML/CSS/JavaScript (keine Build-Tools)
- **Backend**: Python 3.11 mit FastAPI + Pydantic
- **Server**: nginx (Alpine) als Reverse Proxy
- **Deployment**: Docker Compose
- **Versionskontrolle**: Git + GitHub

### Projektstruktur

```
oysi-static/
├── public/              # Statische Dateien (von nginx ausgeliefert)
│   └── index.html       # Single-Page Landingpage (DE/FR)
├── backend/             # FastAPI Kontaktformular-API
│   ├── main.py          # API-Endpunkte (/contact, /health) + Spam-Schutz
│   ├── requirements.txt # Python-Abhängigkeiten
│   └── Dockerfile       # Python 3.11-slim Image
├── nginx.conf           # Reverse Proxy Config (/ -> static, /api/ -> backend)
├── docker-compose.yml   # Service-Orchestrierung
├── .env                 # SMTP-Zugangsdaten (NICHT in Git!)
├── .gitignore           # Ignoriert .env und andere sensible Dateien
└── CLAUDE.md            # Diese Dokumentation
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

## Spam-Schutz

Das Kontaktformular ist gegen Bots geschützt durch drei Mechanismen:

### 1. Honeypot-Feld
- Verstecktes Feld `website` im Formular
- Für Menschen unsichtbar (CSS), Bots füllen es aus
- Bei Ausfüllung: Fake-Erfolg zurückgeben (Bot merkt nichts)

### 2. Zeitprüfung
- Zeitstempel wird bei Seitenaufruf gesetzt
- Formular muss mindestens **3 Sekunden** offen sein
- Bots die sofort absenden werden erkannt

### 3. Rate Limiting
- Max. **3 Anfragen pro IP** in **10 Minuten**
- Bei Überschreitung: HTTP 429 Fehler
- In-Memory Speicherung (Reset bei Container-Neustart)

### Konfiguration (backend/main.py)

```python
MIN_FORM_TIME_MS = 3000        # Mindestzeit in ms (3 Sek)
MAX_REQUESTS_PER_IP = 3        # Max Anfragen pro IP
RATE_LIMIT_WINDOW_SEC = 600    # Zeitfenster in Sekunden (10 Min)
```

## Context

### Was macht das Projekt?

Eine "In Vorbereitung"-Landingpage für die OYSI GmbH mit:
- Zweisprachige Anzeige (Deutsch/Französisch)
- Kontaktformular das E-Mails an `olivier.hoefer@oysi.gmbh` sendet
- Spam-Schutz (Honeypot, Zeitprüfung, Rate Limiting)
- Impressum mit vollständigen Firmendaten (HRB 109351, Saarbrücken)

### Kritische Aspekte

1. **Umgebungsvariablen** (`.env` - nicht in Git!):
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
  "message": "Nachrichtentext",
  "website": "",
  "form_time": 1704067200000
}
```

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `email` | string | E-Mail-Adresse des Absenders (validiert) |
| `message` | string | Nachrichtentext |
| `website` | string | Honeypot-Feld (muss leer sein) |
| `form_time` | int | Zeitstempel in ms beim Laden der Seite |
