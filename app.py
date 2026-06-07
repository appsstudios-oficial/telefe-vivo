import requests
from flask import Flask, Response

app = Flask(__name__)

@app.route('/lista.m3u')
def obtener_lista():
    # Tu lista oficial de junio
    url_tu_lista = "https://raw.githubusercontent.com/appsstudios-oficial/listas2026/refs/heads/main/junio2026.m3u" 
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url_tu_lista, headers=headers)
        # Le entregamos el texto de la lista completo a tu TV o VLC
        return Response(response.text, mimetype='text/plain')
    except Exception as e:
        return f"Error al cargar la lista: {e}", 500

if __name__ == "__main__":
    app.run()
