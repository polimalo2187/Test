#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_hyperlink_signed_pairs.py
------------------------------
Test de prueba para conectarse al exchange Hyperlink usando
firma de wallet Ethereum para obtener pares tipo Perpetual.
"""

import os
import json
import requests
from eth_account import Account
from eth_account.messages import encode_defunct

# --- Configuración desde variables de entorno ---
WALLET_ADDRESS = os.getenv("HYPERLINK_WALLET_ADDRESS")
PRIVATE_KEY = os.getenv("HYPERLINK_PRIVATE_KEY")

if not WALLET_ADDRESS or not PRIVATE_KEY:
    raise ValueError("❌ Define HYPERLINK_WALLET_ADDRESS y HYPERLINK_PRIVATE_KEY en las variables del entorno.")

# URL base del Hyperlink / HyperETH
BASE_URL = "https://api.hypereth.io/v1/hl"
SYMBOLS_ENDPOINT = "/getSymbolInfo"  # Ajusta según la documentación oficial

def firmar_mensaje(message: str, private_key: str) -> str:
    """
    Firma un mensaje usando la clave privada de Ethereum.
    """
    msg = encode_defunct(text=message)
    signed_message = Account.sign_message(msg, private_key=private_key)
    return signed_message.signature.hex()

def obtener_pares_perpetual():
    """
    Obtiene los pares tipo PERPETUAL firmando la petición con la wallet.
    """
    # Payload que se envía al endpoint
    payload = {
        "wallet": WALLET_ADDRESS
    }

    # Convertimos payload a string JSON para firmar
    payload_str = json.dumps(payload, separators=(',', ':'))
    signature = firmar_mensaje(payload_str, PRIVATE_KEY)

    headers = {
        "X-Wallet-Address": WALLET_ADDRESS,
        "X-Wallet-Signature": signature,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}{SYMBOLS_ENDPOINT}"
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"❌ Error HTTP: {response.status_code}")
            print(response.text)
            return []

        data = response.json()
        # Filtramos solo pares tipo PERPETUAL
        pares_perpetual = [
            s for s in data.get("symbols", []) if s.get("type") == "PERPETUAL"
        ]

        print(f"✅ Se encontraron {len(pares_perpetual)} pares Perpetual:")
        for p in pares_perpetual:
            print(f" - {p['symbol']} (Base: {p['baseAsset']}, Quote: {p['quoteAsset']})")

        return pares_perpetual

    except Exception as e:
        print(f"❌ Excepción al conectar: {e}")
        return []

if __name__ == "__main__":
    obtener_pares_perpetual()
