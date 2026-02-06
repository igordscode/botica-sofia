import requests
import json
import sys

def get_rates():
    try:
        # Usando uma API pública simples (pode ser trocada pela que você preferir)
        # Exemplo: AwesomeAPI (gratuita e não precisa de chave para cotações básicas)
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,BRL-PYG,USD-PYG"
        response = requests.get(url)
        data = response.json()
        
        # Extraindo as cotações
        brl_pyg = float(data['BRLPYG']['bid'])
        usd_pyg = float(data['USDPYG']['bid'])
        
        result = {
            "BRL_TO_PYG": brl_pyg,
            "USD_TO_PYG": usd_pyg,
            "INFO": "Para converter Real para Guarani, multiplique o valor em Real por este fator."
        }
        
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Erro ao buscar câmbio: {e}")

if __name__ == "__main__":
    get_rates()
