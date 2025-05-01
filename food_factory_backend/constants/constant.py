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

# SHIPPED_EMAIL = {
#     "SUBJECT": "Your Order Has Been Shipped!",
#     "MESSAGE": """\
# Dear {customer_name},

# We are excited to inform you that your order (Order ID: {order_id}) has been shipped and is on its way to you.

# 📦 **Order Details**:
# - **Order ID:** {order_id}
# - **Total Price:** ${total_price}
# - **Shipping Address:** {shipping_address}

# 🚚 **Delivery Information**:
# - **Assigned Delivery Staff:** {delivery_boy_name}
# - **Contact Number:** {delivery_boy_phone}

# You can track your order and get real-time updates by visiting our website.

# Thank you for shopping with us!

# Best Regards,  
# {company_name}
# """
# }

ORDER_PROCESSING_EMAIL = {
    "STATUS": "Order Processing",
    "SUBJECT": "⏳ Your Order is Being Processing!",
    "MESSAGE": """\
Hi {customer_name},

Just letting you know — your order (Order ID: _{order_id}_) is now being processing 🛠️

Our team is working hard to get it ready for shipment. We’ll update you soon!

Thank you for your patience 🙏

Best,  
_{company_name} Team_
"""
}

ORDER_PROCESSED_EMAIL = {
    "STATUS": "Order Processed",
    "SUBJECT": "✅ Your Order Has Been Processed!",
    "MESSAGE": """\
Hi {customer_name},

Awesome news! Your order (Order ID: _{order_id}_) has been processed and packed 📦🎉

We’re getting it ready for shipment. Tracking details will be updated shortly.

Stay excited! Your order is on its way 🚀

Warm Regards,  
_{company_name} Team_
"""
}

ORDER_CANCELLED_EMAIL = {
    "STATUS": "Order Cancelled",
    "SUBJECT": "⚠️ Your Order Has Been Cancelled",
    "MESSAGE": """\
Hi {customer_name},

We regret to inform you that your order (Order ID: _{order_id}_) has been cancelled. ❌

If this was a mistake or if you need assistance, please reach out to our support team immediately.

We’re here to help you anytime! 🤝

Sincerely,  
_{company_name} Support_
"""
}

ORDER_PLACED_EMAIL = {
    "STATUS": "Order Placed",
    "SUBJECT": "🎉 Your Order is Confirmed!",
    "MESSAGE": """\
Hi {customer_name},

Thank you for placing your order with us! 🛒

🧾 Order Details:
- Order ID: _{order_id}_
- Total Amount: ₹_{total_price}_
- Shipping Address: _{shipping_address}_

Your order is now being prepared. We’ll notify you once it moves to the next stage!

Thanks for trusting us 🙌

Warm Regards,  
_{company_name} Team_
"""
}

SHIPPED_EMAIL = {
    "SUBJECT": "🎉 Your Order Has Been Shipped!",
    "MESSAGE": """\
Hi {customer_name},

Good news! Your order (Order ID: _{order_id}_) has been shipped and is on its way 🚚✨

📦 Order Summary:
- Order ID: _{order_id}_
- Total Price: ₹_{total_price}_
- Shipping Address: _{shipping_address}_

🚚 Delivery Information:
- Delivery Staff: _{delivery_boy_name}_
- Contact Number: _{delivery_boy_phone}_

You can track your shipment and see real-time updates on our website.

Thank you for choosing us! We hope you enjoy your purchase 💖

Best Wishes,  
_{company_name} Team_
"""
}

DELIVERED_EMAIL = {
    "STATUS": "Order Delivered",
    "SUBJECT": "🎉 Your Order Has Been Delivered!",
    "MESSAGE": """\
Hi {customer_name},

We are thrilled to inform you that your order (Order ID: {order_id}) has been SUCCESSFULLY DELIVERED 🏡✨

ORDER SUMMARY:
- Order ID: {order_id}
- Total Price: ₹{total_price}
- Delivered To: {shipping_address}

We hope you loved your shopping experience with us 💖  
We would love to hear your feedback!

Thank you once again for choosing {company_name} 🙏

Best Wishes,  
{company_name} Team
"""
}

ORDER_ASSIGNED_EMAIL = {
    "STATUS": "Order Assigned",
    "SUBJECT": "📦 New Order Assigned to You!",
    "MESSAGE": """\
Hi {staff_name},

Good news! A new delivery order has been assigned to you.

🚚 Assignment Details:
- Order ID: _{order_id}_
- Customer Address: _{shipping_address}_
- Staff Type: _{staff_type}_

Please check your delivery dashboard for more instructions and start processing this order as soon as possible.

Let’s keep the delivery smooth and on time! ⏱️

Thanks for your dedication 🙌

Warm Regards,  
_{company_name} Team_
"""
}
