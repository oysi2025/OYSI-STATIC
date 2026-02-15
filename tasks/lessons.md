# Lessons Learned - oysi-static

> Ce fichier capture les erreurs et corrections pour éviter de les répéter.
> Claude Code DOIT mettre à jour ce fichier après chaque correction d'Olivier.

---

## Leçons

### 2026-02-02: CSS Minification überschreibt Sprachinhalte

**Problem:** Das CSS-Minify-Skript hat versehentlich deutschen Inhalt in FR/EN Dateien kopiert.

**Ursache:** Skript hat nicht nur CSS minifiziert, sondern ganze Dateien überschrieben.

**Lösung:**
- Immer Backup vor Batch-Operationen prüfen
- Nach Skript-Ausführung Stichproben der Inhalte verifizieren
- Sprachversionen separat behandeln

### 2026-02-02: EXIF-Orientierung bei WebP-Konvertierung

**Problem:** Bilder waren um 90° verdreht nach WebP-Konvertierung.

**Ursache:** `ImageOps.exif_transpose()` wurde nicht angewendet.

**Lösung:**
```python
from PIL import Image, ImageOps
img = Image.open('photo.jpeg')
img = ImageOps.exif_transpose(img)  # WICHTIG!
img.save('photo.webp', 'WEBP', quality=85)
```

### 2026-02-02: Dateiberechtigungen für CDN

**Problem:** Neue Dateien auf CDN waren nicht lesbar (HTTP 403/404).

**Ursache:** Dateien wurden mit `rw-r-----` (640) erstellt statt `rw-r--r--` (644).

**Lösung:** `chmod 644` für alle Web-Assets.

### 2026-02-02: CDN-Cache bei neuen Dateien

**Problem:** Neue Dateien (favicon.svg) wurden mit 404 gecacht.

**Lösung:** Cache-Busting-Parameter verwenden (`?v=2`).

### 2026-02-15: Docker Volume Mount Caching bei nginx.conf

**Problem:** Nach Änderung von nginx.conf und `nginx -s reload` im Container wurden die alten Regeln weiterhin angewendet.

**Ursache:** Docker bind mounts cachen die Datei zum Zeitpunkt der Container-Erstellung. Ein `nginx -s reload` liest die gecachte Version.

**Lösung:** Immer `docker compose up -d --force-recreate site-vitrine` statt nur `nginx -s reload` verwenden.

### 2026-02-15: Duplicate Microdata + JSON-LD Schema

**Problem:** GSC meldete "Duplicate field FAQPage" auf faq.html.

**Ursache:** Sowohl Microdata (`<html itemtype="FAQPage">`) als auch JSON-LD `@type: FAQPage` waren gleichzeitig aktiv.

**Lösung:** Microdata vom `<html>` Tag entfernen, nur JSON-LD verwenden. JSON-LD ist der von Google bevorzugte Ansatz.

---

## Patterns spécifiques à oysi-static

| Pattern | Beschreibung |
|---------|--------------|
| Sprachversionen | Separate HTML-Dateien in `/de/`, `/fr/`, `/en/` |
| Bilder | WebP auf CDN (`cdn.oysi.tech/images/`) |
| Favicons | CDN unter `/oysi/` |
| CSS | Inline in jeder HTML-Datei (minifiziert) |

---

## Anti-patterns à éviter

| ❌ Ne pas faire | ✅ Faire à la place |
|----------------|---------------------|
| Batch-Skripte ohne Backup | `public.backup.YYYYMMDD/` erstellen |
| Bilder ohne EXIF-Transpose | Immer `ImageOps.exif_transpose()` |
| Neue CDN-Dateien ohne chmod | `chmod 644` nach Upload |
| Statische Assets ohne Version | Cache-Busting `?v=X` hinzufügen |

---

## Checklist de review

Basée sur les leçons apprises pour ce service :
- [ ] Sprachversionen (DE/FR/EN) haben unterschiedliche Inhalte
- [ ] Bilder sind korrekt orientiert (nicht verdreht)
- [ ] CDN-Dateien haben 644 Berechtigungen
- [ ] Neue Assets haben Cache-Busting-Parameter
