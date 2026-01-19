import requests
import json

URL = "https://api.hyperliquid.xyz/info"

def leer_perps():
    payload = {
        "type": "meta"
    }

    response = requests.post(URL, json=payload, timeout=10)
    response.raise_for_status()

    data = response.json()

    universe = data.get("universe", [])

    print(f"\n✅ Total de PERPS encontrados: {len(universe)}\n")

    for market in universe:
        name = market.get("name")
        sz_decimals = market.get("szDecimals")
        max_lev = market.get("maxLeverage")

        print(f"{name:10} | sizeDecimals={sz_decimals} | maxLev={max_lev}")

if __name__ == "__main__":
    print("🔍 Conectando a Hyperliquid y leyendo PERPS...\n")
    leer_perps()
