import requests
import json
import sys

def get_rates():
    try:
        # Tentando buscar os pares
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,USD-PYG,BRL-PYG"
        response = requests.get(url, timeout=15)
        
        if response.status_code != 200:
            print(json.dumps({"ERROR": f"API retornou status {response.status_code}", "INFO": "Falha na API"}, indent=2))
            return

        data = response.json()
        
        # DEBUG: Se você quiser ver o que está vindo, a Sofia pode ler isso
        # print(f"DEBUG_RAW_DATA: {data}") 

        # Pegando os valores com tratamento de erro
        usd_brl = float(data.get('USDBRL', {}).get('bid', 0))
        usd_pyg = float(data.get('USDPYG', {}).get('bid', 0))
        brl_pyg = float(data.get('BRLPYG', {}).get('bid', 0))

        # Lógica de Cross-Rate se necessário
        if brl_pyg == 0 and usd_brl > 0 and usd_pyg > 0:
            brl_pyg = usd_pyg / usd_brl
            info_msg = "Calculado via Cross-Rate (USD)."
        elif brl_pyg > 0:
            info_msg = "Cotação direta via AwesomeAPI."
        else:
            # Se chegamos aqui, vamos mostrar as chaves que a API enviou para entender o erro
            keys_found = list(data.keys())
            info_msg = f"Erro: Chaves não encontradas. API enviou: {keys_found}"

        result = {
            "BRL_TO_PYG": round(brl_pyg, 2) if brl_pyg > 0 else "N/A",
            "USD_TO_PYG": round(usd_pyg, 2) if usd_pyg > 0 else "N/A",
            "USD_TO_BRL": round(usd_brl, 2) if usd_brl > 0 else "N/A",
            "INFO": info_msg
        }
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({"ERROR": str(e), "INFO": "Erro crítico no script"}, indent=2))

if __name__ == "__main__":
    get_rates()