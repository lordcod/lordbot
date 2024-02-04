from _executer import execute

execute(
    """
        ALTER TABLE guilds
        RENAME COLUMN disabled_commands TO command_permissions;
    """
)
