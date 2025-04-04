import json
from constants.constant import TRUE
from constants.queries import (
    INSERT_STAFF_QUERY, SET_ORDER_TO_DELIVERY_BOY_QUERY,CHECK_STAFF_QUERY,
    FETCH_STAFF_BY_ID_QUERY,FETCH_ALL_DELIVERY_BOY_QUERY, FETCH_ALL_STAFF_QUERY,
    FETCH_STAFF_BY_NUMBER_QUERY, SET_ORDER_TO_NULL_DELIVERY_BOY_QUERY
)
from django.utils.crypto import get_random_string
from constants.bd_config import EMAIL_SEND_TO_USER


def insert_staff(db_connection, request):
    try:
        cursor = db_connection.cursor()
        data = request.data  # Use request.data for Django REST framework

        # Extract required fields
        name = data.get("name")
        phone = data.get("phone")
        alternate_phone = data.get("alternate_phone", None)  # Optional field
        address = data.get("address")
        staff_type = data.get("staff_type") # Default NULL

        print(name,phone)
        # Check for missing required fields
        if not name or not phone or not address or not staff_type:
            return {"error": "Missing required fields"}, 400

        # Execute insert query
        cursor.execute(
            INSERT_STAFF_QUERY,
            (name, phone, alternate_phone, address, staff_type)
        )
        
        staff_id = cursor.lastrowid  # Get the last inserted staff ID
        db_connection.commit()

        return {"message": "Staff inserted successfully", "staff_id": staff_id}, 201

    except Exception as e:
        db_connection.rollback()
        if hasattr(e, "args") and e.args[0] == 1062:  # Duplicate entry error
            return {"error": "Phone number already exists"}, 400
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        
def assign_order_to_delivery_boy(db_connection, staff_id, order_id):
    try:
        print(f"Assigning order: staff_id={staff_id}, order_id={order_id}")

        cursor = db_connection.cursor()

        print(f"Executing CHECK_STAFF_QUERY for staff_id={staff_id}")
        cursor.execute(CHECK_STAFF_QUERY, (staff_id,))
        print("Query executed successfully")

        result = cursor.fetchone()
        print("Staff query result:", result)

        if not result:
            print(f"Staff ID {staff_id} not found or not a delivery boy.")
            return {"error": "Staff not found or not a delivery boy"}, 400

        if order_id is None:
            print(f"Setting order_id to NULL for staff_id={staff_id}")
            cursor.execute(SET_ORDER_TO_NULL_DELIVERY_BOY_QUERY, (staff_id,))
        else:
            print(f"Assigning order_id={order_id} to staff_id={staff_id}")
            cursor.execute(SET_ORDER_TO_DELIVERY_BOY_QUERY, (order_id, staff_id))

        db_connection.commit()
        affected_rows = cursor.rowcount
        print(f"Rows affected: {affected_rows}")

        cursor.close()

        if affected_rows > 0:
            return {"message": "Order assigned to delivery boy successfully", "staff_id": staff_id, "order_id": order_id}, 200
        else:
            print("Failed to assign order")
            return {"error": "Failed to assign order"}, 500

    except Exception as e:
        print(f"Error in assign_order_to_delivery_boy: {e}")
        db_connection.rollback()
        return {"error": str(e)}, 500


        
def fetch_staff_by_id(db_connection, staff_id):
    cursor = None
    try:
        # LOGGER.info("fetch_user_by_email! ")
        cursor = db_connection.cursor(dictionary=True)  
        cursor.execute(FETCH_STAFF_BY_ID_QUERY, (staff_id,))
        user = cursor.fetchone() 
        return user  
    except Exception as e:
        # LOGGER.error(f"Error fetching user: {e}")
        return None
    finally:
        cursor.close()
        
