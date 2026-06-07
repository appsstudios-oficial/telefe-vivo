import requests
import base64
from flask import Flask, Response, request

app = Flask(__name__)

URL_CIFRADA = b"aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2FwcHNzdHVkaW9zLW9maWNpYWwvbGlzdGFzMjAyNi9yZWZzL2hlYWRzL21haW4vanVuaW8yMDI2Lm0zdQ=="
CLAVE_ACCESO = "MiTele2026"

@app.route('/lista.m3u')
def obtener_lista():
    # 1. Validar clave secreta
    clave_recibida = request.args.get('clave')
    if clave_recibida != CLAVE_ACCESO:
        return "No encontrado", 404

    # 2. Leer quién pide la lista
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Si entran desde un navegador web de PC puro, los bloqueamos de una
    navegadores_web = ['chrome', 'edge', 'firefox', 'opera']
    
    # Si es un navegador web puro y NO viene de una app de IPTV conocida, bloqueamos
    if any(nav in user_agent for nav in navegadores_web) and not any(rep in user_agent for rep in ['vlc', 'smarters', 'iptv']):
        return "<h1>404 Not Found</h1>The server can not find the requested page.", 404

    try:
        # Para cualquier otro caso (VLC PC, VLC Celu, Smart TV), entregamos la lista
        url_real = base64.b64decode(URL_CIFRADA).decode('utf-8')
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_real, headers=headers)
        
        return Response(response.text, mimetype='text/plain')
    except Exception as e:
        return "Error interno", 500

if __name__ == "__main__":
    app.run()
