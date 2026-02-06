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

def get_client(telefone):
    conn = get_connection()
    cur = conn.cursor()
    # Busca cliente pelo telefone
    cur.execute("""
        SELECT id, nome, cidade, funil_etapa, crm_clickup_id 
        FROM clientes WHERE telefone = %s
    """, (telefone,))
    client = cur.fetchone()
    cur.close()
    conn.close()
    
    if client:
        return {
            "id": client[0],
            "nome": client[1],
            "cidade": client[2],
            "etapa": client[3],
            "clickup_id": client[4],
            "exists": True
        }
    return {"exists": False}

def upsert_client(telefone, nome, etapa="novo_contato", clickup_id=None):
    conn = get_connection()
    cur = conn.cursor()
    
    # Insere ou Atualiza Cliente
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
    client_id = cur.fetchone()[0]
    
    # Registra o Evento na Jornada
    cur.execute("""
        INSERT INTO eventos_jornada (cliente_id, tipo_evento, para_etapa)
        VALUES (%s, 'mudanca_etapa', %s)
    """, (client_id, etapa))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"DB_SUCCESS: Cliente {telefone} salvo/atualizado na etapa {etapa}.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 postgres_tool.py get [telefone] ou upsert [telefone] [nome] [etapa] [clickup_id]")
    else:
        action = sys.argv[1]
        if action == "get":
            client = get_client(sys.argv[2])
            print(json.dumps(client))
        elif action == "upsert":
            # Args: telefone, nome, etapa, clickup_id
            tel = sys.argv[2]
            nome = sys.argv[3]
            etapa = sys.argv[4] if len(sys.argv) > 4 else "novo_contato"
            clickup_id = sys.argv[5] if len(sys.argv) > 5 else None
            upsert_client(tel, nome, etapa, clickup_id)