import sys
import os
import requests
import json
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

CLICKUP_TOKEN = os.getenv("CLICKUP_TOKEN")
LIST_ID = os.getenv("CLICKUP_LIST_ID")

def create_task(nome, numero, resumo):
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    
    headers = {
        "Authorization": CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": f"Lead: {nome}",
        "description": f"""Número: {numero}
Resumo: {resumo}""",
        "status": "nuevo contacto" # Status inicial padrão
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"CLICKUP_SUCCESS: Task criada. ID: {data['id']}")
    else:
        print(f"CLICKUP_ERROR: {response.status_code} - {response.text}")

def update_status(task_id, new_status):
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    
    headers = {
        "Authorization": CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    
    payload = {
        "status": new_status.lower()
    }
    
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"CLICKUP_SUCCESS: Status atualizado para {new_status}")
    else:
        print(f"CLICKUP_ERROR: {response.status_code} - {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python3 clickup_tool.py create 'Nome' 'Numero' 'Resumo'")
        print("  python3 clickup_tool.py status 'TASK_ID' 'Novo Status'")
    else:
        action = sys.argv[1]
        if action == "create":
            create_task(sys.argv[2], sys.argv[3], sys.argv[4])
        elif action == "status":
            update_status(sys.argv[2], sys.argv[3])
