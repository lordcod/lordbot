from _executer import execute



guild_id = 1179069504186232852
value = """
    {
        "operate": 1,
        "distribution":{
            "cooldown":{
                "type":1,
                "rate":2,
                "per":30
            }
        }
    }
"""
execute(
        """
            UPDATE 
                guilds 
            SET 
                command_permissions = jsonb_set(command_permissions::jsonb, '{balance}', %s) 
            WHERE 
                id = %s
        """, 
        (value, guild_id, )
)