# ============================================================
# SCREEN DE PARES – Hyperliquid (TEST AUTOCONTENIDO)
# OBJETIVO: Probar conexión y leer todos los pares
# ============================================================

import time
import httpx
import os

# ============================================================
# CONFIGURACIÓN
# ============================================================

VERBOSE_LOGS = True
PRODUCTION_MODE = False

HYPER_BASE_URL = "https://api.hyperliquid.xyz"
REQUEST_TIMEOUT = 10  # segundos

# ============================================================
# LOG SIMPLE
# ============================================================

def safe_log(*args):
    if VERBOSE_LOGS and not PRODUCTION_MODE:
        print(*args)
    else:
        print(*args)

# ============================================================
# REQUEST A HYPERLIQUID
# ============================================================

def make_request(endpoint: str, payload: dict, timeout: int = REQUEST_TIMEOUT):
    try:
        with httpx.Client(timeout=timeout, headers={"Content-Type": "application/json"}) as client:
            r = client.post(f"{HYPER_BASE_URL}{endpoint}", json=payload)
            r.raise_for_status()
            data = r.json()
            return data
    except httpx.HTTPStatusError as e:
        safe_log(f"❌ HTTP error: {e.response.status_code} {e.response.text}")
    except Exception as e:
        safe_log(f"❌ Error request {endpoint}:", e)
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
