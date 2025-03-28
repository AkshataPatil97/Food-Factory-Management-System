import json
from constants.queries import INSERT_STAFF_QUERY, SET_ORDER_TO_DELIVERY_BOY_QUERY,CHECK_STAFF_QUERY,FETCH_STAFF_BY_ID_QUERY

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
        cursor = db_connection.cursor()

        cursor.execute(CHECK_STAFF_QUERY, (staff_id,))
        result = cursor.fetchone()

        if not result:
            return {"error": "Staff not found or not a delivery boy"}, 400

        # Update order_id for delivery boy
        cursor.execute(SET_ORDER_TO_DELIVERY_BOY_QUERY, (order_id, staff_id))
        db_connection.commit()

        if cursor.rowcount > 0:
            return {"message": "Order assigned to delivery boy successfully", "staff_id": staff_id, "order_id": order_id}, 200
        else:
            return {"error": "Failed to assign order"}, 500

    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        
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
    
