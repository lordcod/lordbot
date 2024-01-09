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
# execute(
#         """
#             UPDATE 
#                 guilds 
#             SET 
#                 command_permissions = jsonb_set(command_permissions::jsonb, '{balance}', %s) 
#             WHERE 
#                 id = %s
#         """, 
#         (value, guild_id, )
# )

data = """
{
    "channel-suggest-id": 1189644187772129462,

    "channel-offers-id": 1189644228834381935,
    "channel-approved-id": 1189644276645240933,

    "moderation-role-ids":[1179070749361840220]
}
"""
execute(
        """
            UPDATE 
                guilds 
            SET 
                ideas = %s
            WHERE 
                id = %s
        """, 
        (data, guild_id, )
)