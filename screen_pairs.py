# ============================================================
# SCREEN DE PARES – Hyperliquid (TEST PURO)
# OBJETIVO: Leer TODOS los pares perpetuos disponibles
# ============================================================

import requests

# ============================================================
# LOG SIMPLE
# ============================================================

def safe_log(*args):
    print(*args)

# ============================================================
# OBTENER TODOS LOS PARES
# ============================================================

def get_all_pairs():
    url = "https://api.hyperliquid.xyz/info"
    payload = {"type": "metaAndAssetCtxs"}

    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        response = r.json()
    except Exception as e:
        safe_log("❌ Error HTTP Hyperliquid:", e)
        return {}

    if not response or not isinstance(response, list) or len(response) != 2:
        safe_log("❌ Respuesta inválida de Hyperliquid")
        return {}

    meta, asset_ctxs = response
    pairs = {}

    for asset in asset_ctxs:
        symbol = asset.get("coin")
        if not symbol:
            continue

        price = float(asset.get("markPx") or 0)
        if price <= 0:
            continue

        pairs[f"{symbol}-PERP"] = {
            "price": price,
            "volume": float(asset.get("dayNtlVlm") or 0),
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
        safe_log(f"✅ Pares encontrados: {len(pairs)}\n")
        for symbol, data in pairs.items():
            safe_log(symbol, data)
