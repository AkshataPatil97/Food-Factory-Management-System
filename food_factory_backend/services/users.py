from constants.queries import (
    USER_INSERT_QUERY, UPDATE_ADMIN_DETAILS_QUERY, FETCH_ALL_USERS_QUERY ,FETCH_USER_BY_EMAIL, FETCH_USER_BY_ID, OTP_INSERT_QUERY, 
    FETCH_EMAIL_FOR_OTP, UPDATE_NEW_OTP, UPDATE_PASSWORD_QUERY, DEALER_DATA_INSERT_QUERY, FETCH_DEALER_DETAILS_QUERY, UPDATE_DEALER_DETAILS_QUERY,
    UPDATE_USER_DETAILS_QUERY, ADMIN_DATA_INSERT_QUERY, FETCH_ADMIN_DETAILS_QUERY, FETCH_COMPANY_DETAILS_QUERY, INSER_COMPANY_DETAIL
)
from constants.constant import TRUE, DEALER_ADMIN_DETAILS, DEALER_ADMIN_DETAILS_COLUMNS, USER_DETAILS, USER_DETAILS_COLUMNS
from constants.bd_config import EMAIL_SEND_TO_USER
from services.sendemail import send_email
from services.passwordencrypt import encrypt_password
from services.dbConfigService import fetch_db_config_data
from django.utils.crypto import get_random_string
from datetime import datetime
from logger import LOGGER
import json


def insert_user(db_connection, data):
    """ Insert a new user into the database.
    Args:
        db_connection: The active database connection.
        data (dict): A dictionary containing user data.
            Required keys: 'username', 'email', 'password', 'role', 'is_delete'.
    Returns:
        bool: True if the user was successfully inserted, False otherwise."""

    try:
        LOGGER.info("Inside insert_user! ",data.get('username'))
        cursor = db_connection.cursor()
        cursor.execute(USER_INSERT_QUERY, (
            data.get('username'),
            data.get('email'),
            encrypt_password(data.get('password')),
            data.get('role'),
            data.get('is_delete', 0)  
        ))
        user_id = cursor.lastrowid 
        isEmailSend = fetch_db_config_data(db_connection, EMAIL_SEND_TO_USER)
        if isEmailSend == TRUE:
            isSend = send_email_to_user(data.get('email'))
            if isSend:
                db_connection.commit()
                return {"success": True, "user_id": user_id}
            else:
                return {"success": False, "error": "Failed to send email"}
        else:
            db_connection.commit()
            return {"success": True, "user_id": user_id}

        
    except Exception as e:
        if e.args[0] == 1062:
            LOGGER.error("Duplicate email detected")
            return "email already exists"
        else:
            LOGGER.error(f"Error inserting user: {str(e)}")
            return False
    finally:
        cursor.close()


def fetchall_users(db_connection):
    cursor = None
    try:
        LOGGER.info("Inside fetchall_user! ")
        cursor = db_connection.cursor()
        cursor.execute(FETCH_ALL_USERS_QUERY)
        data = cursor.fetchall()
        db_connection.commit()
        return data
    except Exception as e:
        LOGGER.error(f"Error fetching users: {str(e)}")
        return e
    finally:
        cursor.close()

def fetch_user_by_email(db_connection, email):
    cursor = None
    try:
        LOGGER.info("fetch_user_by_email! ")
        cursor = db_connection.cursor(dictionary=True)  
        cursor.execute(FETCH_USER_BY_EMAIL, (email,))
        user = cursor.fetchone() 
        return user  
    except Exception as e:
        LOGGER.error(f"Error fetching user: {e}")
        return None
    finally:
        cursor.close()
        
def fetch_user_by_id(db_connection, user_id):
    cursor = None
    try:
        LOGGER.info("fetch_user_by_email! ")
        cursor = db_connection.cursor(dictionary=True)  
        cursor.execute(FETCH_USER_BY_ID, (user_id,))
        user = cursor.fetchone() 
        return user  
    except Exception as e:
        LOGGER.error(f"Error fetching user: {e}")
        return None
    finally:
        cursor.close()

def send_email_to_user(email):
    cursor = None 
    try:
        LOGGER.info("Inside send_email_to_user! ",email)
        subject = "Welcome to Our Platform"
        message = "Thank you for registering with us!"
        recipient_list = [email]  

        send_email(subject, message, recipient_list)
        LOGGER.info("send_email_to_user END....")
        return True

    except Exception as e:
        LOGGER.error(f"Error sending email: {e}")
        return False

def send_otp_email(db_connection, email):
    cursor = None 
    try:
        LOGGER.info("send_otp_email! ",email)
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
        LOGGER.error(f"Error fetching user: {e}")
        return None, {e}
    
def set_otp_in_db(db_connection, otp, email):
    cursor = None 
    try:
        print(email)
        cursor = db_connection.cursor(dictionary=True)  
        user = fetch_user_for_otp(db_connection, email)
        
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


