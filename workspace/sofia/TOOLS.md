# MANUAL DE FERRAMENTAS DA SOFIA 🛠️

Você tem as seguintes ferramentas de terminal à sua disposição. Use-as sempre para manter o sistema atualizado.

### 1. BANCO DE DADOS (PostgreSQL)
- **Upsert Cliente:** `python3 tools/postgres_tool.py upsert "[Telefone]" "[Nome]" "[Etapa]"`
  - Use sempre no primeiro contato para registrar o lead.
- **Salvar Receita:** `python3 tools/postgres_tool.py receita "[Telefone]" "[URL_DA_IMAGEM]"`
  - Use assim que o cliente mandar a foto da receita.
- **Registrar Evento:** `python3 tools/postgres_tool.py evento "[Telefone]" "[Tipo]" "[JSON_DADOS]"`
  - Use para B.I. (Ex: tipo='orcamento_enviado', dados='{"valor": 150000}').

### 2. CRM (ClickUp)
- **Criar Task:** `python3 tools/clickup_tool.py create "[Nome]" "[Telefone]" "[Resumo]"`
- **Mudar Status:** `python3 tools/clickup_tool.py status "[TASK_ID]" "[Novo Status]"`
  - Status válidos: "nuevo contacto", "triage (ia)", "receta recibida", "en producción".

### 3. CÂMBIO
- **Consultar:** `python3 tools/get_exchange.py`
  - Retorna cotações Real/Guarani/Dólar com cache de segurança.

### 4. NOTIFICAÇÕES (WhatsApp)
- **Avisar Grupo:** `python3 tools/notify_lead.py "[ETAPA]" "[Nome]" "[Telefone]" "[Resumo]"`