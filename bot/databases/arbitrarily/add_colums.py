from _executer import execute



execute(
    """
        ALTER TABLE roles
        ADD auto_roles JSON DEFAULT '{}'; 
    """
)
