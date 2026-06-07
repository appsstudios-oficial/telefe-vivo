import requests
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/telefe.m3u8')
def telefe():
    # API pública directa
    url_api = "https://telefe.com/api/v1/channels/telefe-interior/stream"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://telefe.com/'
    }
    try:
        response = requests.get(url_api, headers=headers)
        data = response.json()
        
        # Corrección de la lectura del JSON: Telefe devuelve una lista o un objeto directo
        if isinstance(data, list) and len(data) > 0:
            enlace_m3u8 = data[0].get('streamUrl') or data[0].get('stream_url')
        else:
            enlace_m3u8 = data.get('streamUrl') or data.get('stream_url')
            
        if not enlace_m3u8:
            return "No se pudo encontrar la URL del stream en la respuesta de Telefe", 500
            
        # Redireccionamos a VLC o la Smart TV
        return redirect(enlace_m3u8, code=302)
    except Exception as e:
        return f"Error interno en el servidor: {e}", 500

if __name__ == "__main__":
    app.run()
