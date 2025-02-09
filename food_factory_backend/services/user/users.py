from constants.queries import USER_INSERT_QUERY, FETCH_ALL_USERS_QUERY ,FETCH_USER_BY_EMAIL, OTP_INSERT_QUERY, FETCH_EMAIL_FOR_OTP, UPDATE_NEW_OTP, UPDATE_PASSWORD_QUERY
from constants.constant import TRUE
from constants.bd_config import EMAIL_SEND_TO_USER
from services.sendemail.sendemail import send_email
from services.passwordencrypt.passwordencrypt import encrypt_password
from services.db_config.dbConfigService import fetch_db_config_data
from django.utils.crypto import get_random_string
from datetime import datetime

def insert_user(db_connection, data):
    """ Insert a new user into the database.
    Args:
        db_connection: The active database connection.
        data (dict): A dictionary containing user data.
            Required keys: 'username', 'email', 'password', 'role', 'is_delete'.
    Returns:
        bool: True if the user was successfully inserted, False otherwise."""

    try:
        cursor = db_connection.cursor()
        cursor.execute(USER_INSERT_QUERY, (
            data.get('username'),
            data.get('email'),
            encrypt_password(data.get('password')),
            data.get('role'),
            data.get('is_delete', 0)  
        ))
        isEmailSend = fetch_db_config_data(db_connection, EMAIL_SEND_TO_USER)
        if isEmailSend == TRUE:
            isSend = send_email_to_user(data.get('email'))
            if isSend:
                db_connection.commit()
                return True
            else:
                return False
        else:
            db_connection.commit()
            return True

        
    except Exception as e:
        if e.args[0] == 1062:
            print("Duplicate email detected")
            return "email already exists"
        else:
            print(f"Error inserting user: {str(e)}")
            return False
    finally:
        cursor.close()


def fetchall_users(db_connection):
    try:
        cursor = db_connection.cursor()
        cursor.execute(FETCH_ALL_USERS_QUERY)
        data = cursor.fetchall()
        db_connection.commit()
        return data
    except Exception as e:
        print(f"Error fetching users: {str(e)}")
        return e
    finally:
        cursor.close()

def fetch_user_by_email(db_connection, email):
    try:
        cursor = db_connection.cursor(dictionary=True)  
        cursor.execute(FETCH_USER_BY_EMAIL, (email,))
        user = cursor.fetchone() 
        return user  
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        cursor.close()

def send_email_to_user(email):
    try:
        subject = "Welcome to Our Platform"
        message = "Thank you for registering with us!"
        recipient_list = [email]  

        send_email(subject, message, recipient_list)
        return True

    except Exception as e:
        print(f"Error fetching user: {e}")
        return False

def send_otp_email(db_connection, email):
    try:
        isEmailSend = fetch_db_config_data(db_connection, EMAIL_SEND_TO_USER)
        if isEmailSend == TRUE:
            otp = get_random_string(length=6, allowed_chars='0123456789')
            subject = "Password Reset OTP"
            message = f"Your OTP for password reset is {otp}. This OTP expires in 5 minutes."
            recipient_list = [email] 
            isSetOTPToDb = set_otp_in_db(db_connection, otp, email)
            if not isSetOTPToDb:
                return None, "Error in set OTP"
            
            send_email(subject, message, recipient_list)
            return otp, None
        else:
            return None, "Email Not Send."
    
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None, {e}
    
def set_otp_in_db(db_connection, otp, email):
    try:
        cursor = db_connection.cursor(dictionary=True)  
        user = fetch_user_for_otp(cursor, email)
        
        if not user:
            # Insert new OTP entry
            cursor.execute(OTP_INSERT_QUERY, (email, otp))
        else:
            # Update existing OTP
            cursor.execute(UPDATE_NEW_OTP, (otp, email))

        db_connection.commit()
        return True

    except Exception as e:
        print(f"Error setting OTP: {str(e)}")
        return False
    finally:
        cursor.close()


def fetch_user_for_otp(cursor, email):
    try:
        cursor.execute(FETCH_EMAIL_FOR_OTP, (email,))
        return cursor.fetchone()  # Fetch the user record
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None

def verify_otp(db_connection, request):
    try:
        cursor = db_connection.cursor(dictionary=True)  
        email = request.data.get("email")
        otp = request.data.get("otp")
        current_time_str = request.data.get("currentTime")  

        try:
            current_time = datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Invalid datetime format for currentTime.")
            return False

        user = fetch_user_for_otp(cursor, email)
        
        if not user:
            print("Email not found in OTP records.")
            return False 

        stored_otp = user["otp"]
        updated_at = user["updated_at"]
        expires_at = user["expires_at"]
        
        if isinstance(updated_at, str):
            updated_at = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")

        if isinstance(expires_at, str):
            expires_at = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S")

        print(f"Updated At: {updated_at}, Expires At: {expires_at}, Current Time: {current_time}")

        if stored_otp != otp:
            print("OTP does not match.")
            return False

        if not (updated_at <= current_time <= expires_at):
            print("OTP expired or invalid time range.")
            return False
        return True

    except Exception as e:
        print(f"Error verifying OTP: {str(e)}")
        return False
    finally:
        cursor.close()

def password_reset(db_connection, request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")
        cursor = db_connection.cursor()
        user = fetch_user_by_email(db_connection, email)
        if not user:
            return False
        cursor.execute(UPDATE_PASSWORD_QUERY, (encrypt_password(password), email))
        db_connection.commit()
        return True
    except Exception as e:
        print(f"Error in reseting password: {str(e)}")
        return False
    finally:
        cursor.close() 