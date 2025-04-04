import json
from decimal import Decimal
from constants.queries import INSERT_INVOICE_QUERY, FETCH_USER_INVOICES_QUERY, FETCH_INVOICES_FOR_7_DAYS_QUERY

def invoice_details(db_connection, order_id, user_id):
    try:
        from .orderService import fetch_order_by_id_invoice
        from .users import fetch_user_by_id, fetch_dealer_details_by_id
        
        print(f"Inside invoice_details - Order ID: {order_id}, User ID: {user_id}")

        # ✅ Pass only order_id (Fixes 'Python type type cannot be converted' error)
        orders = fetch_order_by_id_invoice(db_connection, order_id)

        if not orders:
            print("No orders found or invalid format.")
            return {"error": "No valid orders found"}

        print("Fetched Orders:", orders)

        # Fetch user details
        user_data = fetch_user_by_id(db_connection, user_id) or {}
        dealer_details = fetch_dealer_details_by_id(db_connection, user_id) or {}

        # Merge user and dealer details
        user_info = {**user_data, **dealer_details}

        if not user_info:
            print("No user details found.")
            return {"error": "User details not found"}

        print("Fetched User Data:", user_info)

        # Compute total amount safely
        total_amount = sum(Decimal(order_item.get('sub_total', 0)) for order_item in orders.get("order_items", []))
        print(f"Total Amount: {total_amount}")

        # Prepare invoice data
        invoice_data = {
            "user_id": user_id,
            "order_data": json.dumps(orders, default=str),  # Convert to JSON string
            "user_data": json.dumps(user_info, default=str),  # Convert to JSON string
            "total_amount": total_amount,
            "status": "Pending"  # Default status
        }

        print("Invoice Data to Insert:", invoice_data)

        # Insert into invoices table
        with db_connection.cursor() as cursor:
            cursor.execute(INSERT_INVOICE_QUERY, (
                invoice_data['user_id'],
                invoice_data['order_data'],
                invoice_data['user_data'],
                invoice_data['total_amount'],
                invoice_data['status']
            ))
            invoice_id = cursor.lastrowid  # Get inserted row ID
            db_connection.commit()

        print(f"Invoice Inserted Successfully - ID: {invoice_id}")
        return {"message": "Invoice generated successfully", "invoice_id": invoice_id}

    except Exception as e:
        db_connection.rollback()
        print(f"Error inserting invoice: {str(e)}")
        return {"error": str(e)}
    
def fetch_invoices_user_id(db_connection, request):
    cursor = None
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        cursor = db_connection.cursor(dictionary=True)  
        cursor.execute(FETCH_USER_INVOICES_QUERY, (user_id,))
        invoices = cursor.fetchall() 
        return invoices  
    except Exception as e:
        return None
    finally:
        cursor.close()
        
def fetch_all_invoices(db_connection):
    cursor = None
    try:
        cursor = db_connection.cursor(dictionary=True)  
        cursor.execute(FETCH_INVOICES_FOR_7_DAYS_QUERY)
        invoices = cursor.fetchall() 
        return invoices  
    except Exception as e:
        return None
    finally:
        cursor.close()
        
