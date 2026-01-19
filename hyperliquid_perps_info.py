import requests

URL = "https://api.hyperliquid.xyz/info"

payload = {
    "type": "meta"
}

try:
    print("🔍 Conectando a Hyperliquid y leyendo PERPS...\n")

    r = requests.post(URL, json=payload, timeout=10)
    r.raise_for_status()

    data = r.json()

    universe = data.get("universe", [])

    if not universe:
        print("❌ No se encontró universe")
        exit(1)

    print(f"✅ Total de mercados encontrados: {len(universe)}\n")

    for market in universe:
        name = market.get("name")
        index = market.get("index")
        max_leverage = market.get("maxLeverage")
        sz_decimals = market.get("szDecimals")

        print(
            f"PERP: {name:<6} | "
            f"Index: {index:<3} | "
            f"MaxLev: {max_leverage:<3} | "
            f"SizeDecimals: {sz_decimals}"
        )

except Exception as e:
    print("❌ ERROR al obtener info de Hyperliquid:")
    print(e)
