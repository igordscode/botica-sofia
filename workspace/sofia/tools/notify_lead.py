import sys
import json

# Dicionário de Grupos (Funil de Vendas)
# Adicione os IDs reais conforme você for criando os grupos
GRUPOS = {
    "NOVO_LEAD": "120363406353899223@g.us", # Grupo Geral de Leads
    "EM_ATENDIMENTO": "ID_DO_GRUPO_ATENDIMENTO@g.us",
    "QUALIFICADO": "ID_DO_GRUPO_QUALIFICADO@g.us",
    "ORCAMENTO": "ID_DO_GRUPO_ORCAMENTOS@g.us", # Receitas e Presupostos
}

def notify(etapa_slug, nome, numero, resumo):
    # Seleciona o grupo. Se não achar o slug, envia para o geral (NOVO_LEAD)
    group_id = GRUPOS.get(etapa_slug, GRUPOS["NOVO_LEAD"])
    
    # Formatação do número para link nativo
    clean_number = "".join(filter(str.isdigit, numero))
    formatted_number = f"+{clean_number}"
    
    # Nome amigável da etapa para o cabeçalho
    etapa_nome = etapa_slug.replace("_", " ").title()
    
    message = (
        f"*Notificação BoticAI - {etapa_nome}* ✅\n\n"
        f"*Nome:* {nome}\n"
        f"*Número:* {formatted_number}\n"
        f"*Resumo:* {resumo}"
    )
    
    payload = {
        "chatId": group_id,
        "text": message
    }
    
    print(f"NOTIFY_SUCCESS: Lead enviado para o grupo {etapa_slug} ({group_id})")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Erro: Use: python3 notify_lead.py 'ETAPA_SLUG' 'Nome' 'Numero' 'Resumo'")
    else:
        notify(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])