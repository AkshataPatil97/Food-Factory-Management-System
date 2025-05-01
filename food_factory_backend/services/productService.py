from constants.queries import INSERT_PRODUCT_QUERY, FETCH_ALL_PRODUCT_QUERY, FETCH_PRODUCT_BY_CODE, UPDATE_PRODUCT_BY_CODE, DELETE_PRODUCT_BY_CODE
import base64

def insert_product(db_connection, request):
    try:
        cursor = db_connection.cursor()
        data = request.data
        product_img_file = request.FILES.get('product_img')

        product_img_data = None
        if product_img_file:
            product_img_data = product_img_file.read()  # Read binary content

        cursor.execute(INSERT_PRODUCT_QUERY, (
            data.get('product_name'),
            data.get('product_code'),
            data.get('category_id'),
            data.get('manufacturing_date'),
            data.get('expiry_date'),
            data.get('price'),
            product_img_data,  # Store binary directly
        ))
        db_connection.commit()
        return True

    except Exception as e:
        if e.args[0] == 1062:
            print("Duplicate product detected")
            return "product already exists"
        print(f"Error inserting product: {str(e)}")
        return False
    finally:
        cursor.close()

def fetchall_products(db_connection):
    try:
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(FETCH_ALL_PRODUCT_QUERY)
        data = cursor.fetchall()

        for product in data:
            if product.get('product_img'):
                try:
                    # Convert binary to base64 string
                    product['product_img'] = base64.b64encode(product['product_img']).decode('utf-8')
                except Exception as e:
                    product['product_img'] = None

        return data
    except Exception as e:
        print(f"Error fetching product: {str(e)}")
        return {"error": str(e)}
    finally:
        cursor.close()


def fetch_product_by_code(db_connection, code):
    try:
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute(FETCH_PRODUCT_BY_CODE, (code,))
        product = cursor.fetchone()
        if product.get('product_img'):
                try:
                    # Convert binary to base64 string
                    product['product_img'] = base64.b64encode(product['product_img']).decode('utf-8')
                except Exception as e:
                    product['product_img'] = None
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
        data = req.data  
        product_img_file = req.FILES.get('product_img')
        
        product_img_data = None
        if product_img_file:
            product_img_data = product_img_file.read()
            
        cursor.execute(UPDATE_PRODUCT_BY_CODE, (
            data.get("product_name"),
            data.get("category_id"),
            data.get("manufacturing_date"),
            data.get("expiry_date"),
            data.get("price"),
            product_img_data,
            code  # Using the provided product code
        ))
        
        db_connection.commit()
        return cursor.rowcount > 0  # Returns True if update was successful

    except Exception as e:
        print("Error updating product:", e)
        return False

    finally:
        cursor.close()

