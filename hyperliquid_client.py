# ============================================================
# HYPERLIQUID CLIENT – Conexión segura y blindada
# ============================================================

import time
import httpx
from eth_account import Account
from eth_account.messages import encode_structured_data
from config import HYPER_BASE_URL, REQUEST_TIMEOUT, VERBOSE_LOGS, PRODUCTION_MODE

# ============================================================
# LOG CONTROLADO
# ============================================================
def safe_log(*args):
    if VERBOSE_LOGS or not PRODUCTION_MODE:
        print(*args)

# ============================================================
# HTTP REQUEST CON REINTENTOS
# ============================================================
def make_request(endpoint: str, payload: dict, retries: int = 4, backoff: float = 1.0, timeout: float = None):
    if timeout is None:
        timeout = REQUEST_TIMEOUT

    for attempt in range(1, retries + 1):
        try:
            with httpx.Client(timeout=timeout, headers={"Content-Type": "application/json"}) as client:
                r = client.post(f"{HYPER_BASE_URL}{endpoint}", json=payload)
                r.raise_for_status()
                data = r.json()

                if isinstance(data, (dict, list)):
                    return data
                raise ValueError("Respuesta JSON inválida")

        except (httpx.RequestError, httpx.HTTPStatusError, ValueError) as e:
            safe_log(f"❌ HTTP error [{attempt}/{retries}] {endpoint}:", e)
        except Exception as e:
            safe_log(f"❌ Unknown error [{attempt}/{retries}] {endpoint}:", e)

        if attempt < retries:
            time.sleep(backoff * attempt)

    return {}
