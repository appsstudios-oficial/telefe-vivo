import requests
import base64
from flask import Flask, Response, request

app = Flask(__name__)

# URL de tu lista de junio cifrada
URL_CIFRADA = b"aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2FwcHNzdHVkaW9zLW9maWNpYWwvbGlzdGFzMjAyNi9yZWZzL2hlYWRzL21haW4vanVuaW8yMDI2Lm0zdQ=="
CLAVE_ACCESO = "MiTele2026"

@app.route('/lista.m3u')
def obtener_lista():
    # 1. Validar clave secreta
    clave_recibida = request.args.get('clave')
    if clave_recibida != CLAVE_ACCESO:
        return "No encontrado", 404

    # 2. Leer firma del dispositivo/app
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Lista ampliada de reproductores permitidos (Smart TV, Celular y VLC)
    permitidos = [
        'vlc', 'iptv', 'smarters', 'xciptv', 'ott', 'player', 
        'smarttv', 'tivi', 'mxplayer', 'core', 'lavf', 'http-client'
    ]
    
    # Navegadores web comunes a bloquear
    navegadores = ['chrome', 'safari', 'edge', 'opera', 'firefox']

    # Si la app se identifica como uno de los reproductores permitidos, pasa directo
    es_reproductor = any(rep in user_agent for rep in permitidos)
    
    # Si tiene pinta de navegador de PC/Celular y NO está en los permitidos, se bloquea
    es_navegador_puro = any(nav in user_agent for nav in navegadores) and not es_reproductor

    if es_navegador_puro:
        # Engañamos al intruso con un error 404 falso
        return "<h1>404 Not Found</h1>The server can not find the requested page.", 404

    try:
        # Si pasó los filtros, el servidor Render procesa tu lista original
        url_real = base64.b64decode(URL_CIFRADA).decode('utf-8')
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_real, headers=headers)
        
        return Response(response.text, mimetype='text/plain')
    except Exception as e:
        return "Error interno", 500

if __name__ == "__main__":
    app.run()
