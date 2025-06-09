import psycopg2
from psycopg2.extensions import connection as PGConnection

def get_connection() -> PGConnection:
    return psycopg2.connect(
        dbname="sql_mystery",
        user="tui",
        password="504",
        host="10.61.49.169",
        port="3389"
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
    with conn.cursor() as cur:
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s;
        """, (schema, table_name))
        colunas = [row[0] for row in cur.fetchall()]
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
        if cur.rowcount != 0:
            conn.commit()

        return cur.rowcount


def insert(table_name, dicio, schema='public'):
    """
    Insere um novo registro em uma tabela, com base nos dados fornecidos via dicionário.

    Args:
        nome_tabela (str): Nome da tabela de destino.
        dicio (dict): Dicionário contendo os dados a serem inseridos (chaves = colunas).
        schema (str): Nome do schema da tabela (padrão: 'public').
    """
    conn = get_connection()
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
    conn.close()


def update(table_name, id, column_name, value, schema='public'):
    """
    Atualiza uma linha na tabela especificada com os valores fornecidos.

    Parâmetros:
    - table_name (str): nome da tabela onde a atualização será feita.
    - id: valor da chave primária para identificar a linha a ser atualizada.
    - column_name(str): Nome da coluna a ser editada
    - value: Novo valor a ser atribuído
    - schema (str): esquema do banco de dados, padrão é 'public'.
    """
    conn = get_connection()
    colunas = get_columns(table_name=table_name)
    id_column_name = colunas[0]

    query = f"UPDATE {schema}.{table_name} SET {column_name} = %s WHERE {id_column_name} = %s;"
    valores = list(value) + [id]

    with conn.cursor() as cur:
        cur.execute(query, valores)
        conn.commit()
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

    conn.close()
    return tables_info


def select(query: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)

            return cur.fetchall()


def delete_2(table_name, dicio, schema='public'):
    """
    Remove uma linha da tabela especificada com base em uma correspondência exata de valores.

    Parâmetros:
    - table_name (str): Nome da tabela no banco de dados.
    - dicio (dict): Dicionário contendo os pares coluna:valor que identificam exatamente a linha a ser excluída.
    - schema (str, opcional): Nome do schema onde está a tabela (padrão é 'public').

    Comportamento:
    - A função monta dinamicamente uma cláusula WHERE usando apenas as colunas presentes em `dicio`
      e de fato existentes na tabela.
    - O DELETE só será executado se todos os valores no dicionário coincidirem com uma linha da tabela.
    - Usado principalmente para garantir que apenas a linha completamente correspondente seja excluída.

    Exemplo:
        delete_2('users', {'id': 3, 'name': 'João', 'email': 'joao@email.com'})
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    colunas = get_columns(table_name=table_name)
    campos = []
    valores = []
    
    for coluna in colunas:
        if coluna in dicio:
            campos.append(coluna)
            valores.append(dicio[coluna])

    where_clause = ' AND '.join([f"{col} = %s" for col in campos])
    query = f"DELETE FROM {schema}.{table_name} WHERE {where_clause};"
    
    cursor.execute(query, valores)
    conn.commit()
    cursor.close()
    conn.close()


def create_index(table_name, column_names, index_name=None, unique=False, schema='public'):
    """
    Cria um índice em uma ou mais colunas de uma tabela.

    Parâmetros:
    - table_name (str): Nome da tabela onde o índice será criado.
    - column_names (list[str]): Lista com os nomes das colunas que farão parte do índice.
    - index_name (str, opcional): Nome do índice. Se não for fornecido, será gerado automaticamente.
    - unique (bool, opcional): Se True, cria um índice UNIQUE. Padrão é False.
    - schema (str, opcional): Nome do schema da tabela. Padrão é 'public'.

    Exemplo:
        create_index('users', ['email'], unique=True)
        → cria um índice único na coluna "email" da tabela "users"
    """

    if index_name is None:
        index_name = f"{table_name}_{'_'.join(column_names)}_idx"

    cols_str = ', '.join(column_names)
    unique_str = 'UNIQUE' if unique else ''
    
    query = f"""
        CREATE {unique_str} INDEX IF NOT EXISTS {index_name}
        ON {schema}.{table_name} ({cols_str});
    """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    print(get_info().keys())