def fetch_user_for_otp(db_connection, email):
    cursor = None 
    try:
        cursor = db_connection.cursor(dictionary=True)  
        cursor.execute(FETCH_EMAIL_FOR_OTP, (email,))
        return cursor.fetchone()  # Fetch the user record
    except Exception as e:
        print(f"Error fetching user: {e}")
        return {}
    finally:
        cursor.close()

def verify_otp(db_connection, request):
    cursor = None 
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

        user = fetch_user_for_otp(db_connection, email)
        
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
    cursor = None 
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
        
def insert_dealer_details(db_connection, user_id):
    cursor = None 
    try:
        LOGGER.info(f"Inside insert_dealer_details! user_id: {user_id}")
        cursor = db_connection.cursor()
        cursor.execute(DEALER_DATA_INSERT_QUERY, (user_id,))
        db_connection.commit()
        LOGGER.info("insert_dealer_details END...")
        return True
    except Exception as e:
        LOGGER.error(f"Error in reseting password: {str(e)}")
        return False
    finally:
        cursor.close() 

        
def insert_admin_details(db_connection, user_id):
    cursor = None 
    try:
        LOGGER.info(f"Inside insert_admin_details! user_id: {user_id}")
        cursor = db_connection.cursor()
        cursor.execute(ADMIN_DATA_INSERT_QUERY, (user_id,))
        db_connection.commit()
        LOGGER.info("insert_admin_details END...")
        return True
    except Exception as e:
        LOGGER.error(f"Error in insert admin details: {str(e)}")
        return False
    finally:
        cursor.close() 
        
def fetch_dealer_details(db_connection, request):
    cursor = None 
    try:
        LOGGER.info("Inside fetch_dealer_details!")
        
        data = json.loads(request.body)
        cursor = db_connection.cursor(dictionary=True) 
        if data.get('user_role') == "Dealer":
            cursor.execute(FETCH_DEALER_DETAILS_QUERY, (data.get('user_id'),))
        if data.get('user_role') == "Admin":
            cursor.execute(FETCH_ADMIN_DETAILS_QUERY, (data.get('user_id'),))
        dealer_details = cursor.fetchone()  
        
        if dealer_details:
            return dealer_details 
        else:
            return {}  
        
    except Exception as e:
        LOGGER.error(f"Error fetching dealer details: {e}")
        return {} 
    
    finally:
        cursor.close()
        
def fetch_user_details(db_connection, user_id):
    cursor = None 
    try:
        LOGGER.info("Inside fetch_user_details!")
        print(user_id)
        cursor = db_connection.cursor(dictionary=True) 
        cursor.execute(FETCH_USER_BY_ID, (user_id,))  # Use user_id directly
        user_details = cursor.fetchone() 
        
        return user_details if user_details else {}  
        
    except Exception as e:
        LOGGER.error(f"Error fetching user details: {e}")
        return {} 
    
    finally:
        if cursor:
            cursor.close()

        
def update_dealer_details(db_connection, request):
    cursor = None  
    
    try:
        LOGGER.info("Inside update_dealer_details!")
        
        data = json.loads(request.body)
        update_field = data.get('update_field')
        update_value = data.get('update_value')
        user_id = data.get('user_id')

        if update_field not in DEALER_ADMIN_DETAILS.values():
            return update_user_data(db_connection, request)
        
        column_name = DEALER_ADMIN_DETAILS_COLUMNS.get(
            next((key for key, value in DEALER_ADMIN_DETAILS.items() if value == update_field), None)
        )

        if not column_name:
            raise ValueError("Invalid update field")
        
        user = fetch_user_details(db_connection, user_id)
        print(user)
        if user["role"] == "Dealer":
            user_details_update_query = f"{UPDATE_DEALER_DETAILS_QUERY} {column_name} = %s WHERE user_id = %s"
            LOGGER.info(f"Update Query - {user_details_update_query}")

        if user["role"] == "Admin":
            user_details_update_query = f"{UPDATE_ADMIN_DETAILS_QUERY} {column_name} = %s WHERE user_id = %s"
            LOGGER.info(f"Update Query - {user_details_update_query}")
            
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(user_details_update_query, (update_value, user_id))  
        db_connection.commit()

        LOGGER.info("update_dealer_details END...")
        return user_id  

    except Exception as e:
        LOGGER.error(f"Error updating dealer details: {e}")
        return None 

    finally:
        if cursor:
            cursor.close()

