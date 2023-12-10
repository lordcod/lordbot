from typing import Any,Dict,Union
import ujson as json
from psycopg2.extensions import connection

class Json:
    def loads(data):
        try:
            data = json.loads(data)
            return data
        except:
            return data
    
    def dumps(data):
        try:
            data = json.dumps(data)
            return data
        except Exception as err:
            return data

class Formating:
    def on_error(func):
        def wrapped(data: Dict[Any,Any]):
            try:
                result = func(data)
                return result
            except:
                return data
        return wrapped
    
    @on_error
    def loads(data: Dict[str,Any]):
        new_data = {}
        for key in data:
            value = data[key]
            if key.isdigit:
                new_data[int(key)] = value
            else:
                new_data[key] = value
        return new_data
    
    @on_error
    def dumps(data: Dict[Union[str,int],Any]):
        new_data = {}
        for key in data:
            
            if type(key) == int:
                new_data[str(key)] = data[key]
            else:
                new_data[key] = data[key]
        return new_data

def register_table(table_name: str, variable: str, connection: connection):
    with connection.cursor() as cursor:
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({variable})"
        )

def get_info_colums(table_name: str, connection: connection):
    query = """
        SELECT
            column_name,
            ordinal_position,
            data_type,
            column_default
        FROM
            information_schema.columns
        WHERE
            table_name = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (table_name,))
        
        info = cursor.fetchall()
        
        if not info:
            return None
        
        return list(info)
