import json 
from constants.queries import(
    INSERT_ORDER_DETAIL_QUERY, INSERT_ORDER_PRODUCT_DETAILS_QUERY,
    FETCH_USER_ORDERS_QUERY, CANCEL_ORDER_QUERY, UPDATE_ORDER_QUERY,
    FETCH_EXISTING_ORDER_ITEMS_QUERY, UPDATE_ORDER_ITEM_QUERY, DELETE_ORDER_ITEM_QUERY,
    FETCH_ALL_ORDER_QUERY, UPDATE_ORDER_STATUS_QUERY, FETCH_CANCELED_ORDER_QUERY,
    FETCH_DELIVERED_ORDER_QUERY, SET_ORDER_TO_DELIVERY_BOY_QUERY, FETCH_ORDER_BY_ID_QUERY
)
from config.connection import get_conn, close_conn


# def insert_order(db_connection, request):
#     try:
#         from .sendemail import send_order_placed_email
#         cursor = db_connection.cursor()
#         data = json.loads(request.body)

#         userData = fetch_user_for_order(db_connection, data.get("user_id"))
#         print(userData)
#         # Insert order into orders table
#         cursor.execute(
#             INSERT_ORDER_DETAIL_QUERY,
#             (data.get("user_id"), data.get("total_price"), data.get("status"),
#              data.get("is_cancelled", False), data.get("cancellation_reason"))
#         )
        
#         # Get the last inserted order_id
#         order_id = cursor.lastrowid  
#         db_connection.commit()
        
#         send_order_placed_email(userData, data.get("total_price"))
#         return order_id  # Return order_id

#     except Exception as e:
#         db_connection.rollback()
#         print(f"Error inserting order: {str(e)}")
#         return None  

#     finally:
#       cursor.close()

def insert_order(db_connection, request):
    try:
        from .sendemail import send_order_placed_email
        cursor = db_connection.cursor()
        data = json.loads(request.body)

        userData = fetch_user_for_order(db_connection, data.get("user_id"))

        # Validate address presence
        address_payload = userData.get("address_payload")
        if not address_payload:
            return {"success": False, "message": "User address is missing. Cannot place order."}

        # Insert order into orders table
        cursor.execute(
            INSERT_ORDER_DETAIL_QUERY,
            (data.get("user_id"), data.get("total_price"), data.get("status"),
             data.get("is_cancelled", False), data.get("cancellation_reason"))
        )
        
        # Get the last inserted order_id
        order_id = cursor.lastrowid  
        db_connection.commit()
        
        send_order_placed_email(userData, data.get("total_price"))
        return {"success": True, "order_id": order_id}

    except Exception as e:
        db_connection.rollback()
        print(f"Error inserting order: {str(e)}")
        return {"success": False, "message": f"Error inserting order: {str(e)}"}

    finally:
        cursor.close()

def insert_order_details(db_connection, order_id, request):
    try:
        order_items = request.data.get("order_items", [])
        
        if not order_items:
            return {"error": "No order items provided"}
        
        cursor = db_connection.cursor()
        for item in order_items:
            cursor.execute(INSERT_ORDER_PRODUCT_DETAILS_QUERY, (
                order_id,
                item.get("product_id"),
                item.get("quantity", 1),
                item.get("price_at_order")
            ))
        
        db_connection.commit()
        return {"message": "Order items inserted successfully"}
    
    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}
    
    finally:
        cursor.close()
