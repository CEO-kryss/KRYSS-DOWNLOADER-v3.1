from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

TARGET_HEIGHTS = [1080, 720, 480, 360, 250, 144] 

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/get_formats', methods=['POST'])
def get_formats():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL manquante'}), 400

    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'cookiefile': 'cookies.txt',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats_raw = info.get('formats', [])

            # ── 1. Chercher les formats combinés ──
            combined = {}
            for f in formats_raw:
                h = f.get('height')
                if h not in TARGET_HEIGHTS: continue
                if f.get('vcodec', 'none') == 'none' or f.get('acodec', 'none') == 'none': continue
                tbr = f.get('tbr') or 0
                if h not in combined or tbr > (combined[h].get('tbr') or 0):
                    combined[h] = f

            # ── 2. Prendre le meilleur flux vidéo seul ──
            video_only = {}
            for f in formats_raw:
                h = f.get('height')
                if h not in TARGET_HEIGHTS: continue
                if f.get('vcodec', 'none') == 'none': continue
                if h in combined: continue
                tbr = f.get('tbr') or 0
                if h not in video_only or tbr > (video_only[h].get('tbr') or 0):
                    video_only[h] = f

            # ── 3. Construire les formats vidéo ──
            formats = []
            for h in TARGET_HEIGHTS:
                if h in combined:
                    f = combined[h]
                    filesize = f.get('filesize') or f.get('filesize_approx')
                    formats.append({
                        'resolution': f"{h}p",
                        'ext': f.get('ext', 'mp4'),
                        'url': f.get('url'),
                        'filesize': f"{round(filesize/1024/1024, 1)} Mo" if filesize else "Inconnu",
                        'type': 'direct',
                        'audio_badge': '✅ Audio inclus'
                    })
                elif h in video_only:
                    f = video_only[h]
                    filesize = f.get('filesize') or f.get('filesize_approx')
                    formats.append({
                        'resolution': f"{h}p",
                        'ext': f.get('ext', 'mp4'),
                        'url': f.get('url'),
                        'filesize': f"{round(filesize/1024/1024, 1)} Mo" if filesize else "Inconnu",
                        'type': 'video_only',
                        'audio_badge': '⚠️ Sans audio'
                    })

            # ── 4. CHERCHER LES MEILLEURS FLUX AUDIO SEULS (LA NOUVEAUTÉ) ──
            audio_formats = []
            for f in formats_raw:
                # On cherche les flux qui ont un codec audio, mais PAS de codec vidéo
                if f.get('vcodec', 'none') == 'none' and f.get('acodec', 'none') != 'none':
                    if f.get('ext') in ['m4a', 'webm']: # Les meilleurs formats audios YouTube
                        filesize = f.get('filesize') or f.get('filesize_approx')
                        audio_formats.append({
                            'quality': f"{round(f.get('abr') or f.get('tbr') or 0)} kbps",
                            'ext': f.get('ext'),
                            'filesize': f"{round(filesize/1024/1024, 1)} Mo" if filesize else "Inconnu",
                            'url': f.get('url')
                        })
            
            # On trie pour avoir la meilleure qualité audio en haut, et on garde les 2 meilleurs
            audio_formats.sort(key=lambda x: int(x['quality'].split(' ')[0]), reverse=True)
            top_audios = audio_formats[:2]

            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'formats': formats,
                'audios': top_audios # On envoie les audios au HTML
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)