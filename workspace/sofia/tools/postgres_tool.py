import sys
import os
import psycopg2
import json
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT")
    )

def registrar_evento(telefone, tipo, de_etapa=None, para_etapa=None, dados=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Busca ID do cliente pelo telefone
        cur.execute("SELECT id FROM clientes WHERE telefone = %s", (telefone,))
        res = cur.fetchone()
        if not res: return "ERRO: Cliente não encontrado."
        cliente_id = res[0]

        cur.execute("""
            INSERT INTO eventos_jornada (cliente_id, tipo_evento, de_etapa, para_etapa, meta_dados)
            VALUES (%s, %s, %s, %s, %s)
        """, (cliente_id, tipo, de_etapa, para_etapa, json.dumps(dados) if dados else None))
        conn.commit()
        return f"EVENTO_SUCCESS: {tipo} registrado."
    finally:
        cur.close()
        conn.close()

def upsert_cliente(telefone, nome, etapa="novo_contato", clickup_id=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        query = """
        INSERT INTO clientes (telefone, nome, funil_etapa, crm_clickup_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (telefone) 
        DO UPDATE SET 
            nome = COALESCE(EXCLUDED.nome, clientes.nome),
            funil_etapa = EXCLUDED.funil_etapa,
            crm_clickup_id = COALESCE(EXCLUDED.crm_clickup_id, clientes.crm_clickup_id),
            updated_at = CURRENT_TIMESTAMP
        RETURNING id;
        """
        cur.execute(query, (telefone, nome, etapa, clickup_id))
        cliente_id = cur.fetchone()[0]
        conn.commit()
        
        # Registra mudança de etapa automaticamente
        registrar_evento(telefone, "mudanca_etapa", para_etapa=etapa)
        
        return f"DB_SUCCESS: Cliente {telefone} atualizado."
    finally:
        cur.close()
        conn.close()

def salvar_receita(telefone, url):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM clientes WHERE telefone = %s", (telefone,))
        cliente_id = cur.fetchone()[0]
        cur.execute("INSERT INTO receitas (cliente_id, arquivo_url) VALUES (%s, %s)", (cliente_id, url))
        conn.commit()
        return "RECEITA_SUCCESS: Imagem salva no banco."
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    action = sys.argv[1]
    if action == "upsert":
        print(upsert_cliente(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "novo_contato"))
    elif action == "receita":
        print(salvar_receita(sys.argv[2], sys.argv[3]))
    elif action == "evento":
        print(registrar_evento(sys.argv[2], sys.argv[3], dados=json.loads(sys.argv[4]) if len(sys.argv) > 4 else None))
