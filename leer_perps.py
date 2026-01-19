import requests
from tabulate import tabulate

def obtener_perps_tabla():
    url = "https://api.hyperleak.io/v2/hyperliquid/getSymbolInfo"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        perps = data.get("symbols", [])
        filtered_perps = []

        for p in perps:
            simbolo = p.get("symbol")
            precio = p.get("lastPrice")
            max_lev = p.get("maxLeverage", "N/A")
            size_decimals = p.get("sizeDecimals", "N/A")
            
            if precio is not None:
                filtered_perps.append([simbolo, precio, max_lev, size_decimals])

        if filtered_perps:
            print(tabulate(filtered_perps, headers=["PERP", "Precio", "MaxLev", "SizeDecimals"], tablefmt="pretty"))
        else:
            print("No se encontraron PERPS con precio disponible.")

    except requests.exceptions.RequestException as e:
        print(f"ERROR al conectar con Hyperliquid: {e}")
    except Exception as e:
        print(f"ERROR inesperado: {e}")

if __name__ == "__main__":
    obtener_perps_tabla()
