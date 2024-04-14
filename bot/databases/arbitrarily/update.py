from _executer import execute
import orjson

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

value = orjson.dumps([
    {"role_id": 1213860890395287653, "amount": 100, "name": "Green"},
    {"role_id": 1213860899300053003, "amount": 200, "limit": 5},
    {"role_id": 1213860908896624731, "amount": 300},
    {"role_id": 1213860917734023210, "amount": 400},
    {"role_id": 1213860926629879861, "amount": 500, "name": "Green + Blue"}
]).decode()
data = """
{
    "enabled": true,
    "channel_suggest_id": 1221062419800002630,
    "message_suggest_id": 1221070231167045783,
    "cooldown": 30,

    "channel_offers_id": 1221062432844152944,
    "channel_approved_id": 1221062447067037798,
    "thread_delete": true,
    "reaction_system": 1,
    "moderation_role_ids":[1179070749361840220]
}
"""
execute(
    """
            UPDATE 
                guilds 
            SET id = 1179069504186232852, ideas = %s
            WHERE 
                id = %s
        """,
    (data, guild_id, )
)
