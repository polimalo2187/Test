import requests

URL = "https://api.hyperliquid.xyz/info"

payload = {
    "type": "meta"
}

def safe(v):
    return v if v is not None else "N/A"

try:
    print("🔍 Conectando a Hyperliquid y leyendo PERPS...\n")

    r = requests.post(URL, json=payload, timeout=10)
    r.raise_for_status()

    data = r.json()
    universe = data.get("universe", [])

    print(f"✅ Total de mercados encontrados: {len(universe)}\n")

    for market in universe:
        name = safe(market.get("name"))
        index = safe(market.get("index"))
        max_leverage = safe(market.get("maxLeverage"))
        sz_decimals = safe(market.get("szDecimals"))

        print(
            f"PERP: {name} | "
            f"Index: {index} | "
            f"MaxLev: {max_leverage} | "
            f"SizeDecimals: {sz_decimals}"
        )

except Exception as e:
    print("❌ ERROR al obtener info de Hyperliquid:")
    print(e)
