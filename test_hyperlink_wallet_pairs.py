#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_hyperlink_wallet_pairs.py
-----------------------------
Test de prueba para conectarse al exchange Hyperlink usando
la dirección de wallet y la clave privada, y listar pares tipo Perpetual.
"""

import os
import requests
import json

# --- Configuración desde variables de entorno ---
WALLET_ADDRESS = os.getenv("HYPERLINK_WALLET_ADDRESS")
PRIVATE_KEY = os.getenv("HYPERLINK_PRIVATE_KEY")

if not WALLET_ADDRESS or not PRIVATE_KEY:
    raise ValueError("❌ Por favor define HYPERLINK_WALLET_ADDRESS y HYPERLINK_PRIVATE_KEY en las variables del entorno.")

# URL base del Hyperlink / HyperETH
BASE_URL = "https://api.hypereth.io/v1/hl"
SYMBOLS_ENDPOINT = "/getSymbolInfo"  # Ajustar según la documentación

def firmar_peticion(payload: dict, private_key: str) -> str:
    """
    Función de ejemplo para firmar una petición con la clave privada.
    La implementación exacta depende de la documentación de Hyperlink.
    Aquí solo devolvemos un placeholder.
    """
    # TODO: reemplazar con la firma real según Hyperlink
    return "SIGNATURE_PLACEHOLDER"

def obtener_pares_perpetual():
    """
    Obtiene los pares tipo PERPETUAL firmando la petición con la wallet.
    """
    payload = {
        "wallet": WALLET_ADDRESS
    }
    signature = firmar_peticion(payload, PRIVATE_KEY)

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
        # Filtramos solo pares PERPETUAL
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
