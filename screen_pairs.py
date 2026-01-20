# ============================================================
# SCREEN DE PARES – Hyperliquid (Test Independiente)
# OBJETIVO: Probar conexión y leer todos los pares
# ============================================================

import time
import httpx

# ============================================================
# CONFIG TEST – Variables de entorno del servidor
# ============================================================

# Nombre de variable en el servidor para la dirección de la wallet
WALLET_ENV_VAR = "USER_WALLET"

# Nombre de variable en el servidor para la private key
PRIVATE_KEY_ENV_VAR = "USER_PRIVATE_KEY"

# Logs simples para test
VERBOSE_LOGS = True
PRODUCTION_MODE = False

# Base URL Hyperliquid
HYPER_BASE_URL = "https://api.hyperliquid.xyz"
REQUEST_TIMEOUT = 10

# ============================================================
# LOG SIMPLE
# ============================================================

def safe_log(*args):
    if VERBOSE_LOGS and not PRODUCTION_MODE:
        print(*args)
    else:
        print(*args)

# ============================================================
# HTTP REQUEST
# ============================================================

def make_request(endpoint: str, payload: dict, timeout: float = None):
    if timeout is None:
        timeout = REQUEST_TIMEOUT
    try:
        with httpx.Client(timeout=timeout, headers={"Content-Type": "application/json"}) as client:
            r = client.post(f"{HYPER_BASE_URL}{endpoint}", json=payload)
            r.raise_for_status()
            data = r.json()
            return data
    except httpx.HTTPStatusError as e:
        safe_log(f"❌ HTTP error {e.response.status_code}: {e}")
    except Exception as e:
        safe_log(f"❌ Error desconocido en request {endpoint}: {e}")
    return {}

# ============================================================
# OBTENER TODOS LOS PARES
# ============================================================

def get_all_pairs():
    r = make_request("/info", {"type": "metaAndAssetCtxs"})
    if not r or not isinstance(r, list) or len(r) < 2:
        safe_log("❌ Respuesta inválida de Hyperliquid")
        return {}

    meta, asset_ctxs = r
    pairs = {}

    for asset in asset_ctxs:
        symbol = asset.get("coin")
        if not symbol:
            continue
        price = float(asset.get("markPx", 0) or 0)
        if price <= 0:
            continue
        pairs[f"{symbol}-PERP"] = {
            "price": price,
            "volume": float(asset.get("dayNtlVlm", 0) or 0)
        }

    return pairs

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    safe_log("🔹 Iniciando screen de pares Hyperliquid")
    pairs = get_all_pairs()
    if not pairs:
        safe_log("❌ No se encontraron pares")
    else:
        safe_log("✅ Pares encontrados:")
        for symbol, data in pairs.items():
            safe_log(symbol, data)
