import os
import requests

# Variables de entorno
PRIVATE_KEY = os.getenv("HYPERLEAK_WALLET_PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("HYPERLEAK_WALLET_ADDRESS")

# Endpoint para pares (ejemplo, ajustar según Hyperleak)
PAIRS_ENDPOINT = "https://api.hyperleak.io/v1/markets"

def listar_pares():
    try:
        r = requests.get(PAIRS_ENDPOINT, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        pares = []
        for market in data.get("data", []):
            if market.get("status") == "active":
                pares.append(market.get("symbol"))
        
        print("✅ Pares activos encontrados:")
        for p in pares:
            print(p)
        
        return pares
    
    except Exception as e:
        print("❌ ERROR al conectar con Hyperleak:")
        print(str(e))
        return []

if __name__ == "__main__":
    print("🔍 Probando conexión y listando pares en Hyperleak...")
    listar_pares()
