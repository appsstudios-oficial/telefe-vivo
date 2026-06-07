import requests
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/telefe.m3u8')
def telefe():
    # Esta es la API oficial de Telefe que genera los enlaces como el tuyo
    url_api = "https://server.idp.telefe.com/get_live_stream?channel=telefe_interior"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        data = requests.get(url_api, headers=headers).json()
        enlace_m3u8 = data['stream_url']
        # Redirecciona a VLC o a tu Smart TV al enlace con el token nuevo en tiempo real
        return redirect(enlace_m3u8, code=302)
    except Exception as e:
       return f"Error: {e}", 500

if __name__ == "__main__":
    app.run()
