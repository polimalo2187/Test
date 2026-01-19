import os
import requests
from eth_account import Account
from eth_account.messages import encode_defunct

# --------------------------
# Leer las variables de entorno del servidor
# --------------------------
WALLET_ADDRESS = os.getenv("HYPERLEAK_WALLET_ADDRESS")
PRIVATE_KEY = os.getenv("HYPERLEAK_WALLET_PRIVATE_KEY")

if not WALLET_ADDRESS or not PRIVATE_KEY:
    print("❌ ERROR: Las variables de entorno no están definidas correctamente")
    exit(1)

# --------------------------
# Endpoint REST Hyperleak
# --------------------------
URL = "https://api.hyperleak.io/v2/hyperliquid/getSymbolInfo"

# --------------------------
# Firma básica para autenticación
# --------------------------
message = encode_defunct(text=WALLET_ADDRESS)
signed_message = Account.sign_message(message, private_key=PRIVATE_KEY)
signature = signed_message.signature.hex()

headers = {
    "X-Wallet-Address": WALLET_ADDRESS,
    "X-Signature": signature
}

# --------------------------
# Request y listado de símbolos
# --------------------------
try:
    print("🔍 Probando conexión y listando símbolos de Hyperleak...")
    response = requests.get(URL, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()

    symbols = data.get("symbols", [])
    if not symbols:
        print("⚠️ No se encontraron símbolos")
    else:
        print(f"✅ Se encontraron {len(symbols)} símbolos:\n")
        for s in symbols:
            print(f"Symbol: {s.get('symbol')}, Base: {s.get('base')}, Quote: {s.get('quote')}, Status: {s.get('status')}")

except requests.exceptions.RequestException as e:
    print("❌ ERROR al conectar con Hyperleak:")
    print(e)
