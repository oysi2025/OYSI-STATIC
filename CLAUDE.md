# OYSI Static Website

Corporate Landingpage für die OYSI GmbH (https://oysi.gmbh) mit Kontaktformular-Backend.

**Repository**: https://github.com/oysi2025/OYSI-STATIC

## Quick Info

| Aspekt | Details |
|--------|---------|
| **URL** | https://oysi.gmbh |
| **Sprachen** | DE (index.html), FR (/fr/), EN (/en/) - separate HTML-Dateien |
| **Letztes Audit** | ✅ 31. Januar 2026 (WCAG 2.2 AA, Security, CWV) |
| **Passwort-Schutz** | ❌ Entfernt (Januar 2026) |
| **CDN** | https://cdn.oysi.tech (Logos, Favicons, OG-Images) |
| **Reverse Proxy** | Traefik (kein direkter Port-Zugriff) |
| **Analytics** | Google Analytics 4 (`G-GDV44WVP0Z`) + Consent Mode v2 |

## Kontaktdaten

| Feld | Wert |
|------|------|
| **Adresse** | Halbergstr. 4, 66121 Saarbrücken |
| **Telefon** | +49 681 / 309 883 75 |
| **E-Mail** | hello@oysi.gmbh |
| **HRB** | 109351 (AG Saarbrücken) |
| **USt-IdNr** | DE368627554 |

**Hinweis:** Keine Mobilnummer auf der Website (Datenschutz).

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

## Projektstruktur (Stand: Februar 2026)

```
oysi-static/
├── public/
│   ├── de/                  # Deutsche Seiten (Master)
│   │   ├── index.html       # Homepage
│   │   ├── about.html       # Über uns
│   │   ├── services.html    # Leistungen
│   │   ├── dpp.html         # Digital Product Passport
│   │   ├── outcomes.html    # Referenzen & Case Studies (NEU)
│   │   ├── seo-block.html   # Pillar Page (NEU, in Arbeit)
│   │   ├── faq.html         # FAQ
│   │   ├── contact.html     # Kontakt
│   │   ├── legal.html       # Impressum
│   │   └── privacy.html     # Datenschutz
│   ├── fr/                  # Französische Seiten (Struktur identisch)
│   ├── en/                  # Englische Seiten (Struktur identisch)
│   ├── archive/             # Alte Seiten (Backup)
│   ├── sitemap.xml          # 30 URLs mit hreflang
│   └── robots.txt
├── backend/
│   ├── main.py              # FastAPI Kontaktformular-API
│   ├── requirements.txt
│   └── Dockerfile
├── nginx.conf               # Sprachrouting + 301 Redirects
├── docker-compose.yml       # Service-Orchestrierung (Traefik Labels)
├── .env                     # SMTP-Zugangsdaten (NICHT in Git!)
└── CLAUDE.md
```

### URL-Struktur (Stand: Februar 2026)

**Root** → 302 Redirect zu `/de/`

| Seite | DE | FR | EN |
|-------|----|----|-----|
| **Homepage** | `/de/` | `/fr/` | `/en/` |
| **Über uns** | `/de/about.html` | `/fr/about.html` | `/en/about.html` |
| **Leistungen** | `/de/services.html` | `/fr/services.html` | `/en/services.html` |
| **DPP** | `/de/dpp.html` | `/fr/dpp.html` | `/en/dpp.html` |
| **Outcomes** | `/de/outcomes.html` | `/fr/outcomes.html` | `/en/outcomes.html` |
| **SEO-Block** | `/de/seo-block.html` | `/fr/seo-block.html` | `/en/seo-block.html` |
| **FAQ** | `/de/faq.html` | `/fr/faq.html` | `/en/faq.html` |
| **Kontakt** | `/de/contact.html` | `/fr/contact.html` | `/en/contact.html` |
| **Impressum** | `/de/legal.html` | `/fr/legal.html` | `/en/legal.html` |
| **Datenschutz** | `/de/privacy.html` | `/fr/privacy.html` | `/en/privacy.html` |

### 301 Redirects (SEO-Migration)

Alte URLs werden automatisch auf neue umgeleitet:
- `/about/` → `/de/about.html`
- `/services/` → `/de/services.html`
- `/services/dpp/` → `/de/dpp.html`
- `/contact/` → `/de/contact.html`
- `/faq/` → `/de/faq.html`
- `/legal/` → `/de/legal.html`
- `/privacy/` → `/de/privacy.html`

### Neue Seiten (Februar 2026)

**outcomes.html** – Referenzen & Case Studies
- KPI-Grid: 6 Wo. Audit-ready, −70% Behördenrückfragen, 50% schnellere Freigaben, 3.800+ Produkte, 0 Blockierer
- 3 Case Studies: Chemiehandel, Labor & Produktion, Logistik & Gefahrgut
- Schema.org: ItemList mit 3 Articles

**seo-block.html** – Pillar Page (in Arbeit)
- Geplant: REACH Compliance Guide 2026

### Datenschutzseite (Stand: 31. Januar 2026)

Vollständige DSGVO-konforme Datenschutzerklärung mit 7 Abschnitten:

1. **Datenschutz auf einen Blick** - Allgemeine Hinweise, Verantwortlicher, Datenerfassung
2. **Hosting** - OVH (Saarbrücken), AVV, ISO 27001/27701
3. **Allgemeine Hinweise** - Verantwortlicher, Widerrufsrecht, SSL/TLS
4. **Datenerfassung** - Cookies (oysi_consent, _ga), Server-Logs, Kontaktanfragen
5. **Analyse-Tools (Google)** - Consent Mode V2 (4 Parameter), GA4 mit IP-Anonymisierung, EU-US DPF
6. **Betroffenenrechte** - Art. 15-21 DSGVO, Aufsichtsbehörde (UDZ Saarland)
7. **Aktualität** - Stand Januar 2026

**Hinweis:** Keine Mobilnummer im Verantwortlichen-Abschnitt (gemäß Policy).

### Sprachversionen (Homepage only)

| URL | Datei | Canonical |
|-----|-------|-----------|
| `oysi.gmbh/` | `public/index.html` | `oysi.gmbh/` |
| `oysi.gmbh/fr/` | `public/fr/index.html` | `oysi.gmbh/fr/` |
| `oysi.gmbh/en/` | `public/en/index.html` | `oysi.gmbh/en/` |

**Hinweis:** Unterseiten (about, services, etc.) sind aktuell nur auf Deutsch. i18n kann später ergänzt werden.

**WICHTIG:** Nach Änderungen an `index.html`:
```bash
./build-i18n.sh && docker compose restart site-vitrine
```

## Design System (Stand: Januar 2026)

### Farbpalette (OYSI Corporate Identity - Beige + Petrol Blue)

```css
:root {
    /* OYSI Corporate Identity */
    --oysi-primary: #095A7D;        /* Petrol Blue Dark - Header, Footer */
    --oysi-secondary: #027897;      /* Petrol Blue Medium - Sections */
    --oysi-accent: #17ACBA;         /* Teal - Links, Icons, Accents */
    --oysi-accent-light: #52CCCD;   /* Teal Light - Hover states */
    --oysi-highlight: #EF655E;      /* Coral - CTA (1 per page!) */
    --oysi-bg-main: #F0ECE6;        /* Warm Beige - Main background */
    --oysi-bg-alt: #D8D3CC;         /* Gray Beige - Alternating sections */
    --oysi-text-muted: #8A949B;     /* Muted text */
    --oysi-text-primary: #095A7D;   /* Headings (petrol blue) */
    --oysi-text-body: #2D3748;      /* Body text (dark gray) */

    /* Legacy mappings (for compatibility) */
    --bg-primary: var(--oysi-primary);
    --bg-secondary: var(--oysi-secondary);
    --bg-card: var(--oysi-bg-alt);
    --accent-primary: var(--oysi-accent);
    --accent-secondary: var(--oysi-accent-light);

    /* Industrial/Chemical accent colors */
    --chemical-yellow: #fbbf24;
    --chemical-orange: #f97316;
    --industrial-steel: #64748b;
    --safety-green: #17ACBA;        /* Now uses accent color */
}
```

### Farbverwendung

| Farbe | Verwendung |
|-------|------------|
| `--oysi-primary` (#095A7D) | Header, Footer, Primary Backgrounds |
| `--oysi-secondary` (#027897) | Hero Gradient, Section Backgrounds |
| `--oysi-accent` (#17ACBA) | Links, Icons, Timeline, Badges |
| `--oysi-accent-light` (#52CCCD) | Hover States, Highlights |
| `--oysi-highlight` (#EF655E) | **CTA Buttons** (nur 1 pro Viewport!) |
| `--oysi-bg-main` (#F0ECE6) | Body Background (Warm Beige) |
| `--oysi-bg-alt` (#D8D3CC) | Alternating Sections (Gray Beige) |
| `--oysi-text-primary` (#095A7D) | Headings |
| `--oysi-text-body` (#2D3748) | Body Text |
| `--oysi-text-muted` (#8A949B) | Secondary/Muted Text |

### iOS Safari Compatibility (Stand: Januar 2026)

**WICHTIG:** iOS Safari hat Rendering-Probleme mit `backdrop-filter: blur()`.

Die folgenden CSS-Fixes sind in allen HTML-Seiten implementiert (direkt nach `:root`):

```css
/* iOS Safari: Disable backdrop-filter (causes rendering issues) */
@supports (-webkit-touch-callout: none) {
    * {
        -webkit-backdrop-filter: none !important;
        backdrop-filter: none !important;
    }
    .nav.scrolled {
        background: rgba(9, 90, 125, 0.98) !important;
    }
}
```

**Zusätzlich vermeiden:**
- `inset: 0` → Explizit `top: 0; left: 0; right: 0; bottom: 0` verwenden
- `position: fixed` mit `backdrop-filter` kombinieren
- Fullscreen-Overlays die `overflow: hidden` auf body setzen

### Scroll-to-Top Button (Stand: Januar 2026)

Ein Scroll-to-Top Button erscheint nach 500px Scrolltiefe:

```css
.scroll-to-top {
    position: fixed;
    bottom: 100px;
    right: 24px;
    width: 56px;
    height: 56px;
    background: var(--oysi-highlight);  /* Coral */
    color: #ffffff;
    border-radius: 50%;
    display: none;  /* Default hidden */
    z-index: 999999;  /* Above cookie banner */
}
.scroll-to-top.visible {
    display: flex;
}
```

**HTML-Position:** Nach `</footer>`, vor `<script>`
**JavaScript:** Fügt `.visible` class bei `scrollY > 500` hinzu

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

Logos benötigen Brightness-Filter wegen des petrol-blauen Header/Footer-Hintergrunds:

```css
.hero-logo img { filter: brightness(2) contrast(1.1); }
.nav-logo img { filter: brightness(1.8) contrast(1.1); }
.footer-brand .logo { filter: brightness(1.6) contrast(1.1); }
```

### Karten-Design (Semi-transparent)

```css
.card {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(9, 90, 125, 0.15);
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
- **A) Highlight-Spans** (`.hl`): Wichtige Zahlen/Begriffe in Akzentfarbe (#17ACBA)
- **B) Zwei-Zeilen-Layout**: Titel + Text, darunter Detail-Zeile (kleiner, grau)
- Mobil-safe: kein Hover, keine versteckten Infos
- Highlight nicht fett, Farbe reicht → Premium-Look

**Features:**
- Auto-Scroll Animation (15s Zyklus)
- Pause bei Hover
- Gradient-Mask (oben/unten ausgeblendet)
- Teal Highlight für aktuellen Eintrag (02/2026) - jetzt `--oysi-accent` statt grün

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
.timeline-text { font-size: 0.9rem; color: var(--oysi-text-body); }
.timeline-detail { font-size: 0.8rem; color: var(--oysi-text-muted); }
.timeline-text .hl, .timeline-detail .hl { color: var(--oysi-accent); }
.timeline-item.highlight .timeline-year { color: var(--oysi-accent); }
```

## SEO (2026 Best Practices - GEO/AEO Ready)

### Unterseiten-SEO (Stand: 31. Januar 2026)

Alle 7 Unterseiten wurden auf Homepage-Niveau gebracht:

| Feature | Implementiert auf allen Unterseiten |
|---------|-------------------------------------|
| **Google Consent Mode v2** | ✅ Erweitert mit `allow_google_signals: false` |
| **Hreflang Tags** | ✅ DE + x-default |
| **Open Graph** | ✅ og:title, og:description, og:image, og:url |
| **Twitter Cards** | ✅ summary_large_image (Hauptseiten) / summary (Legal) |
| **Geo Meta Tags** | ✅ DE-SL, Saarbrücken |
| **Preconnect/DNS-Prefetch** | ✅ cdn.oysi.tech, fonts.googleapis.com |
| **JSON-LD WebPage** | ✅ Mit dateModified, isPartOf, breadcrumb |
| **JSON-LD BreadcrumbList** | ✅ Startseite → Aktuelle Seite |
| **Seitenspezifische Schemas** | ✅ FAQPage, LocalBusiness, Service, AboutPage |

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

### Schema.org Validator-Konformität

Folgende Anpassungen wurden für Google Rich Results gemacht:

| Problem | Lösung |
|---------|--------|
| `PostalAddress` unvollständig | `streetAddress` + `postalCode` hinzugefügt |
| `Product` ohne offers/review | `@type: Thing` statt `Product` in OfferCatalogs |
| `ItemList` ohne item-Property | `ListItem.item` mit `@type: Service` |
| `Person.sameAs` leer | Leeres Array entfernt |
| `HowTo.estimatedCost` nicht-numerisch | Feld entfernt |

Validierung: https://validator.schema.org/ und https://search.google.com/test/rich-results

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

### Google Analytics 4

**Hinweis:** Wir verwenden gtag.js (GA4 direkt), NICHT den Google Tag Manager (GTM).

Google Tag ist auf allen Seiten eingebunden (direkt nach `<head>`):

| Property | Wert |
|----------|------|
| **Measurement ID** | `G-GDV44WVP0Z` |
| **Eingebunden in** | Alle Seiten (Homepage + 7 Unterseiten + Sprachversionen) |

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GDV44WVP0Z"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-GDV44WVP0Z');
</script>
```

### Cookie Consent Banner (DSGVO-konform)

**Stand: Januar 2026** - Implementiert als **Non-Blocking Bottom-Bar** mit Google Consent Mode v2.

| Feature | Status |
|---------|--------|
| **Google Consent Mode v2** | ✅ GA4 erst nach Einwilligung aktiv |
| **Non-Blocking Design** | ✅ Bottom-bar, Seite bleibt scrollbar |
| **iOS Safari Compatible** | ✅ Kein backdrop-filter, kein overflow:hidden |
| **3 klare Buttons** | ✅ "Alle akzeptieren", "Nur Essenzielle", "Einstellungen" |
| **Responsive** | ✅ 48px Touch Targets, Mobile-optimiert |
| **Corporate Design** | ✅ Petrol Blue mit OYSI CI Farben |
| **i18n** | ✅ Separate HTML-Dateien (DE/FR/EN) |
| **Footer-Link** | ✅ "Cookie-Einstellungen" zum nachträglichen Ändern |

**WICHTIG - iOS Safari Kompatibilität:**
- Kein `document.body.style.overflow = 'hidden'`
- Kein Fullscreen-Overlay mit `position: fixed; inset: 0`
- Kein `backdrop-filter: blur()`
- Einfache Bottom-Bar mit `position: fixed; bottom: 0`

**CSS-Struktur:**
```css
.cookie-banner {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 99999;
    padding: 16px;
    background: #ffffff;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.15);
}
.cookie-banner-overlay {
    display: none;  /* Kein Overlay mehr */
}
```

**JavaScript:**
```javascript
const COOKIE_NAME = 'oysi_consent';
const COOKIE_EXPIRY_DAYS = 365;

// Google Consent Mode v2 Default (vor gtag.js)
gtag('consent', 'default', {
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied',
    'analytics_storage': 'denied',
    'wait_for_update': 500
});

// Nach Einwilligung
gtag('consent', 'update', {
    'analytics_storage': 'granted',
    'ad_storage': 'granted'
});
```

**Footer-Link zum Öffnen:**
```javascript
window.openCookieConsent()  // Öffnet Banner mit aktuellen Einstellungen
```

## Spam-Schutz

Das Kontaktformular ist gegen Bots geschützt:

| Mechanismus | Details |
|-------------|---------|
| **Honeypot** | Verstecktes `website`-Feld, Fake-Erfolg bei Ausfüllung |
| **Zeitprüfung** | Mindestens 3 Sekunden Formularladezeit |
| **Rate Limiting** | Max. 3 Anfragen/IP in 10 Minuten |

### E-Mail Anti-Scraping

Die E-Mail-Adresse ist vor Bots geschützt:

```html
<a href="#" class="email-protect" data-u="hello" data-d="oysi.gmbh">
    hello[at]oysi.gmbh
</a>
```

JavaScript baut zur Laufzeit die echte E-Mail und den `mailto:`-Link zusammen. Bots ohne JS sehen nur `hello[at]oysi.gmbh`.

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

## SOPS Secret Management

> Siehe `/.claude/SOPS.md` fuer Architektur und Befehle.

| Datei | Inhalt |
|-------|--------|
| `secrets/.env.enc.yaml` | EMAIL_PASSWORD, SMTP_SERVER, EMAIL_SENDER, EMAIL_RECIPIENT |

## Netzwerk & Deployment

| Netzwerk | Zweck |
|----------|-------|
| `proxy` | Traefik → Container |
| `oysi-net` | Interne Kommunikation |
| `default` | Backend-Kommunikation |

**Traefik Labels:**
- `oysi.gmbh` / `www.oysi.gmbh` → oysi_static:80
- `oysi.tech` / `www.oysi.tech` → Redirect zu oysi.gmbh

## Sektionen der Website (Homepage)

### 1. Hero
- Großes Logo mit Glow-Effekt
- Stats-Counter (animiert)
- **KPI-Bar** (neu 01/2026): 4 messbare Outcomes direkt unter Hero-CTAs
  - `−60%` Koordinationsaufwand bei SDB-Erstellung
  - `24h` Lieferzeit für Compliance-Dokumente
  - `3.800+` Substanzen sofort abrufbar
  - `0` IT-Ressourcen für DPP nötig
- **CTAs** (Hierarchie):
  - Primary: `Kostenfreie Ersteinschätzung` (Coral mit Pulse-Animation)
  - Secondary: `Lexikon entdecken`
- Hexagon-Molekül-Hintergrund (SVG Pattern)

### 2. Über uns
- Auto-Scroll Timeline (8 Meilensteine, Zwei-Zeilen-Layout)
- Gründer-Info mit E-E-A-T Schema
- Trust-Badges
- GHS-Piktogramm Strip

### 3. Leistungen
- 4 Service-Karten mit SVG-Icons
- **SEO-optimierte H2-Titel** (neu 01/2026):
  - `REACH-konforme Chemikalien & Compliance in Europa`
  - `Digitaler Produktpass (DPP) für Chemikalien – EU-konform`

### 4. Digital Solutions
- Browser-Frames für dpp.oysi.gmbh und oysi.eu

### 5. Branchen (Segmentierung)
- Problem → Lösung Pattern pro Segment
- 4 Industrie-SVG-Icons (Barrel, Test Tubes, Spray Bottle, Gear)

### 6. Warum OYSI
- USP-Liste mit Checkmarks

### 7. Kontakt (Premium B2B - neu 01/2026)

**Positionierung:** Exklusiv, strategisch, CEO-direkt (nicht generisch)

| Element | DE | FR | EN |
|---------|----|----|-----|
| **Section-Label** | Strategische Beratung | Conseil stratégique | Strategic Advisory |
| **Section-Title** | Ihr Projekt vertraulich bewerten lassen | Faire évaluer votre projet en toute confidentialité | Have Your Project Confidentially Evaluated |
| **Section-Subtitle** | Persönliche Ersteinschätzung durch den Geschäftsführer – keine Wartezeiten, keine Call-Center. | Première évaluation personnalisée par le directeur général – sans attente, sans centre d'appels. | Personal initial assessment by the CEO – no waiting, no call centers. |
| **Form-Title** | Strategische Anfrage stellen | Soumettre une demande stratégique | Submit a Strategic Inquiry |
| **Placeholder** | Beschreiben Sie kurz Ihr Projekt oder Ihre Compliance-Herausforderung... | Décrivez brièvement votre projet ou votre défi de conformité... | Briefly describe your project or compliance challenge... |
| **Submit-Button** | Projekt vertraulich einreichen | Soumettre votre projet en toute confidentialité | Submit Project Confidentially |

**Formular-Features:**
- Inquiry-Type Checkboxes (Projekt / Compliance-Check / DPP)
- Honeypot Spam-Schutz
- ARIA-Attribute für Accessibility
- Rate Limiting (3 Anfragen/10 Min)

### 8. Footer
- Links, Legal (HRB 109351, DE368627554)
- Cookie-Einstellungen Link

## Wichtige URLs im OYSI-Ökosystem

| URL | Beschreibung |
|-----|--------------|
| https://oysi.gmbh | Corporate Website (dieses Projekt) |
| https://oysi.eu | Chemie-Lexikon (3.800+ Substanzen) |
| https://dpp.oysi.gmbh | Digital Product Passport |
| https://cdn.oysi.tech | CDN für statische Assets |

## Häufige Änderungen

### Farben ändern

Alle Farben sind als CSS Custom Properties in `:root` definiert (Zeile ~400-435).

### SVG Icons ändern

Die SVG-Icons sind inline im HTML definiert:
- **Service Icons:** Zeile ~2463-2530
- **Industry Icons:** Zeile ~2610-2660

Alle Icons verwenden `stroke="currentColor"` und erben die Farbe von `.service-icon` / `.industry-icon`.

### Sprachversionen aktualisieren

**ACHTUNG:** Jede Sprachversion hat eine eigene HTML-Datei:
- `/public/index.html` - Deutsche Version (Master)
- `/public/fr/index.html` - Französische Version
- `/public/en/index.html` - Englische Version

Bei Änderungen an CSS oder JavaScript müssen ALLE Dateien aktualisiert werden!

Die deutsche Version (`index.html`) verwendet KEIN client-seitiges i18n mehr - der Inhalt ist direkt auf Deutsch im HTML.

---

## Changelog (Januar 2026)

### 31. Januar 2026 - Audit & Conversion-Optimierung

**Technisches Audit (Mobile/Desktop):**
- WCAG 2.2 AA Compliance geprüft
- Core Web Vitals optimiert (LCP, CLS, INP)
- Security Headers hinzugefügt (CSP, X-Content-Type-Options, Referrer-Policy)

**Accessibility-Fixes (P0-P2):**
- `aria-live="polite"` für Formular-Feedback
- `aria-invalid` für Validierungsstatus
- Focus-Trap für Cookie-Dialog
- Touch-Targets auf 44px minimum erhöht
- `role="alert"` für Fehlermeldungen

**Conversion-Optimierung:**
- **KPI-Bar:** 4 messbare Outcomes unter Hero (−60%, 24h, 3.800+, 0)
- **CTA-Hierarchie:** Primary mit Pulse-Glow Animation hervorgehoben
- **SEO H2-Titel:** Keyword-optimiert für Suchintent
- **Premium-Kontaktbereich:** B2B-exklusiv, CEO-direkt positioniert

**Schema.org Updates:**
- `Speakable` für Voice Search
- `Person` mit E-E-A-T Signalen (Olivier Höfer)
- `HowTo` für AI-Antworten

---

### 31. Januar 2026 - Major Update

**OYSI Corporate Identity Refonte:**
- Alle Farben von Navy/Dark Theme auf Beige + Petrol Blue umgestellt
- ~200+ Farbwerte pro Seite aktualisiert (11 HTML-Dateien)
- CSS Custom Properties (`:root`) mit neuer OYSI CI Palette
- Alle hardcoded rgba() und hex Werte durch Variablen ersetzt

**iOS Safari Fixes:**
- `backdrop-filter: blur()` auf iOS deaktiviert (verursacht Rendering-Probleme)
- `inset: 0` durch explizite `top/left/right/bottom` ersetzt
- Media Query `@supports (-webkit-touch-callout: none)` für iOS-spezifisches CSS

**Passwort-Schutz entfernt:**
- Preview-Modus mit Passwort komplett entfernt
- CSS, HTML und JavaScript für Password-Gate gelöscht
- Website ist jetzt öffentlich zugänglich

**Cookie Banner neu implementiert:**
- Fullscreen-Overlay durch Non-Blocking Bottom-Bar ersetzt
- `overflow: hidden` auf body entfernt (blockierte Scrollen auf iOS)
- Google Consent Mode v2 weiterhin aktiv
- iOS Safari kompatibel

**Scroll-to-Top Button:**
- Neuer Button unten rechts nach 500px Scrolltiefe
- Coral-Farbe (`--oysi-highlight`) als Akzent
- z-index 999999 (über Cookie Banner)
- Smooth-Scroll Animation

**Sprachversionen:**
- Client-seitiges i18n auf deutscher Hauptseite deaktiviert
- Jede Sprache hat nun dedizierte HTML-Datei mit nativen Inhalten
- Language-Switcher verlinkt direkt auf `/`, `/fr/`, `/en/`

---

## Logs

- **Loki:** `{filename=~".*oysi_static.*"}` → [Grafana Explore](https://grafana.oysi.tech/explore)
- **Docker:** `docker logs oysi_static --tail 50`

---

## Task Management

Siehe `tasks/todo.md` | `tasks/lessons.md` | Regeln: `/.claude/GLOBAL_CLAUDE.md`
