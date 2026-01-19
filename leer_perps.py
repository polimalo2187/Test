import requests

def obtener_perps():
    url = "https://api.hyperleak.io/v2/hyperliquid/getSymbolInfo"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        perps = data.get("symbols", [])
        for p in perps:
            simbolo = p.get("symbol")
            precio = p.get("lastPrice")
            max_lev = p.get("maxLeverage", "N/A")
            size_decimals = p.get("sizeDecimals", "N/A")
            if precio is not None:
                print(f"PERP: {simbolo} | Precio: {precio} | MaxLev: {max_lev} | SizeDecimals: {size_decimals}")

    except requests.exceptions.RequestException as e:
        print(f"ERROR al conectar con Hyperliquid: {e}")

if __name__ == "__main__":
    print("Conectando a Hyperliquid y leyendo PERPS...")
    obtener_perps()