def fetch_orders_by_userId(db_connection, request):
    try:
        from .users import fetch_user_details
        user_id = request.data.get("user_id")  # Use request.data instead of json.loads(request.body)
        if not user_id:
            return {"error": "User ID is required"}

        with db_connection.cursor(dictionary=True) as cursor:
            cursor.execute(FETCH_USER_ORDERS_QUERY, (user_id,))
            rows = cursor.fetchall()

        db_connection.commit()

        if not rows:
            return {}  # Return an empty object instead of {"message": "No orders found", "data": []}

        orders = []  # Change from dictionary to list
        order_map = {}

        for row in rows:
            order_id = row["order_id"]

            if order_id not in order_map:
                order_data = {
                    "order_id": order_id,
                    "user_id": row["user_id"],
                    "user": fetch_user_details(db_connection, row["user_id"]),
                    "total_price": float(row["total_price"]),
                    "status": row["status"],
                    "order_date": row["order_date"].strftime("%Y-%m-%d %H:%M:%S") if row["order_date"] else None,
                    "updated_at": row["updated_at"].strftime("%Y-%m-%d %H:%M:%S") if row["updated_at"] else None,
                    "is_cancelled": bool(row["is_cancelled"]),
                    "cancellation_reason": row["cancellation_reason"],
                    "order_items": []
                }
                order_map[order_id] = order_data
                orders.append(order_data)  # Append to the list

            order_map[order_id]["order_items"].append({
                "order_item_id": row["order_item_id"],
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "quantity": row["quantity"],
                "price_at_order": float(row["price_at_order"]),
                "sub_total": float(row["sub_total"]),
            })

        return orders  # Now returning a list, not a dictionary

    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}


def cancel_order(db_connection, request):
    try:
        data = json.loads(request.body)
        order_id = data.get("order_id")
        cancel_reason = data.get("cancel_reason")
        user_id = data.get("user_id")

        if not order_id or not cancel_reason or not user_id:
            return {"error": "Missing required parameters"}

        with db_connection.cursor() as cursor:
            cursor.execute(CANCEL_ORDER_QUERY, (cancel_reason, order_id, user_id))
            db_connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Order canceled successfully"}
            else:
                return {"error": "Order not found or cannot be canceled"}

    except Exception as e:
        return {"error": str(e)}

def update_order(db_connection, data):
    try:
        from .sendemail import send_order_update_email
        cursor = db_connection.cursor()
        cursor.execute(
            UPDATE_ORDER_QUERY,
            (data.get("total_price"), data.get("status"), data.get("is_cancelled", False),
             data.get("cancellation_reason"), data.get("order_id"))
        )
        db_connection.commit()
        userData = fetch_user_for_order(db_connection, data.get("user_id"))
        send_order_update_email(userData, data.get("total_price"))
        return {"message": "Order updated successfully"}

    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}

    finally:
        cursor.close()


def update_order_items(db_connection, order_id, data):
    try:
        cursor = db_connection.cursor()
        order_items = data.get("order_items", [])

        # Fetch existing items for comparison
        cursor.execute(FETCH_EXISTING_ORDER_ITEMS_QUERY, (order_id,))
        existing_items = {row[0]: row for row in cursor.fetchall()}  # {product_id: (order_item_id, product_id, quantity, price_at_order)}

        for item in order_items:
            product_id = item.get("product_id")
            if product_id in existing_items:
                # Update existing order item
                cursor.execute(
                    UPDATE_ORDER_ITEM_QUERY,
                    (item.get("quantity", 1), item.get("price_at_order"), order_id, product_id)
                )
                existing_items.pop(product_id)
            else:
                # Insert new order item
                cursor.execute(
                    INSERT_ORDER_PRODUCT_DETAILS_QUERY,
                    (order_id, product_id, item.get("quantity", 1), item.get("price_at_order"))
                )

        # Remove any remaining items (those not present in request)
        for product_id in existing_items:
            cursor.execute(DELETE_ORDER_ITEM_QUERY, (order_id, product_id))

        db_connection.commit()
        return {"message": "Order items updated successfully"}

    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}

    finally:
        cursor.close()

def fetch_order_by_id(db_connection,order_id):
    try:
        from .users import fetch_user_details
        with db_connection.cursor(dictionary=True) as cursor:
            cursor.execute(FETCH_ORDER_BY_ID_QUERY, (order_id,))
            rows = cursor.fetchall()

        if not rows:
            return {"error": "Order not found"}

        order_data = None
        order_items = []

        for row in rows:
            if not order_data:
                order_data = {
                    "order_id": row["order_id"],
                    "user_id": row["user_id"],
                    "user": fetch_user_for_order(db_connection, row["user_id"]),
                    "total_price": float(row["total_price"]),
                    "status": row["status"],
                    "order_date": row["order_date"].strftime("%Y-%m-%d %H:%M:%S") if row["order_date"] else None,
                    "updated_at": row["updated_at"].strftime("%Y-%m-%d %H:%M:%S") if row["updated_at"] else None,
                    "is_cancelled": bool(row["is_cancelled"]),
                    "cancellation_reason": row["cancellation_reason"],
                    "order_items": order_items  # Reference the list directly
                }

            order_items.append({
                "order_item_id": row["order_item_id"],
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "quantity": row["quantity"],
                "price_at_order": float(row["price_at_order"]),
                "sub_total": float(row["sub_total"]),
            })

        return order_data  

    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}

