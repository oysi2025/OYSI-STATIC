# OYSI Static Website

Corporate Landingpage für die OYSI GmbH (https://oysi.gmbh) mit Kontaktformular-Backend.

**Repository**: https://github.com/oysi2025/OYSI-STATIC

## Quick Info

| Aspekt | Details |
|--------|---------|
| **URL** | https://oysi.gmbh |
| **Sprachen** | DE, FR, EN (Client-seitig umschaltbar) |
| **Passwort-Schutz** | `oysi2026` (Preview-Modus) |
| **CDN** | https://cdn.oysi.tech (Logos, Favicons, OG-Images) |
| **Reverse Proxy** | Traefik (kein direkter Port-Zugriff) |

## WICHTIG: Wettbewerbsverbot

**Keine Inhalte zu Pool- & Wasserpflege oder Brennstoffen!**

Der Geschäftsführer hat ein Wettbewerbsverbot. Folgende Themen dürfen NICHT auf der Website erscheinen:
- Pool-Chemie / Pool & Wellness
- Wasserpflege / Wasseraufbereitung
- Brennstoffe / Fuels

Stattdessen fokussieren wir auf: **Industrie & Labor**

## Commands

```bash
# Container starten/rebuilden
docker compose up -d --build

# Logs anzeigen
docker compose logs -f

# Container stoppen
docker compose down

# Health Check (nur intern via Traefik)
docker exec oysi_static wget -q --spider http://127.0.0.1/
```

## Projektstruktur

```
oysi-static/
├── public/
│   ├── index.html       # Deutsche Version (Master)
│   ├── fr/index.html    # Französische Version (generiert)
│   ├── en/index.html    # Englische Version (generiert)
│   ├── sitemap.xml      # Sitemap mit hreflang
│   └── robots.txt
├── backend/
│   ├── main.py          # FastAPI Kontaktformular-API
│   ├── requirements.txt
│   └── Dockerfile
├── nginx.conf           # Reverse Proxy mit Sprachrouting
├── docker-compose.yml   # Service-Orchestrierung (Traefik Labels)
├── build-i18n.sh        # ⚠️ Nach Änderungen an index.html ausführen!
├── .env                 # SMTP-Zugangsdaten (NICHT in Git!)
└── CLAUDE.md
```

### Sprachversionen (SEO-optimiert)

| URL | Datei | Canonical |
|-----|-------|-----------|
| `oysi.gmbh/` | `public/index.html` | `oysi.gmbh/` |
| `oysi.gmbh/fr/` | `public/fr/index.html` | `oysi.gmbh/fr/` |
| `oysi.gmbh/en/` | `public/en/index.html` | `oysi.gmbh/en/` |

**WICHTIG:** Nach Änderungen an `index.html`:
```bash
./build-i18n.sh && docker compose restart site-vitrine
```

## Design System (Stand: Januar 2026)

### Farbpalette (Navy Blue + Industrial Theme)

```css
:root {
    /* Backgrounds */
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-card: rgba(30, 41, 59, 0.7);

    /* Accent - Professional Blue */
    --accent-primary: #3b82f6;
    --accent-secondary: #60a5fa;

    /* Industrial/Chemical accent colors */
    --chemical-yellow: #fbbf24;
    --chemical-orange: #f97316;
    --industrial-steel: #64748b;
    --safety-green: #22c55e;

    /* Text */
    --text-primary: #ffffff;
    --text-secondary: #e2e8f0;
    --text-muted: #94a3b8;
}
```

### Hero Background (Hexagonales Molekül-Muster)

Der Hero-Bereich verwendet ein hexagonales Molekül-Muster statt einfacher Dots:

```css
.hex-grid {
    background-image: url("data:image/svg+xml,..."); /* Hexagon SVG Pattern */
    opacity: 0.8;
    animation: float 30s ease-in-out infinite;
}
```

### SVG Icons (Chemie-Industrie-Stil)

**Service Icons** (`.service-icon svg`):
| Service | Icon | Beschreibung |
|---------|------|--------------|
| Chemikalienhandel | Erlenmeyer Flask | Klassisches Labor-Symbol |
| Compliance | GHS Diamond | Gefahrstoff-Raute mit Ausrufezeichen |
| DPP | QR Code | Digitaler Produktpass |
| Lexikon | Benzene Ring | Molekül-Hexagon mit Atomen |

**Industry Icons** (`.industry-icon svg`):
| Branche | Icon | Beschreibung |
|---------|------|--------------|
| Industrie | Barrel/Drum | Chemikalienfass |
| Labor | Test Tubes | Reagenzgläser im Rack |
| Reinigung | Spray Bottle | Sprühflasche |
| Handwerk | Gear | Zahnrad/Settings |

```css
.service-icon svg, .industry-icon svg {
    stroke: var(--accent-primary);
    stroke-width: 1.5;
    fill: none;
}
```

### GHS-Piktogramm Strip

Nach den Trust-Badges werden 5 GHS-Piktogramme angezeigt:

| Piktogramm | Bedeutung |
|------------|-----------|
| GHS02 | Entzündbar |
| GHS05 | Ätzend |
| GHS06 | Giftig |
| GHS07 | Reizend |
| GHS09 | Umweltgefährlich |

**CDN-Pfad:** `https://cdn.oysi.tech/ghs/GHS0X.svg`

```css
.ghs-strip {
    display: flex;
    gap: 0.75rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.03);
}
.ghs-strip img {
    width: 36px;
    filter: grayscale(30%) brightness(0.9);
}
.ghs-strip img:hover {
    filter: grayscale(0%) brightness(1);
}
```

### Chemical Data Typography

Für CAS-Nummern, Formeln und technische Daten:

```css
.chemical-data {
    font-family: 'JetBrains Mono', 'Fira Code', var(--font-mono);
    letter-spacing: 0.02em;
}
```

### Logo-Sichtbarkeit

Logos benötigen Brightness-Filter wegen dunklem Hintergrund:

```css
.hero-logo img { filter: brightness(2) contrast(1.1); }
.nav-logo img { filter: brightness(1.8) contrast(1.1); }
.footer-brand .logo { filter: brightness(1.6) contrast(1.1); }
```

### Karten-Design (Semi-transparent)

```css
.card {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(148, 163, 184, 0.2);
}
```

### Timeline (Auto-Scroll, Zwei-Zeilen-Layout)

Die Firmengeschichte wird als auto-scrollende Timeline mit Zwei-Zeilen-Layout dargestellt:

| Jahr | Titel | Text | Detail (Highlight) |
|------|-------|------|-------------------|
| 1995 | Ursprung | Start in einer Garage | Luisenthalerstraße, **Saarbrücken** |
| 2005 | Gründung | Firmengründung | **Höfer Chemie GmbH** |
| 2009 | Industrialisierung | Eigene Produktion & Logistik | Standort **Sulzbach** |
| 2018 | Produktionsstandort | Neubau in Kleinblittersdorf | **11.500 m²** Produktionsfläche |
| 2021 | Logistikzentrum | Inbetriebnahme Logistik | **10.500 m²** Lager- & Versandfläche |
| 2022 | Beteiligungsverkauf | Verkauf der Unternehmensanteile | **Minderheitsgesellschafter** |
| 01/2026 | Exit Management | Abgabe der Geschäftsführung | **Kein Gesellschafter mehr** |
| 02/2026 | Neustart | **OYSI GmbH** | Technische Chemie & Digital *(grün)* |

**Design-Prinzipien (A + B Konzept):**
- **A) Highlight-Spans** (`.hl`): Wichtige Zahlen/Begriffe in Akzentfarbe (#3b82f6)
- **B) Zwei-Zeilen-Layout**: Titel + Text, darunter Detail-Zeile (kleiner, grau)
- Mobil-safe: kein Hover, keine versteckten Infos
- Highlight nicht fett, Farbe reicht → Premium-Look

