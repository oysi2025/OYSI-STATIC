#!/bin/bash
# Build-Skript für internationale Versionen
# Führe dieses Skript nach Änderungen an index.html aus!

cd /home/ubuntu/services/oysi-static/public

echo "Building French version..."
sed -e 's/<html lang="de"/<html lang="fr"/g' \
    -e 's|<link rel="canonical" href="https://oysi.gmbh/">|<link rel="canonical" href="https://oysi.gmbh/fr/">|g' \
    -e 's|<meta property="og:url" content="https://oysi.gmbh/">|<meta property="og:url" content="https://oysi.gmbh/fr/">|g' \
    -e 's|<meta property="og:locale" content="de_DE">|<meta property="og:locale" content="fr_FR">|g' \
    -e 's|<meta name="twitter:url" content="https://oysi.gmbh/">|<meta name="twitter:url" content="https://oysi.gmbh/fr/">|g' \
    -e 's|"inLanguage": "de-DE"|"inLanguage": "fr-FR"|g' \
    -e 's|<meta name="DC.language" content="de">|<meta name="DC.language" content="fr">|g' \
    index.html > fr/index.html

echo "Building English version..."
sed -e 's/<html lang="de"/<html lang="en"/g' \
    -e 's|<link rel="canonical" href="https://oysi.gmbh/">|<link rel="canonical" href="https://oysi.gmbh/en/">|g' \
    -e 's|<meta property="og:url" content="https://oysi.gmbh/">|<meta property="og:url" content="https://oysi.gmbh/en/">|g' \
    -e 's|<meta property="og:locale" content="de_DE">|<meta property="og:locale" content="en_US">|g' \
    -e 's|<meta name="twitter:url" content="https://oysi.gmbh/">|<meta name="twitter:url" content="https://oysi.gmbh/en/">|g' \
    -e 's|"inLanguage": "de-DE"|"inLanguage": "en-US"|g' \
    -e 's|<meta name="DC.language" content="de">|<meta name="DC.language" content="en">|g' \
    index.html > en/index.html

echo "Done! FR and EN versions updated."
echo ""
echo "Don't forget to restart the container:"
echo "  cd /home/ubuntu/services/oysi-static && docker compose restart site-vitrine"