def fetch_all_order(db_connection):
    try:
        from .users import fetch_user_details
        with db_connection.cursor(dictionary=True) as cursor:
            cursor.execute(FETCH_ALL_ORDER_QUERY)
            rows = cursor.fetchall()

        if not rows:
            return []  # Return an empty list instead of {}

        orders = []  
        order_map = {}

        for row in rows:
            order_id = row["order_id"]

            if order_id not in order_map:
                order_data = {
                    "order_id": order_id,
                    "user_id": row["user_id"],
                    "user": fetch_user_for_order(db_connection, row["user_id"]),
                    "total_price": float(row["total_price"]),
                    "status": row["status"],
                    "order_date": row["order_date"].strftime("%Y-%m-%d %H:%M:%S") if row["order_date"] else None,
                    "updated_at": row["updated_at"].strftime("%Y-%m-%d %H:%M:%S") if row["updated_at"] else None,
                    "is_cancelled": bool(row["is_cancelled"]),
                    "cancellation_reason": row["cancellation_reason"],
                    "order_items": []
                }
                order_map[order_id] = order_data
                orders.append(order_data)  

            order_map[order_id]["order_items"].append({
                "order_item_id": row["order_item_id"],
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "quantity": row["quantity"],
                "price_at_order": float(row["price_at_order"]),
                "sub_total": float(row["sub_total"]),
            })

        return orders


    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}

def update_order_status(db_connection, request):
    try:
        from constants.constant import  (SHIPPED_EMAIL,ORDER_PLACED_EMAIL,ORDER_CANCELLED_EMAIL,ORDER_PROCESSING_EMAIL,ORDER_PROCESSED_EMAIL,DELIVERED_EMAIL)
        from services.sendemail import send_order_status_email
        
        order_id = request.data.get("order_id")
        status = request.data.get("status")
        
        STATUS_EMAIL_MAP = {
            "Placed": ORDER_PLACED_EMAIL,
            "Cancelled": ORDER_CANCELLED_EMAIL,
            "Processing": ORDER_PROCESSING_EMAIL,
            "Processed": ORDER_PROCESSED_EMAIL,
            "Shipped": SHIPPED_EMAIL,
            "Delivered": DELIVERED_EMAIL
        }
        email_template = STATUS_EMAIL_MAP.get(status)
        
        if not order_id or not status:
            return {"error": "Order ID and Status are required"}
        with db_connection.cursor() as cursor:
            cursor.execute(UPDATE_ORDER_STATUS_QUERY, (status, order_id))
            db_connection.commit()
            
            if email_template:
                send_order_status_email(request, email_template)

            if cursor.rowcount == 0:
                return {"error": "Order not found or status unchanged"}
            
        return {"success": True, "message": "Order status updated successfully"}

    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}

def update_shipped_order_status(db_connection, request):
    try:
        order_id = request.data.get("order_id")
        status = request.data.get("status")
        staff_id = request.data.get("staff_id")
        
        if not order_id or not status:
            return {"error": "Order ID and Status are required"}
        
        with db_connection.cursor() as cursor:
            # Update order status
            cursor.execute(UPDATE_ORDER_STATUS_QUERY, (status, order_id))
            
            # If staff_id is provided, assign order to delivery staff
            if staff_id:
                cursor.execute(SET_ORDER_TO_DELIVERY_BOY_QUERY, (order_id, staff_id))

            if cursor.rowcount == 0:
                return {"error": "Order not found or status unchanged"}

            db_connection.commit()
           
        return {"success": True, "message": "Order status updated successfully"}

    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}

