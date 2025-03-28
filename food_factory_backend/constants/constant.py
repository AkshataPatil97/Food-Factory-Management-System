TRUE = 'true'
FALSE = 'false'

DEALER_ADMIN_DETAILS = {
    "MOBILE_NUMBER" : 'Mobile Number',
    "ADDRESS" : 'Address',
    "SHOP_NAME" : 'Business Name',
    "PROFILE_PHOTO" : 'Profile Photo',
    "ABOUT" : 'About'
}

DEALER_ADMIN_DETAILS_COLUMNS = {
    "MOBILE_NUMBER" : 'mobile_no',
    "ADDRESS" : 'address_payload',
    "SHOP_NAME" : 'shop_name',
    "PROFILE_PHOTO" : 'profile_photo',
    "ABOUT" : 'about'
}

USER_DETAILS = {
    "EMAIL": 'Email',
    "NAME": 'Name',

}

USER_DETAILS_COLUMNS = {
    "NAME": 'username',
    "EMAIL": 'email',
}

SHIPPED_EMAIL = {
    "SUBJECT": "Your Order Has Been Shipped!",
    "MESSAGE": """\
Dear {customer_name},

We are excited to inform you that your order (Order ID: {order_id}) has been shipped and is on its way to you.

📦 **Order Details**:
- **Order ID:** {order_id}
- **Total Price:** ${total_price}
- **Shipping Address:** {shipping_address}

🚚 **Delivery Information**:
- **Assigned Delivery Staff:** {delivery_boy_name}
- **Contact Number:** {delivery_boy_phone}

You can track your order and get real-time updates by visiting our website.

Thank you for shopping with us!

Best Regards,  
{company_name}
"""
}
