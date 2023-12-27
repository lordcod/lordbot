data = {}

def get_table(table_name):
    if table_name not in data:
        data[table_name] = {}
    return data[table_name]

def get(table_name, key, *, default = None):
    table = get_table(table_name)
    if key not in table:
        return default
    
    return table[key]

def set(table_name, key, value):
    table = get_table(table_name)
    
    table[key] = value