def fetch_delivered_order(db_connection):
    try:
        from .users import fetch_user_details
        with db_connection.cursor(dictionary=True) as cursor:
            cursor.execute(FETCH_DELIVERED_ORDER_QUERY)
            rows = cursor.fetchall()

        if not rows:
            return []  # Return an empty list instead of {}

        orders = []  
        order_map = {}

        for row in rows:
            order_id = row["order_id"]

            if order_id not in order_map:
                order_data = {
                    "order_id": order_id,
                    "user_id": row["user_id"],
                    "user": fetch_user_for_order(db_connection, row["user_id"]),
                    "total_price": float(row["total_price"]),
                    "status": row["status"],
                    "order_date": row["order_date"].strftime("%Y-%m-%d %H:%M:%S") if row["order_date"] else None,
                    "updated_at": row["updated_at"].strftime("%Y-%m-%d %H:%M:%S") if row["updated_at"] else None,
                    "is_cancelled": bool(row["is_cancelled"]),
                    "cancellation_reason": row["cancellation_reason"],
                    "order_items": []
                }
                order_map[order_id] = order_data
                orders.append(order_data)  

            order_map[order_id]["order_items"].append({
                "order_item_id": row["order_item_id"],
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "quantity": row["quantity"],
                "price_at_order": float(row["price_at_order"]),
                "sub_total": float(row["sub_total"]),
            })

        return orders  

    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}
    
def fetch_canceled_order(db_connection):
    try:
        from .users import fetch_user_details
        with db_connection.cursor(dictionary=True) as cursor:
            cursor.execute(FETCH_CANCELED_ORDER_QUERY)
            rows = cursor.fetchall()

        if not rows:
            return []  # Return an empty list instead of {}

        orders = []  
        order_map = {}

        for row in rows:
            order_id = row["order_id"]

            if order_id not in order_map:
                order_data = {
                    "order_id": order_id,
                    "user_id": row["user_id"],
                    "user": fetch_user_for_order(db_connection, row["user_id"]),
                    "total_price": float(row["total_price"]),
                    "status": row["status"],
                    "order_date": row["order_date"].strftime("%Y-%m-%d %H:%M:%S") if row["order_date"] else None,
                    "updated_at": row["updated_at"].strftime("%Y-%m-%d %H:%M:%S") if row["updated_at"] else None,
                    "is_cancelled": bool(row["is_cancelled"]),
                    "cancellation_reason": row["cancellation_reason"],
                    "order_items": []
                }
                order_map[order_id] = order_data
                orders.append(order_data)  

            order_map[order_id]["order_items"].append({
                "order_item_id": row["order_item_id"],
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "quantity": row["quantity"],
                "price_at_order": float(row["price_at_order"]),
                "sub_total": float(row["sub_total"]),
            })

        return orders  

    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}

def fetch_order_by_id_invoice(db_connection, order_id):
    try:
        with db_connection.cursor(dictionary=True) as cursor:
            cursor.execute(FETCH_ORDER_BY_ID_QUERY, (order_id,))
            rows = cursor.fetchall()

        if not rows:
            return []  # ✅ Return an empty list instead of an error dict

        order_data = None
        order_items = []

        for row in rows:
            if not order_data:
                order_data = {
                    "order_id": row["order_id"],
                    "user_id": row["user_id"],
                    "total_price": float(row["total_price"]),
                    "status": row["status"],
                    "order_date": row["order_date"].strftime("%Y-%m-%d %H:%M:%S") if row["order_date"] else None,
                    "updated_at": row["updated_at"].strftime("%Y-%m-%d %H:%M:%S") if row["updated_at"] else None,
                    "is_cancelled": bool(row["is_cancelled"]),
                    "cancellation_reason": row["cancellation_reason"],
                    "order_items": order_items  # Reference the list directly
                }

            order_items.append({
                "order_item_id": row["order_item_id"],
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "quantity": row["quantity"],
                "price_at_order": float(row["price_at_order"]),
                "sub_total": float(row["sub_total"]),
            })

        return order_data  # ✅ Return the order object

    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}


def fetch_user_for_order(db_connection, user_id):
    from .users import fetch_user_by_id,fetch_dealer_details_by_id
    user_data = fetch_user_by_id(db_connection, user_id) or {}
    dealer_details = fetch_dealer_details_by_id(db_connection, user_id) or {}

    user = {**user_data, **dealer_details}     
    return user