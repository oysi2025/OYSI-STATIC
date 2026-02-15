# Todo - oysi-static

> Letzte Aktualisierung: 2026-02-15
> Service: oysi-static

## En cours

_Keine laufende Aufgabe_

## À faire

### Priorität hoch
- [ ] **Maßnahme 6:** EN-Seiten CTR verbessern (0% CTR trotz Impressions)
- [ ] **Maßnahme 7:** Zusätzliche Schema-Markups (Product-Schema für Chemikalien)
- [ ] **Git Push:** Commits noch nicht gepusht (1x Maßnahmen 1-3, 1x Maßnahmen 4-5)

### Priorität normal
- [ ] **GSC Monitoring:** In 2-4 Wochen Ergebnisse der Maßnahmen 1-5 prüfen
  - Phantom-URLs sollten aus Index verschwinden
  - DPP-Seite CTR für "oysi qr code" sollte steigen
  - Interne Verlinkung sollte Crawl-Effizienz verbessern
- [ ] `public.backup.20260202/` Verzeichnis endgültig aus Git entfernen (bereits deleted, nicht committed)

## Terminé

### 2026-02-15 - SEO-Optimierung (GSC-basiert)
- [x] **Maßnahme 1:** Sitemap & Phantom-URL Cleanup
  - Root 302→301, nginx 410 für index.php/archive, robots.txt Disallow, FAQPage Microdata entfernt
- [x] **Maßnahme 2:** Canonical-Konsolidierung
  - JS Canonical-Bug auf Homepages behoben (DE canonical zeigte auf `/` statt `/de/`)
- [x] **Maßnahme 3:** Title & Meta-Description optimieren
  - 24 Seiten keyword-first, CTR-Trigger in Descriptions
- [x] **Maßnahme 4:** "oysi qr code" Landing Page optimieren
  - H1 mit QR-Code (DE/FR/EN), SoftwareApplication Schema, OG-Titles
- [x] **Maßnahme 5:** Keyword-Strategie + Interne Verlinkung
  - Footer standardisiert (7 Links auf 24 Seiten), tote Links entfernt (/blog/, /partner/)
  - Homepage: Interner Link zu /de/dpp.html in DPP-Sektion
  - EN/FR: Nav-Link zu REACH Guide, Footer mit korrekten Sprachpfaden

### 2026-02-02
- [x] SEO Audit komplett (P0-P2 alle erledigt)
- [x] Performance: Forced Reflow Fixes (~275ms eliminiert)
- [x] Performance: WebP Image Conversion (95% kleiner)
- [x] Performance: CSS Minification (47% kleiner)
- [x] Fix: Bild-Rotation (olivier-shahnaz-hoefer.webp)
- [x] Fix: FR/EN Sprachinhalte wiederhergestellt
- [x] Fix: favicon.svg erstellt und aktiv
- [x] seo-block.html - REACH Compliance Guide 2026 erstellt
- [x] FR/EN Unterseiten komplett übersetzt (alle 10 Seiten x 3 Sprachen)