def fetch_staff_by_phone(db_connection, phone_no):
    cursor = None
    try:
        # LOGGER.info("fetch_user_by_email! ")
        cursor = db_connection.cursor(dictionary=True)  
        cursor.execute(FETCH_STAFF_BY_NUMBER_QUERY, (phone_no,))
        user = cursor.fetchone() 
        return user  
    except Exception as e:
        # LOGGER.error(f"Error fetching user: {e}")
        return None
    finally:
        cursor.close()
        
def fetch_all_delivery_staff(db_connection):
    cursor = None
    try:
        cursor = db_connection.cursor(dictionary=True)  
        cursor.execute(FETCH_ALL_DELIVERY_BOY_QUERY)  
        staff_members = cursor.fetchall()  
        return staff_members  
    except Exception as e:
        # LOGGER.error(f"Error fetching staff: {e}")
        return None
    finally:
        if cursor:
            cursor.close()

def fetch_all_staff(db_connection):
    cursor = None
    try:
        cursor = db_connection.cursor(dictionary=True)  
        cursor.execute(FETCH_ALL_STAFF_QUERY)  
        staff_members = cursor.fetchall()  
        return staff_members  
    except Exception as e:
        # LOGGER.error(f"Error fetching staff: {e}")
        return None
    finally:
        if cursor:
            cursor.close()


def update_staff(db_connection, staff_id, request):
    try:
        cursor = db_connection.cursor()
        data = request.data  # Use request.data for Django REST framework

        # Extract the fields to update
        name = data.get("name")
        phone = data.get("phone")
        alternate_phone = data.get("alternate_phone", None)  # Optional field
        address = data.get("address")
        staff_type = data.get("staff_type")  # Optional

        # Check for required fields
        if not name or not phone or not address:
            return {"error": "Missing required fields"}, 400

        # Prepare the SQL update query
        update_query = """
            UPDATE staff
            SET name = %s, phone = %s, alternate_phone = %s, address = %s, staff_type = %s, updated_at = NOW()
            WHERE id = %s
        """
        
        # Execute the update query
        cursor.execute(update_query, (name, phone, alternate_phone, address, staff_type, staff_id))

        # Commit the changes
        db_connection.commit()

        # Check if any row was updated
        if cursor.rowcount == 0:
            return {"error": "Staff not found"}, 404

        return {"message": "Staff updated successfully"}, 200

    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}, 500

    finally:
        cursor.close()


def delete_staff(db_connection, staff_id):
    try:
        cursor = db_connection.cursor()
       
        # Check for required fields
        if not staff_id:
            return {"error": "Missing required fields"}, 400

        # Prepare the SQL update query
        update_query = """
            UPDATE staff
            SET is_deleted = 1, updated_at = NOW()
            WHERE id = %s
        """
        
        # Execute the update query
        cursor.execute(update_query, (staff_id,))

        # Commit the changes
        db_connection.commit()

        # Check if any row was updated
        if cursor.rowcount == 0:
            return {"error": "Staff not found"}, 404

        return {"message": "Staff updated successfully"}, 200

    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        


def send_otp_email(db_connection, email):
    cursor = None 
    try:
        from .dbConfigService import fetch_db_config_data
        from .sendemail import send_email
        from .users import set_otp_in_db
        # LOGGER.info("send_otp_email! ",email)
        isEmailSend = fetch_db_config_data(db_connection, EMAIL_SEND_TO_USER)
        if isEmailSend == TRUE:
            otp = get_random_string(length=6, allowed_chars='0123456789')
            subject = "Delivery OTP"
            message = f"Your OTP for delivery is {otp}. This OTP expires in 5 minutes."
            recipient_list = [email] 
            isSetOTPToDb = set_otp_in_db(db_connection, otp, email)
            if not isSetOTPToDb:

                return None, "Error in set OTP"
            
            send_email(subject, message, recipient_list)
            return otp, None
        else:
            return None, "Email Not Send."
    
    except Exception as e:
        # LOGGER.error(f"Error fetching user: {e}")
        return None, {e}