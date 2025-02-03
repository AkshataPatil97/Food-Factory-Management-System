# User insert query
USER_INSERT_QUERY = """
    INSERT INTO users (username, email, password, role, is_delete)
    VALUES (%s, %s, %s, %s, %s);
"""

# fetch all user query
FETCH_ALL_USERS_QUERY = """ 
    SELECT * FROM users WHERE is_delete = false;
"""

# fetch user by email
FETCH_USER_BY_EMAIL = """ 
    SELECT * FROM  users WHERE email = %s;
"""
           