**Features:**
- Auto-Scroll Animation (15s Zyklus)
- Pause bei Hover
- Gradient-Mask (oben/unten ausgeblendet)
- Grünes Highlight für aktuellen Eintrag (02/2026)

**Übersetzungs-Keys:** `about.timeline.t1` bis `about.timeline.t8`

| Key | Felder |
|-----|--------|
| t1, t2 | `.title`, `.text` |
| t3 | `.title`, `.text`, `.location` |
| t4, t5 | `.title`, `.text`, `.unit` |
| t6, t7 | `.title`, `.text`, `.detail` |
| t8 | `.title`, `.detail` |

```css
.timeline-wrapper { max-height: 220px; overflow: hidden; }
.timeline { animation: scrollTimeline 15s linear infinite; }
.timeline:hover { animation-play-state: paused; }
.timeline-text { font-size: 0.9rem; color: var(--text-secondary); }
.timeline-detail { font-size: 0.8rem; color: var(--text-muted); }
.timeline-text .hl, .timeline-detail .hl { color: var(--accent-primary); }
.timeline-item.highlight .timeline-year { color: #22c55e; }
```

## SEO (2026 Best Practices - GEO/AEO Ready)

### Structured Data (12 JSON-LD Schemas)

| Schema | Zweck |
|--------|-------|
| `Organization` | Firmendaten, Gründer, Kontakt, knowsAbout, sameAs, Identifier |
| `WebSite` | Site-Suche via oysi.eu/lexikon |
| `WebPage` | Aktuelle Seite mit dateModified |
| `BreadcrumbList` | Navigation für SERP |
| `LocalBusiness` | Lokale SEO, Öffnungszeiten |
| `FAQPage` | 7 FAQs für GEO/AI-Suche (answer-ready format) |
| `Service` | Dienstleistungskatalog |
| `Person` | **NEU 2026:** Olivier Höfer als Experten-Entität (E-E-A-T) |
| `Speakable` | **NEU 2026:** Voice Search Optimierung |
| `HowTo` | **NEU 2026:** "Wie bestelle ich bei OYSI?" für AI-Antworten |
| `DefinedTermSet` | **NEU 2026:** Chemie-Glossar als Entity (DPP, REACH, GHS) |
| `ItemList` | **NEU 2026:** Strukturierte Kernkompetenzen für AI-Zitierung |

