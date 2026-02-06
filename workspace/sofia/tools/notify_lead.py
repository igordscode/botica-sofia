import sys
import json

# Configurações do Grupo
GROUP_ID = "120363406353899223@g.us"

def notify(etapa, nome, numero, resumo):
    # Garante que o número tenha o formato + Internacional para o WhatsApp linkar automático
    clean_number = "".join(filter(str.isdigit, numero))
    formatted_number = f"+{clean_number}"
    
    # Monta a mensagem estruturada (Estilo Nativo)
    message = (
        f"*Notificação BoticAI - {etapa}* ✅\n\n"
        f"*Nome:* {nome}\n"
        f"*Número:* {formatted_number}\n"
        f"*Resumo:* {resumo}"
    )
    
    payload = {
        "chatId": GROUP_ID,
        "text": message
    }
    
    # Saída para o OpenClaw
    print(f"NOTIFY_SUCCESS: Lead {nome} notificado no grupo.")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Erro: Use: python3 notify_lead.py 'Etapa' 'Nome' 'Numero' 'Resumo'")
    else:
        # Pega os argumentos: etapa, nome, numero, resumo
        notify(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
