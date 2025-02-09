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
    SELECT * FROM users WHERE email = %s;
"""

# fetch from db config table
FETCH_DB_CONFIG_DATA = """
    SELECT map_to FROM db_config WHERE map_from = %s; 
"""

# Insert OTP into DB
OTP_INSERT_QUERY = """
    INSERT INTO otp_verification (email, otp, expires_at) 
    VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL 5 MINUTE));
"""

# Fetch by email for OTP
FETCH_EMAIL_FOR_OTP = """
    SELECT * FROM otp_verification WHERE email = %s;
"""

# Update new OTP in DB
UPDATE_NEW_OTP = """
    UPDATE otp_verification 
    SET otp = %s, 
        expires_at = DATE_ADD(NOW(), INTERVAL 5 MINUTE),
        updated_at = NOW() 
    WHERE email = %s;
"""

# Update Password
UPDATE_PASSWORD_QUERY = """
    UPDATE users SET password = %s WHERE email = %s;
"""