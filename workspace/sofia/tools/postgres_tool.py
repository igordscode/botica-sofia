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

def get_client(numero):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome, departamento, crm_id FROM ao_clientes WHERE numero = %s", (numero,))
    client = cur.fetchone()
    cur.close()
    conn.close()
    
    if client:
        return {"nome": client[0], "departamento": client[1], "crm_id": client[2]}
    return None

def upsert_client(numero, nome, departamento, crm_id=None):
    conn = get_connection()
    cur = conn.cursor()
    query = """
    INSERT INTO ao_clientes (numero, nome, departamento, crm_id)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (numero) 
    DO UPDATE SET 
        nome = EXCLUDED.nome,
        departamento = EXCLUDED.departamento,
        crm_id = COALESCE(EXCLUDED.crm_id, ao_clientes.crm_id),
        updated_at = CURRENT_TIMESTAMP;
    """
    cur.execute(query, (numero, nome, departamento, crm_id))
    conn.commit()
    cur.close()
    conn.close()
    print(f"DB_SUCCESS: Cliente {numero} atualizado no banco.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 postgres_tool.py get [numero] ou upsert [numero] [nome] [depto] [crm_id]")
    else:
        action = sys.argv[1]
        if action == "get":
            client = get_client(sys.argv[2])
            print(json.dumps(client))
        elif action == "upsert":
            upsert_client(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else None)
