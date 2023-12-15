import time
import jmespath

data = {}


class BucketType:
    member = 0
    server = 1


class CooldownGuild:
    def __init__(
        self, 
        command_name: str, 
        command_data: dict, 
        guild_id: int
    ) -> None:
        self.command_name = command_name
        self.command_data = command_data
        self.guild_id = guild_id
        
        self.check_register()
    
    def check_register(self) -> None:
        if self.guild_id not in data:
            data[self.guild_id] = {}
        if self.command_name not in data[self.guild_id]:
            data[self.guild_id][self.command_name] = {}
    
    def get(self) -> bool:
        cooldata: dict = data[self.guild_id][self.command_name] 
        
        regular_rate: int = self.command_data.get('rate')
        rate: int = cooldata.get('rate',0)
        per: float = cooldata.get('per',0)
        
        if time.time() >= per:
            print('reset')
            self.reset()
            return True
        
        if regular_rate > rate:
            return True
        return round(per-time.time())
    
    def add(self) -> None:
        global data
        
        cooldata: dict = data[self.guild_id][self.command_name] 
        rate: int = cooldata.get('rate',0)
        per: float = cooldata.get('per',0)
        
        regular_per: int = self.command_data.get('per')
        
        datatime = time.time()+regular_per if rate == 0 else per
        
        
        data[self.guild_id][self.command_name] = {
            'rate':rate+1,
            'per':datatime
        }
    
    def reset(self) -> None:
        data[self.guild_id][self.command_name] = {
            'rate':0,
            'per':0
        }

class CooldownMember:
    def __init__(self, command_name, command_data, guild_id, member_id) -> None:
        self.command_name = command_name
        self.command_data = command_data
        self.guild_id = guild_id
        self.member_id = member_id
    
    def get(self) -> bool:
        return True
    
    def add(self):
        pass
    
    def reset(self):
        pass


class Cooldown:
    def __init__(
        self, 
        command_name: str,
        command_data: dict, 
        guild_id: int,
        member_id: int
    ) -> None:
        self.command_name = command_name
        self.command_data = command_data
        self.guild_id = guild_id
        self.member_id = member_id
    
    def get_service(self):
        cooldata: dict = self.command_data
        type = cooldata.get('type')
        
        if type == BucketType.member:
            classification = CooldownMember(
                self.command_name,
                self.command_data,
                self.guild_id,
                self.member_id
            )
        elif type == BucketType.server:
            classification = CooldownGuild(
                self.command_name,
                self.command_data,
                self.guild_id
            )
        else:
            return None
        return classification
    
    def get(self):
        service = self.get_service()
        
        return service.get()
    
    def add(self):
        service = self.get_service()
        
        service.add()
    
    def reset(self):
        service = self.get_service()
        
        service.reset()

cd = Cooldown(
    'help',
    {
        'type': 1,
        'rate':2,
        'per':3
    },
    123,
    1203
)

print('get',cd.get())
cd.add()
print('get',cd.get())
cd.add()
print('get',cd.get())
cd.add()
print('get',cd.get())
time.sleep(4)
print('get',cd.get())
