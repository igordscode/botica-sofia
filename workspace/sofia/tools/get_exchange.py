import requests
import json
import os
import time

CACHE_FILE = "workspace/tools/exchange_cache.json"
CACHE_DURATION = 1800 # 30 minutos em segundos

def get_rates():
    # 1. Tentar ler do Cache primeiro
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
            # Se o cache tiver menos de 30 min, usa ele
            if time.time() - cache.get('timestamp', 0) < CACHE_DURATION:
                cache['INFO'] = "Valores recuperados do cache (API em espera)."
                print(json.dumps(cache, indent=2))
                return

    # 2. Se não tem cache ou expirou, chama a API
    try:
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,USD-PYG,BRL-PYG"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 429:
            # Se deu erro de limite, tenta usar o cache mesmo expirado
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, 'r') as f:
                    cache = json.load(f)
                    cache['INFO'] = "Limite da API atingido. Usando último valor salvo."
                    print(json.dumps(cache, indent=2))
            else:
                print(json.dumps({"ERROR": "Limite de cotações atingido e sem cache disponível.", "CODE": 429}, indent=2))
            return

        data = response.json()
        
        usd_brl = float(data.get('USDBRL', {}).get('bid', 0))
        usd_pyg = float(data.get('USDPYG', {}).get('bid', 0))
        brl_pyg = float(data.get('BRLPYG', {}).get('bid', 0))

        if brl_pyg == 0 and usd_brl > 0 and usd_pyg > 0:
            brl_pyg = usd_pyg / usd_brl

        result = {
            "BRL_TO_PYG": round(brl_pyg, 2),
            "USD_TO_PYG": round(usd_pyg, 2),
            "USD_TO_BRL": round(usd_brl, 2),
            "timestamp": time.time(),
            "INFO": "Cotação atualizada com sucesso."
        }
        
        # Salva no cache para a próxima vez
        with open(CACHE_FILE, 'w') as f:
            json.dump(result, f)
            
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({"ERROR": str(e), "INFO": "Erro na execução do script."}, indent=2))

if __name__ == "__main__":
    get_rates()
