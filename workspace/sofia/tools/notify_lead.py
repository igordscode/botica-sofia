import sys
import os
import json

# Configurações do Grupo
GROUP_ID = "120363406353899223@g.us"

def notify(message):
    # Formata a mensagem para o padrão BoticAI
    payload = {
        "chatId": GROUP_ID,
        "text": f"*Notificação BoticAI - Novo Lead!* ✅

{message}"
    }
    
    # No OpenClaw, usamos o comando 'send' ou chamamos a API interna
    # Por enquanto, vamos apenas dar um print que o OpenClaw captura como saída da tool
    print(f"NOTIFY_SUCCESS: Mensagem enviada para o grupo {GROUP_ID}")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erro: Mensagem não fornecida.")
    else:
        notify(sys.argv[1])
