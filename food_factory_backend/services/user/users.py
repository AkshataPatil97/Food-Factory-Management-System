from constants.queries import USER_INSERT_QUERY, FETCH_ALL_USERS_QUERY ,FETCH_USER_BY_EMAIL
from constants.constant import TRUE
from constants.bd_config import EMAIL_SEND_TO_USER
from services.sendemail.sendemail import send_email
from services.passwordencrypt.passwordencrypt import encrypt_password
from services.db_config.dbConfigService import fetch_db_config_data

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