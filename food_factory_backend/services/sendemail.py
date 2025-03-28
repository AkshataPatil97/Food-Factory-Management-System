from django.core.mail import send_mail
from .orderService import fetch_order_by_id
from .staffService import fetch_staff_by_id
from config.connection import get_conn, close_conn
from django.conf import settings
from logger import LOGGER

def send_email(subject, message, recipient_list, sender=None):
    if sender is None:
        sender = settings.DEFAULT_FROM_EMAIL

    try:
        LOGGER.info(f"Inside send_email! {recipient_list}")

        send_mail(
            subject,
            message,
            sender,
            recipient_list,
            fail_silently=False  
        )
    except Exception as e:
        LOGGER.error(f"Error sending email:{str(e)}")

def send_shipped_email(request, SHIPPED_EMAIL):
    try:
        from services.users import fetch_user_by_id, fetch_dealer_details_by_id
        db_connection = get_conn()
        order_id = request.data.get("order_id")
        staff_id = request.data.get("staff_id")

        if not order_id or not staff_id:
            return {"error": "Order ID and Staff ID are required"}

        # Fetch details from DB
        order = fetch_order_by_id(db_connection, order_id)
        if not order:
            return {"error": "Order not found"}
        
        user = fetch_user_by_id(db_connection, order["user_id"])
        if not user:
            return {"error": "User not found"}

        user_details = fetch_dealer_details_by_id(db_connection, order["user_id"])
        if not user_details:
            return {"error": "User details not found"}

        staff = fetch_staff_by_id(db_connection, staff_id)
        if not staff:
            return {"error": "Delivery staff not found"}

        # Extract shipping address from user_details
        address_payload = user_details.get("address_payload", "{}")
        shipping_address = format_address(address_payload)

        # Populate email message
        email_message = SHIPPED_EMAIL["MESSAGE"].format(
            customer_name=user["username"],
            order_id=order["order_id"],
            total_price=order["total_price"],
            shipping_address=shipping_address,
            delivery_boy_name=staff["name"],
            delivery_boy_phone=staff["phone"],
            company_name="Your Company Name"
        )

        # Send email
        send_email(
            subject=SHIPPED_EMAIL["SUBJECT"],
            message=email_message,
            recipient_list=[user["email"]]
        )

        return {"success": True, "message": "Shipped email sent successfully"}

    except Exception as e:
        LOGGER.error(f"Error sending email: {str(e)}")
        return {"error": str(e)}
    finally:
        if db_connection:
            close_conn(db_connection)

def format_address(address_payload):
    """Parse and format address payload from JSON string."""
    import json
    
    try:
        address = json.loads(address_payload)
        formatted_address = (
            f"{address.get('street', 'N/A')}, {address.get('landmark', 'N/A')}, "
            f"{address.get('city', 'N/A')}, {address.get('state', 'N/A')} - {address.get('zip', 'N/A')}"
        )
        return formatted_address
    except json.JSONDecodeError:
        return "Invalid Address Format"