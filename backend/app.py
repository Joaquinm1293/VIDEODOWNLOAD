import os
import tempfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app) # Importante para que tu HTML pueda hablar con este servidor

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({"status": "error", "message": "No se proporcionó URL"}), 400

    # Usamos el directorio temporal del servidor en la nube
    tmp_dir = tempfile.gettempdir()
    
    try:
        # 'best' es más seguro para servidores gratis porque no siempre tienen FFmpeg para unir audio/video
        ydl_opts = {
            'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
            'format': 'best', 
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            # Obtenemos la ruta real del archivo descargado
            file_path = ydl.prepare_filename(info)

        # Enviamos el archivo físico al navegador del usuario
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Usar el puerto que la nube nos asigne
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)