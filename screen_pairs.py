# ============================================================
# SCREEN DE PARES – Hyperliquid
# OBJETIVO: Probar conexión y leer todos los pares
# ============================================================

import time
from app.hyperliquid_client import make_request
from app.config import VERBOSE_LOGS, PRODUCTION_MODE

# ============================================================
# LOG SIMPLE
# ============================================================

def safe_log(*args):
    if VERBOSE_LOGS and not PRODUCTION_MODE:
        print(*args)
    else:
        print(*args)

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
