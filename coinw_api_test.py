import os
import time
import hashlib
import requests
import urllib.parse
from json.decoder import JSONDecodeError

API_KEY = os.getenv("COINW_API_KEY")
API_SECRET = os.getenv("COINW_API_SECRET")


def validar_api_coinw():
    if not API_KEY or not API_SECRET:
        print("❌ ERROR: Variables de entorno no configuradas")
        return

    base_url = "https://api.coinw.com"
    path = "/open/api/user/account"
    timestamp = str(int(time.time() * 1000))

    params = {
        "api_key": API_KEY,
        "timestamp": timestamp
    }

    # 1️⃣ Ordenar parámetros
    query_string = urllib.parse.urlencode(sorted(params.items()))

    # 2️⃣ Firma CoinW (MD5)
    sign_payload = f"{query_string}&secret_key={API_SECRET}"
    sign = hashlib.md5(sign_payload.encode("utf-8")).hexdigest().upper()

    # 3️⃣ URL final
    url = f"{base_url}{path}?{query_string}&sign={sign}"

    try:
        r = requests.get(url, timeout=10)

        try:
            data = r.json()
        except JSONDecodeError:
            print("❌ Respuesta NO JSON")
            print(r.text)
            return

        if r.status_code != 200:
            print("❌ HTTP ERROR:", r.status_code)
            print(data)
            return

        if data.get("code") != 0:
            print("❌ API ERROR")
            print(data)
            return

        print("✅ CONEXIÓN EXITOSA CON COINW")
        print(data)

    except Exception as e:
        print("❌ EXCEPCIÓN")
        print(str(e))


if __name__ == "__main__":
    print("🔍 Probando conexión API CoinW (SPOT)...")
    validar_api_coinw()
