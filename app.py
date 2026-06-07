import requests
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/telefe.m3u8')
def telefe():
    # Usamos la API alternativa pública que no bloquea a los servidores
    url_api = "https://telefe.com/api/v1/channels/telefe-interior/stream"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url_api, headers=headers)
        data = response.json()
        
        # Extraemos el enlace master m3u8 con el token fresco
        enlace_m3u8 = data['streamUrl']
        
        # Redireccionamos a VLC o la Smart TV
        return redirect(enlace_m3u8, code=302)
    except Exception as e:
        return f"Error al conectar con Telefe: {e}", 500

if __name__ == "__main__":
    app.run()
