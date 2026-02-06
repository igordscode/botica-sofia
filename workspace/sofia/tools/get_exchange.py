import requests
import json
import sys

def get_rates():
    try:
        # Buscando os 3 principais pares
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,USD-PYG,BRL-PYG"
        response = requests.get(url, timeout=15)
        data = response.json()
        
        # Puxando os valores (bid)
        # Usamos float() direto aqui para garantir que são números
        try:
            usd_brl = float(data.get('USDBRL', {}).get('bid', 0))
            usd_pyg = float(data.get('USDPYG', {}).get('bid', 0))
            brl_pyg = float(data.get('BRLPYG', {}).get('bid', 0))
        except (ValueError, TypeError):
            usd_brl = usd_pyg = brl_pyg = 0

        # Lógica de Fallback (Se BRL-PYG direto estiver zerado ou N/A)
        if brl_pyg == 0 and usd_brl > 0 and usd_pyg > 0:
            brl_pyg = usd_pyg / usd_brl
            info_msg = "Calculado via Cross-Rate (USD)."
        elif brl_pyg > 0:
            info_msg = "Cotação direta via AwesomeAPI."
        else:
            info_msg = "Erro: Dados insuficientes na API."

        result = {
            "BRL_TO_PYG": round(brl_pyg, 2) if brl_pyg > 0 else "N/A",
            "USD_TO_PYG": round(usd_pyg, 2) if usd_pyg > 0 else "N/A",
            "USD_TO_BRL": round(usd_brl, 2) if usd_brl > 0 else "N/A",
            "INFO": info_msg
        }
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        # Se der erro grave, mostra o que aconteceu
        error_result = {
            "BRL_TO_PYG": "N/A",
            "ERROR": str(e),
            "INFO": "Falha na conexão com o serviço de câmbio."
        }
        print(json.dumps(error_result, indent=2))

if __name__ == "__main__":
    get_rates()
