import requests
import json
import sys

def get_rates():
    try:
        # Usando pares individuais para garantir que a API retorne as chaves certas
        # USD-BRL (Dolar/Real), BRL-PYG (Real/Guarani), USD-PYG (Dolar/Guarani)
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,BRL-PYG,USD-PYG"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # A AwesomeAPI retorna chaves como 'BRLPYG', 'USDBRL', etc.
        # Vamos usar .get() para evitar erros de chave inexistente
        rate_brl_pyg = data.get('BRLPYG', {}).get('bid')
        rate_usd_pyg = data.get('USDPYG', {}).get('bid')
        rate_usd_brl = data.get('USDBRL', {}).get('bid')
        
        if not rate_brl_pyg:
            # Fallback caso BRL-PYG falhe: calcular via USD
            # (USD/PYG) / (USD/BRL) = BRL/PYG
            if rate_usd_pyg and rate_usd_brl:
                rate_brl_pyg = float(rate_usd_pyg) / float(rate_usd_brl)
        
        result = {
            "BRL_TO_PYG": float(rate_brl_pyg) if rate_brl_pyg else "N/A",
            "USD_TO_PYG": float(rate_usd_pyg) if rate_usd_pyg else "N/A",
            "USD_TO_BRL": float(rate_usd_brl) if rate_usd_brl else "N/A",
            "INFO": "Cotações atualizadas via AwesomeAPI."
        }
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Erro ao buscar câmbio: {str(e)}")

if __name__ == "__main__":
    get_rates()