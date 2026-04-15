

# 🚀 Kryss-Downloader v3.1

Kryss-Downloader est un outil de récupération de médias YouTube conçu pour offrir une flexibilité maximale et une qualité d'image supérieure (jusqu'à 1080p). Contrairement aux outils classiques, il gère les flux **DASH** (Dynamic Adaptive Streaming over HTTP) pour permettre l'extraction de vidéos haute définition même lorsque l'audio est dissocié.

## 🛠️ Fonctionnalités Clés
- **Qualité HD+** : Support complet du 1080p, 720p et résolutions inférieures.
- **Architecture Pro** : Backend Python (Flask) couplé à la puissance de `yt-dlp`.
- **Bypass Avancé** : Intégration de fichiers de cookies pour contourner les limitations de détection de bots et les restrictions d'âge.
- **UI Futuriste** : Interface "Glassmorphism" réactive avec indicateurs de statut des flux (Complet vs Vidéo seule).
- **Optimisation Serveur** : Extraction directe des URLs de flux sans stockage local pour une performance maximale.

## 💻 Stack Technique
- **Backend** : Python 3.x, Flask
- **Core Logic** : yt-dlp
- **Frontend** : HTML5, CSS3 (Syne & DM Mono fonts), JavaScript (Fetch API)

## 📖 Comment ça marche ?
Le projet utilise une logique de tri des formats pour identifier les flux combinés et les flux séparés. 
1. Si un format **combiné** (Audio + Vidéo) existe, il est marqué comme `✅ Complet`.
2. Pour les résolutions supérieures (1080p), le système propose le flux `⚠ Vidéo seule` accompagné de la meilleure piste audio disponible séparément, permettant une fusion externe via VLC ou ffmpeg.

## 🚀 Installation Locale
1. Clonez le dépôt : `git clone https://github.com/votre-nom/kryss-downloader.git`
2. Installez les dépendances : `pip install flask yt-dlp`
3. Ajoutez votre fichier `cookies.txt` à la racine.
4. Lancez : `python app.py`
