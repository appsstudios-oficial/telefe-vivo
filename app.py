import requests
import base64
from flask import Flask, Response, request

app = Flask(__name__)

# URL de junio cifrada
URL_CIFRADA = b"aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2FwcHNzdHVkaW9zLW9maWNpYWwvbGlzdGFzMjAyNi9yZWZzL2hlYWRzL21haW4vanVuaW8yMDI2Lm0zdQ=="
CLAVE_ACCESO = "MiTele2026"

@app.route('/lista.m3u')
def obtener_lista():
    # 1. Validar clave
    clave_recibida = request.args.get('clave')
    if clave_recibida != CLAVE_ACCESO:
        return "No encontrado", 404

    # 2. Validar quién espía (User-Agent)
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Lista de palabras comunes en navegadores web
    navegadores = ['mozilla', 'chrome', 'safari', 'edge', 'opera', 'android', 'iphone']
    
    # Excepciones: Permitir VLC o reproductores de TV aunque tengan la palabra Mozilla
    permitidos = ['vlc', 'iptv', 'ott', 'smarters', 'player', 'smarttv', 'tivi']

    # Si parece un navegador y NO es un reproductor permitido, lo bloqueamos
    es_navegador = any(nav in user_agent for nav in navegadores)
    es_reproductor = any(rep in user_agent for rep in permitidos)

    if es_navegador and not es_reproductor:
        # Le mentimos al navegador diciendo que la página no existe
        return "<h1>404 Not Found</h1>The server can not find the requested page.", 404

    try:
        # Si pasó los filtros (es VLC o la TV), le damos la lista original
        url_real = base64.b64decode(URL_CIFRADA).decode('utf-8')
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_real, headers=headers)
        
        return Response(response.text, mimetype='text/plain')
    except Exception as e:
        return "Error interno", 500

if __name__ == "__main__":
    app.run()