def update_user_data(db_connection, request):
    cursor = None  
    
    try:
        LOGGER.info("Inside update_user_data!")
        
        data = json.loads(request.body)
        update_field = data.get('update_field')
        update_value = data.get('update_value')
        user_id = data.get('user_id')

        column_name = USER_DETAILS_COLUMNS.get(
            next((key for key, value in USER_DETAILS.items() if value == update_field), None)
        )

        if not column_name:
            raise ValueError("Invalid update field")

        user_details_update_query = f"{UPDATE_USER_DETAILS_QUERY} {column_name} = %s WHERE id = %s"
        LOGGER.info(f"Update Query - {user_details_update_query}")

        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(user_details_update_query, (update_value, user_id))  
        db_connection.commit()

        LOGGER.info("update_user_data END...")
        return user_id  

    except Exception as e:
        LOGGER.error(f"Error updating user details: {e}")
        return None 

    finally:
        if cursor:
            cursor.close()

def fetch_dealer_details_by_id(db_connection, user_id):
    cursor = None 
    try:
        LOGGER.info("Inside fetch_dealer_details!")
        cursor = db_connection.cursor(dictionary=True) 
        cursor.execute(FETCH_DEALER_DETAILS_QUERY, (user_id,))
        dealer_details = cursor.fetchone()  
        
        if dealer_details:
            return dealer_details 
        else:
            return {}  
        
    except Exception as e:
        LOGGER.error(f"Error fetching dealer details: {e}")
        return {} 
    
    finally:
        cursor.close()


def fetch_company_details(db_connection):
    cursor = None 
    try:
        LOGGER.info("Inside fetch_company_details!")
        cursor = db_connection.cursor(dictionary=True) 
        cursor.execute(FETCH_COMPANY_DETAILS_QUERY)
        company_details = cursor.fetchone()  
        
        if company_details:
            return company_details 
        else:
            return {}  
        
    except Exception as e:
        LOGGER.error(f"Error fetching company details: {e}")
        return {} 
    
    finally:
        cursor.close()
        
def insert_company_details(db_connection, request):
    cursor = None
    try:
        LOGGER.info("Inside insert_company_details!")
        data = json.loads(request.body)

        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        alternate_phone = data.get('alternate_phone')
        address = data.get('address')
        company_logo = data.get('company_logo')
        founded_in = data.get('founded_in')

        cursor = db_connection.cursor(dictionary=True)

        insert_query = """
            INSERT INTO companydetail 
            (name, email, phone, alternate_phone, address, company_logo, founded_in)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            name, email, phone, alternate_phone, address, company_logo, founded_in
        ))
        db_connection.commit()

        # Optionally fetch and return the inserted row
        cursor.execute("SELECT * FROM companydetail WHERE id = LAST_INSERT_ID()")
        company_details = cursor.fetchone()

        return company_details if company_details else {}

    except Exception as e:
        LOGGER.error(f"Error inserting company details: {e}")
        return {}

    finally:
        if cursor:
            cursor.close()

def update_company_details(db_connection, request):
    cursor = None
    try:
        LOGGER.info("Inside update_company_details!")
        data = json.loads(request.body)

        company_id = data.get('id')
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        alternate_phone = data.get('alternate_phone')
        address = data.get('address')
        company_logo = data.get('company_logo')
        founded_in = data.get('founded_in')

        if not company_id:
            LOGGER.error("Company ID not provided for update.")
            return {}

        cursor = db_connection.cursor(dictionary=True)

        update_query = """
            UPDATE companydetail
            SET name = %s,
                email = %s,
                phone = %s,
                alternate_phone = %s,
                address = %s,
                company_logo = %s,
                founded_in = %s,
                is_updated = 1
            WHERE id = %s
        """

        cursor.execute(update_query, (
            name, email, phone, alternate_phone, address, company_logo, founded_in, company_id
        ))
        db_connection.commit()

        cursor.execute("SELECT * FROM companydetail WHERE id = %s", (company_id,))
        updated_company = cursor.fetchone()

        return updated_company if updated_company else {}

    except Exception as e:
        LOGGER.error(f"Error updating company details: {e}")
        return {}

    finally:
        if cursor:
            cursor.close()

def delete_company_details(db_connection, request):
    cursor = None
    try:
        LOGGER.info("Inside delete_company_details!")
        data = json.loads(request.body)

        company_id = data.get('id')

        if not company_id:
            LOGGER.error("Company ID not provided for deletion.")
            return {"success": False, "message": "Company ID is required"}

        cursor = db_connection.cursor(dictionary=True)

        delete_query = "DELETE FROM companydetail WHERE id = %s"
        cursor.execute(delete_query, (company_id,))
        db_connection.commit()

        if cursor.rowcount > 0:
            LOGGER.info(f"Company with ID {company_id} deleted successfully.")
            return {"success": True, "message": "Company deleted successfully"}
        else:
            LOGGER.warning(f"No company found with ID {company_id} to delete.")
            return {"success": False, "message": "Company not found"}

    except Exception as e:
        LOGGER.error(f"Error deleting company details: {e}")
        return {"success": False, "message": "Internal server error"}

    finally:
        if cursor:
            cursor.close()
