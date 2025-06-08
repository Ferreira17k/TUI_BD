import psycopg2
from psycopg2.extensions import connection as PGConnection

def get_connection() -> PGConnection:
    return psycopg2.connect(
        dbname="sql_mystery",
        user="tui",
        password="504",
        host="10.61.49.169",
        port="5432"
    )


def get_columns(table_name: str, schema: str = 'public'):
    """
    Retorna a lista de nomes das colunas de uma tabela específica do schema informado.

    Args:
        nome_tabela (str): Nome da tabela.
        schema (str): Nome do schema (padrão: 'public').

    Returns:
        List[str]: Lista com os nomes das colunas da tabela.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s;
            """, (schema, table_name))
            colunas = [row[0] for row in cur.fetchall()]
    finally:
        conn.close()
    
    return colunas


def delete(table_name, id, schema='public'):
    conn = get_connection()
    colunas = get_columns(table_name=table_name)
    id_column_name = colunas[0]
    valores = [id]
    query = f"DELETE FROM {schema}.{table_name} WHERE {id_column_name} = %s;"

    with conn.cursor() as cur:
        cur.execute(query, valores)
        if cur.rowcount == 0:
            print(f"Nenhuma linha foi deletada. ID {id} não foi encontrado.")
        else:
            conn.commit()
            print(f"{cur.rowcount} linha(s) deletada(s) com sucesso.")


def insert(table_name, dicio, schema='public'):
    """
    Insere um novo registro em uma tabela, com base nos dados fornecidos via dicionário.

    Args:
        nome_tabela (str): Nome da tabela de destino.
        dicio (dict): Dicionário contendo os dados a serem inseridos (chaves = colunas).
        schema (str): Nome do schema da tabela (padrão: 'public').
    """
    conn = get_connection()
    try:
        colunas = get_columns(table_name=table_name, schema=schema)

        # Prepara os campos e valores a inserir com base nas colunas existentes
        campos = []
        valores = []
        for coluna in colunas:
            if coluna in dicio:
                campos.append(coluna)
                valores.append(dicio[coluna])

        placeholders = ', '.join(['%s'] * len(campos))
        campos_str = ', '.join(campos)
        query = f"INSERT INTO {schema}.{table_name} ({campos_str}) VALUES ({placeholders});"

        # Executa a inserção
        with conn.cursor() as cur:
            cur.execute(query, valores)
            conn.commit()
            print("Inserção realizada com sucesso.")
    except Exception as e:
        print("Erro ao inserir:", e)
    finally:
        conn.close()


def update(table_name, id, values_dicio, schema='public'):
    """
    Atualiza uma linha na tabela especificada com os valores fornecidos.

    Parâmetros:
    - table_name (str): nome da tabela onde a atualização será feita.
    - id: valor da chave primária para identificar a linha a ser atualizada.
    - values_dicio (dict): dicionário com colunas que serão alteradas como chaves e novos valores como valores.
    - schema (str): esquema do banco de dados, padrão é 'public'.

    Retorna:
    - None. Imprime mensagens de sucesso ou erro.
    """
    conn = get_connection()
    try:
        # Obtém os nomes das colunas da tabela
        colunas = get_columns(table_name=table_name)
        id_column_name = colunas[0]

        set_clause = ", ".join([f"{col} = %s" for col in values_dicio.keys()])
        query = f"UPDATE {schema}.{table_name} SET {set_clause} WHERE {id_column_name} = %s;"

        valores = list(values_dicio.values()) + [id]

        with conn.cursor() as cur:
            cur.execute(query, valores)

            if cur.rowcount == 0:
                print(f"Nenhuma linha atualizada. ID {id} não encontrado.")
            else:
                conn.commit()
                print(f"{cur.rowcount} linha(s) atualizada(s) com sucesso.")

    except Exception as e:
        print("Erro ao atualizar:", e)
    finally:
        conn.close()


def get_info(schema='public'):
    """
    Retorna um dicionário com as tabelas do schema e suas colunas.
    Cada chave é o nome da tabela, e o valor é uma lista de tuplas contendo:
    (nome_coluna, tipo_coluna, booleano_opcional)

    Parâmetros:
    - schema (str): nome do schema no banco, padrão 'public'

    Retorna:
    - dict[str, list[tuple(str, str, bool)]]
    """
    conn = get_connection()
    tables_info = {}

    query = """
    SELECT
        table_name,
        column_name,
        data_type,
        is_nullable
    FROM information_schema.columns
    WHERE table_schema = %s
    ORDER BY table_name, ordinal_position;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(query, (schema,))
            rows = cur.fetchall()

            for table_name, column_name, data_type, is_nullable in rows:
                # Cria a lista para a tabela se não existir
                if table_name not in tables_info:
                    tables_info[table_name] = []

                # Converte is_nullable para booleano
                optional = (is_nullable == 'YES')

                # Adiciona a tupla na lista da tabela
                tables_info[table_name].append((column_name, data_type, optional))

        return tables_info

    except Exception as e:
        print("Erro ao buscar informações das tabelas:", e)
        return {}

    finally:
        conn.close()


# Exemplo de uso:
dicio = {
    'idexperience': 30,
    'name': "cachorro feliz",
    'experiencetype': "animal",
    'description': "Um cachorro muito feliz",
    'siteaddress': "Não",
    'phonenumber': "21234",
    'email': "blablabla@email.com",
}



table_name = 'experience'

# insert(table_name='experience', dicio=dicio, schema='public')

values_dicio = {
    'name': "GAGAGAGAGGAGAGA",
    'description': "Um cachorro muito feliz@ED",
}

# update(table_name, 30, values_dicio)
# delete(table_name=table_name, id=30)

if __name__ == "__main__":
    print(get_info())
