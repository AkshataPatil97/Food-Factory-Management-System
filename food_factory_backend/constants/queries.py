# User insert query
USER_INSERT_QUERY = """
    INSERT INTO users (username, email, password, role, is_delete)
    VALUES (%s, %s, %s, %s, %s);
"""

# Set null details into dealerDetails
DEALER_DATA_INSERT_QUERY = """
    INSERT INTO dealerDetails (user_id, shop_name, address_payload, mobile_no, profile_photo)
    VALUES (%s, NULL, NULL, NULL, NULL)
"""

# fetch all user query
FETCH_ALL_USERS_QUERY = """ 
    SELECT * FROM users WHERE is_delete = false;
"""

# fetch user by email
FETCH_USER_BY_EMAIL = """ 
    SELECT * FROM users WHERE email = %s;
"""

# fetch from db config table
FETCH_DB_CONFIG_DATA = """
    SELECT map_to FROM db_config WHERE map_from = %s; 
"""

# update db config data
UPDATE_DB_CONFIG_DATA = """
    UPDATE db_config SET map_to = %s WHERE map_from = %s;
"""

# Insert OTP into DB
OTP_INSERT_QUERY = """
    INSERT INTO otp_verification (email, otp, expires_at) 
    VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL 5 MINUTE));
"""

# Fetch by email for OTP
FETCH_EMAIL_FOR_OTP = """
    SELECT * FROM otp_verification WHERE email = %s;
"""

# Update new OTP in DB
UPDATE_NEW_OTP = """
    UPDATE otp_verification 
    SET otp = %s, 
        expires_at = DATE_ADD(NOW(), INTERVAL 5 MINUTE),
        updated_at = NOW() 
    WHERE email = %s;
"""

# Update Password
UPDATE_PASSWORD_QUERY = """
    UPDATE users SET password = %s WHERE email = %s;
"""

# Insert Product
INSERT_PRODUCT_QUERY = """    
    INSERT INTO products (product_name, product_code, category_id, manufacturing_date, expiry_date, price)  
    VALUES (%s, %s, %s, %s, %s, %s);
"""

# fetch all product query
FETCH_ALL_PRODUCT_QUERY = """ 
    SELECT * FROM products WHERE is_deleted = false;
"""

# fetch product by code
FETCH_PRODUCT_BY_CODE = """ 
    SELECT * FROM products WHERE product_code = %s;
"""

# delete product by code
DELETE_PRODUCT_BY_CODE = """
    UPDATE products SET is_deleted = TRUE WHERE product_code = %s;
"""

# update product by code
UPDATE_PRODUCT_BY_CODE = """
    UPDATE products
    SET product_name = %s, category_id = %s, manufacturing_date = %s, expiry_date = %s, price = %s
    WHERE product_code = %s
"""

# Fetch dealer details
FETCH_DEALER_DETAILS_QUERY = """
    SELECT * FROM dealerdetails WHERE user_id = %s;
"""

# Update dealer details
UPDATE_DEALER_DETAILS_QUERY = """
    UPDATE dealerdetails SET 
"""

# Update admin details
UPDATE_ADMIN_DETAILS_QUERY = """
    UPDATE admindetails SET 
"""

# Update user details
UPDATE_USER_DETAILS_QUERY = """
    UPDATE users SET
""" 

# fetch user by id
FETCH_USER_BY_ID = """ 
    SELECT email, username, role FROM users WHERE id = %s;
"""

#query for admin
ADMIN_DATA_INSERT_QUERY = """
    INSERT INTO admindetails (user_id, shop_name, address_payload, mobile_no, profile_photo)
    VALUES (%s, NULL, NULL, NULL, NULL)
"""

# Fetch dealer details
FETCH_ADMIN_DETAILS_QUERY = """
    SELECT * FROM admindetails WHERE user_id = %s;
"""

# Insert order details
INSERT_ORDER_DETAIL_QUERY = """
    INSERT INTO orders (user_id, total_price, status, is_cancelled, cancellation_reason) 
    VALUES (%s, %s, %s, %s, %s)
""" 

# Insert product order details
INSERT_ORDER_PRODUCT_DETAILS_QUERY = """
    INSERT INTO order_items (order_id, product_id, quantity, price_at_order)
    VALUES (%s, %s, %s, %s)
"""

# Fetch Users all orders
FETCH_USER_ORDERS_QUERY = """
    SELECT 
        o.order_id,
        o.user_id,
        o.total_price,
        o.status,
        o.order_date,
        o.updated_at,
        o.is_cancelled,
        o.cancellation_reason,
        oi.order_item_id,
        oi.product_id,
        p.product_name,
        oi.quantity,
        oi.price_at_order,
        oi.sub_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_code
    WHERE o.user_id = %s AND o.is_cancelled = FALSE;
"""

# Cancel Order query
CANCEL_ORDER_QUERY = """
    UPDATE orders 
    SET is_cancelled = TRUE, cancellation_reason = %s 
    WHERE order_id = %s AND user_id = %s AND status IN ('Pending', 'Processing');
"""

# Update order details
UPDATE_ORDER_QUERY = """
    UPDATE orders
    SET total_price = %s, status = %s, is_cancelled = %s, cancellation_reason = %s
    WHERE order_id = %s;
"""

# Fetch existing order items
FETCH_EXISTING_ORDER_ITEMS_QUERY = """
    SELECT product_id FROM order_items WHERE order_id = %s;
"""

# Update an existing order item
UPDATE_ORDER_ITEM_QUERY = """
    UPDATE order_items
    SET quantity = %s, price_at_order = %s
    WHERE order_id = %s AND product_id = %s;
"""

# Delete an order item (if it's not in the updated list)
DELETE_ORDER_ITEM_QUERY = """
    DELETE FROM order_items WHERE order_id = %s AND product_id = %s;
"""

# Fetch all Pending, Processing, Shipped order for admin
FETCH_ALL_ORDER_QUERY = """
    SELECT 
        o.order_id,
        o.user_id,
        o.total_price,
        o.status,
        o.order_date,
        o.updated_at,
        o.is_cancelled,
        o.cancellation_reason,
        oi.order_item_id,
        oi.product_id,
        p.product_name,
        oi.quantity,
        oi.price_at_order,
        oi.sub_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_code
    WHERE o.is_cancelled = FALSE
      AND o.status IN ('Pending', 'Processing', 'Shipped');
"""

# Admin Update order status
UPDATE_ORDER_STATUS_QUERY = """
    UPDATE orders 
    SET status = %s, updated_at = NOW()
    WHERE order_id = %s
"""

# Fetch all Delivered order for admin
FETCH_DELIVERED_ORDER_QUERY = """
    SELECT 
        o.order_id,
        o.user_id,
        o.total_price,
        o.status,
        o.order_date,
        o.updated_at,
        o.is_cancelled,
        o.cancellation_reason,
        oi.order_item_id,
        oi.product_id,
        p.product_name,
        oi.quantity,
        oi.price_at_order,
        oi.sub_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_code
    WHERE o.is_cancelled = FALSE
      AND o.status IN ('Delivered');
"""

# Fetch all Delivered order for admin
FETCH_CANCELED_ORDER_QUERY = """
    SELECT 
        o.order_id,
        o.user_id,
        o.total_price,
        o.status,
        o.order_date,
        o.updated_at,
        o.is_cancelled,
        o.cancellation_reason,
        oi.order_item_id,
        oi.product_id,
        p.product_name,
        oi.quantity,
        oi.price_at_order,
        oi.sub_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_code
    WHERE o.is_cancelled = TRUE
      AND o.status IN ('Cancelled');
"""