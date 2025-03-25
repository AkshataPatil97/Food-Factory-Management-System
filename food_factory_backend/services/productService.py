from constants.queries import INSERT_PRODUCT_QUERY, FETCH_ALL_PRODUCT_QUERY, FETCH_PRODUCT_BY_CODE, UPDATE_PRODUCT_BY_CODE, DELETE_PRODUCT_BY_CODE

def insert_product(db_connection, request):
    try:
        cursor = db_connection.cursor()
        data = request.data
        cursor.execute(INSERT_PRODUCT_QUERY, (
           data.get('product_name'),
           data.get('product_code'), 
           data.get('category_id'), 
           data.get('manufacturing_date'), 
           data.get('expiry_date'), 
           data.get('price')
        ))
        db_connection.commit()
        return True    
    except Exception as e:
        if e.args[0] == 1062:
            print("Duplicate product detected")
            return "product already exists"
        else:
            print(f"Error inserting product: {str(e)}")
            return False
    finally:
        cursor.close()


def fetchall_products(db_connection):
    try:
        cursor = db_connection.cursor()
        cursor.execute(FETCH_ALL_PRODUCT_QUERY)
        data = cursor.fetchall()
        db_connection.commit()
        return data
    except Exception as e:
        print(f"Error fetching product: {str(e)}")
        return e
    finally:
        cursor.close()


def fetch_product_by_code(db_connection, code):
    try:
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(FETCH_PRODUCT_BY_CODE, (code,))
        product = cursor.fetchone()
        return product
    except Exception as e:
        print(f"Error fetching product: {e}")
        return None
    finally:
        cursor.close()    

def delete_product(db_connection, code):
    try:
        cursor = db_connection.cursor()
        cursor.execute(DELETE_PRODUCT_BY_CODE, (code,))
        db_connection.commit()
        return cursor.rowcount > 0 
    except Exception as e:
        print("Error marking product as deleted:", e)
        return False
    finally:
        cursor.close()
        
def update_product(db_connection, req, code):
    try:
        cursor = db_connection.cursor()
        data = req.data  # Extracting data from request
        cursor.execute(UPDATE_PRODUCT_BY_CODE, (
            data.get("product_name"),
            data.get("category_id"),
            data.get("manufacturing_date"),
            data.get("expiry_date"),
            data.get("price"),
            code  # Using the provided product code
        ))
        
        db_connection.commit()
        return cursor.rowcount > 0  # Returns True if update was successful

    except Exception as e:
        print("Error updating product:", e)
        return False

    finally:
        cursor.close()

