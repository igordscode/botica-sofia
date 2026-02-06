import sys
import json

# Configurações do Grupo
GROUP_ID = "120363406353899223@g.us"

def notify(etapa, nome, numero, resumo):
    # Limpa o número para o link (remove +, espaços, etc)
    clean_number = "".join(filter(str.isdigit, numero))
    
    # Monta a mensagem estruturada
    message = (
        f"*Notificação BoticAI - Lead Qualificado* ✅\n\n"
        f"*Etapa:* {etapa}\n"
        f"*Nome:* {nome}\n"
        f"*Resumo:* {resumo}\n\n"
        f"*Contato direto:* https://wa.me/{clean_number}"
    )
    
    payload = {
        "chatId": GROUP_ID,
        "text": message
    }
    
    # Saída para o OpenClaw
    print(f"NOTIFY_SUCCESS: Lead {nome} enviado para o grupo.")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Erro: Use: python3 notify_lead.py 'Etapa' 'Nome' 'Numero' 'Resumo'")
    else:
        # Pega os argumentos: etapa, nome, numero, resumo
        notify(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])