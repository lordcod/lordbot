from typing import Any,Dict,Union
import ujson as json
from bot.misc.logger import Logger
from .load import load_db


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
        except:
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

