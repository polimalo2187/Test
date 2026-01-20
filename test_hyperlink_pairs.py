#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_hyperlink_pairs.py
-----------------------
Test de prueba para conectarse al exchange Hyperlink (Hyperliquid) 
y listar solo los pares tipo Perpetual (contratos perpetuos).
"""

import requests
import json

# URL base del endpoint de Hyperlink / HyperETH
BASE_URL = "https://api.hypereth.io/v1/hl"
SYMBOLS_ENDPOINT = "/getSymbolInfo"  # Ajustar según la API final si cambia

def obtener_pares_perpetual():
    """
    Obtiene los pares tipo PERPETUAL desde Hyperlink y los imprime.
    """
    url = f"{BASE_URL}{SYMBOLS_ENDPOINT}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Error HTTP: {response.status_code}")
            return []
        
        data = response.json()
        # Filtramos solo los pares tipo PERPETUAL
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