### GEO 2026 (Generative Engine Optimization)

| Feature | Implementierung |
|---------|-----------------|
| Answer-ready Content | FAQs mit direkten ersten Sätzen |
| Entity Building | sameAs (NorthData, Firmenwissen), Identifier (HRB, USt-IdNr) |
| Speakable | CSS-Selektoren für Voice Search |
| HowTo Schema | Bestellprozess als strukturierte Schritte |
| Author/Person | Olivier Höfer mit knowsAbout, Credentials |

### Meta Tags

- Primary Meta (title, description, keywords, robots)
- Open Graph (vollständig mit image dimensions)
- Twitter Cards (summary_large_image)
- Geo Meta Tags (geo.region, geo.placename)
- Dublin Core (DC.title, DC.creator)

### Core Web Vitals Optimierungen

| Metrik | Implementierung |
|--------|-----------------|
| **LCP** | Preload Logo, preconnect CDN, font-display: swap |
| **CLS** | Explizite width/height, aspect-ratio, content-visibility |
| **INP** | GPU compositing, reduced motion support |

### Accessibility

- Skip-Link für Tastaturnavigation
- ARIA landmarks (role="banner", "navigation", "main", "contentinfo")
- aria-labelledby für alle Sections
- Microdata (itemprop, itemscope, itemtype)

## Spam-Schutz

Das Kontaktformular ist gegen Bots geschützt:

| Mechanismus | Details |
|-------------|---------|
| **Honeypot** | Verstecktes `website`-Feld, Fake-Erfolg bei Ausfüllung |
| **Zeitprüfung** | Mindestens 3 Sekunden Formularladezeit |
| **Rate Limiting** | Max. 3 Anfragen/IP in 10 Minuten |

## API-Endpunkte

| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| POST | `/api/contact` | Kontaktformular absenden |
| GET | `/api/health` | Health Check |

### Kontaktformular-Payload

```json
{
  "email": "absender@example.com",
  "message": "Nachrichtentext",
  "website": "",
  "form_time": 1704067200000
}
```

## Umgebungsvariablen (.env)

```env
EMAIL_PASSWORD=xxx          # SMTP-Passwort (erforderlich)
SMTP_SERVER=smtp.mail.ovh.net
EMAIL_SENDER=info@oysi.tech
EMAIL_RECIPIENT=olivier.hoefer@oysi.gmbh
```

## Netzwerk & Deployment

| Netzwerk | Zweck |
|----------|-------|
| `proxy` | Traefik → Container |
| `oysi-net` | Interne Kommunikation |
| `default` | Backend-Kommunikation |

**Traefik Labels:**
- `oysi.gmbh` / `www.oysi.gmbh` → oysi_static:80
- `oysi.tech` / `www.oysi.tech` → Redirect zu oysi.gmbh

## Sektionen der Website

1. **Hero** - Großes Logo mit Glow, Stats-Counter, CTAs, Hexagon-Molekül-Hintergrund
2. **Über uns** - Firmengeschichte mit Auto-Scroll Timeline (8 Meilensteine, Zwei-Zeilen-Layout), Gründer-Info, Trust-Badges, GHS-Strip
3. **Leistungen** - 4 Service-Karten mit SVG-Icons (Flask, GHS-Diamond, QR-Code, Benzene)
4. **Digital Solutions** - Browser-Frames für dpp.oysi.gmbh und oysi.eu
5. **Branchen** - 4 Industrie-SVG-Icons (Barrel, Test Tubes, Spray Bottle, Gear)
6. **Warum OYSI** - USP-Liste mit Checkmarks
7. **Kontakt** - Kontaktdaten + Formular
8. **Footer** - Links, Legal (HRB 109351, DE368627554)

## Wichtige URLs im OYSI-Ökosystem

| URL | Beschreibung |
|-----|--------------|
| https://oysi.gmbh | Corporate Website (dieses Projekt) |
| https://oysi.eu | Chemie-Lexikon (3.800+ Substanzen) |
| https://dpp.oysi.gmbh | Digital Product Passport |
| https://cdn.oysi.tech | CDN für statische Assets |

## Häufige Änderungen

### Passwort ändern

```javascript
// In index.html, Zeile ~2660
const PASSWORD = 'oysi2026';
```

### Neue Sprache hinzufügen

1. Button in `.lang-switcher` hinzufügen
2. Translations-Objekt erweitern (DE/FR/EN als Vorlage)
3. hreflang-Link im Head hinzufügen

### Farben ändern

Alle Farben sind als CSS Custom Properties in `:root` definiert (Zeile ~400-435).

### SVG Icons ändern

Die SVG-Icons sind inline im HTML definiert:
- **Service Icons:** Zeile ~2463-2530
- **Industry Icons:** Zeile ~2610-2660

Alle Icons verwenden `stroke="currentColor"` und erben die Farbe von `.service-icon` / `.industry-icon`.
