import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
import os 
def conectar_snowflake():
    """Función para conectar a Snowflake"""
    conn = snowflake.connector.connect(
        user=os.environ['SNOWSQL_USER'],
        password=os.environ['SNOWSQL_PWD'],
        account=os.environ['SNOWSQL_ACCOUNT'],
        warehouse='COMPUTE_WH',
        database='SOURCE',
        schema='RAW'
    )
    return conn

def get_data_snowflake(conn):
    """Obtener los datos de la tabla 'subtedata'."""
    cur = conn.cursor()
    try:
        # Ejecutar una consulta para obtener los datos de la tabla 'subtedata'
        cur.execute("SELECT * FROM subtedata")

        # Obtener todos los registros de la tabla
        rows = cur.fetchall()

        # Obtener los nombres de las columnas
        columns = [desc[0] for desc in cur.description]

        # Retornar los datos obtenidos y los nombres de las columnas
        return rows, columns
    except Exception as e:
        print("Error al obtener los datos de la tabla 'subtedata':", e)
        return None, None
    finally:
        cur.close()

# Conectar a Snowflake
conn = conectar_snowflake()

# Obtener los datos de la tabla 'subtedata'
data, columns = get_data_snowflake(conn)

# Si se obtuvieron datos, crear un DataFrame de Pandas y guardarlos como CSV
if data and columns:
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('data_snow.csv', index=False)

# Cerrar la conexión
conn.close()
