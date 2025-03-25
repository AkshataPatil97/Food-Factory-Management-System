import json 
from constants.queries import INSERT_ORDER_DETAIL_QUERY


def insert_order(db_connection, request):
    try:
        cursor = db_connection.cursor()
        data = json.loads(request.body)

        # Insert order into orders table
        cursor.execute(
            INSERT_ORDER_DETAIL_QUERY,
            (data.get("user_id"), data.get("total_price"), data.get("status"),
             data.get("is_cancelled", False), data.get("cancellation_reason"))
        )
        
        # Get the last inserted order_id
        order_id = cursor.lastrowid  
        db_connection.commit()

        return order_id  # Return order_id

    except Exception as e:
        db_connection.rollback()
        print(f"Error inserting order: {str(e)}")
        return None  

    finally:
      cursor.close()

def insert_order_details(db_connection, order_id, request):
    try:
        order_items = request.data.get("order_items", [])
        
        if not order_items:
            return {"error": "No order items provided"}
        
        cursor = db_connection.cursor()
        query = """
            INSERT INTO order_items (order_id, product_id, quantity, price_at_order, sub_total)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        for item in order_items:
            cursor.execute(query, (
                order_id,
                item.get("product_id"),
                item.get("quantity", 1),
                item.get("price_at_order"),
                item.get("sub_total")
            ))
        
        db_connection.commit()
        return {"message": "Order items inserted successfully"}
    
    except Exception as e:
        db_connection.rollback()
        return {"error": str(e)}
    
    finally:
        cursor.close()
