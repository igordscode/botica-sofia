# FERRAMENTAS DA SOFIA 🛠️

A Sofia tem acesso aos seguintes comandos via terminal (exec):

### 1. Notificar Lead
- **Comando:** `python3 workspace/sofia/tools/notify_lead.py "[RESUMO DO LEAD]"`
- **Quando usar:** Assim que receber uma receita ou um pedido claro de orçamento.
- **Exemplo:** `python3 workspace/sofia/tools/notify_lead.py "Cliente Igor (5511...) enviou receita de Eritromicina"`

### 2. Consultar Câmbio
- **Comando:** `python3 workspace/sofia/tools/get_exchange.py`
- **Quando usar:** Quando o cliente perguntar o preço em Reais ou Dólares, ou para converter Gs para outras moedas.
- **Retorno:** JSON com as taxas de conversão.

### 3. Gerenciar CRM (ClickUp)
- **Comando Criar Lead:** `python3 workspace/sofia/tools/clickup_tool.py create "[Nome]" "[Número]" "[Resumo]"`
- **Comando Mudar Status:** `python3 workspace/sofia/tools/clickup_tool.py status "[TASK_ID]" "[Novo Status]"`
- **Quando usar:** 
    - `create`: Quando o cliente for novo.
    - `status`: Quando o cliente avançar no funil (ex: enviou receita, pagou).
- **Nota:** Os status devem ser escritos exatamente como no ClickUp (ex: "receta recibida", "en producción").
