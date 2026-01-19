import os
import time
import hmac
import hashlib
import requests
import urllib.parse
from json.decoder import JSONDecodeError

"""
Script independiente para validar conexión API CoinW (SPOT)
Lee API_KEY y API_SECRET desde variables de entorno
"""

API_KEY = os.getenv("COINW_API_KEY")
API_SECRET = os.getenv("COINW_API_SECRET")


def validar_api_coinw():
    if not API_KEY or not API_SECRET:
        print("❌ ERROR: Variables de entorno no configuradas")
        print("Debe definir COINW_API_KEY y COINW_API_SECRET")
        return

    base_url = "https://api.coinw.com"
    path = "/open/api/user/account"
    method = "GET"

    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"

    params = {
        "api_key": API_KEY,
        "timestamp": timestamp,
        "recvWindow": recv_window
    }

    # 1️⃣ Ordenar parámetros
    query_string = urllib.parse.urlencode(sorted(params.items()))

    # 2️⃣ Payload para firma
    sign_payload = f"{method}{path}?{query_string}"

    # 3️⃣ Firma HMAC SHA256
    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        sign_payload.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    # 4️⃣ URL final
    url = f"{base_url}{path}?{query_string}&sign={signature}"

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        try:
            data = response.json()
        except JSONDecodeError:
            print("❌ Respuesta NO JSON")
            print(response.text)
            return

        if response.status_code != 200:
            print("❌ HTTP ERROR:", response.status_code)
            print(data)
            return

        if data.get("code") != 0:
            print("❌ API ERROR")
            print("Mensaje:", data.get("msg"))
            print("Respuesta completa:", data)
            return

        print("✅ CONEXIÓN EXITOSA CON COINW")
        print("Respuesta:")
        print(data)

    except Exception as e:
        print("❌ EXCEPCIÓN")
        print(str(e))


if __name__ == "__main__":
    print("🔍 Probando conexión API CoinW (SPOT)...")
    validar_api_coinw()
