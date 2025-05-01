from django.core.mail import send_mail
from .orderService import fetch_order_by_id
from .staffService import fetch_staff_by_id
from config.connection import get_conn, close_conn
from django.conf import settings
from logger import LOGGER
from constants.constant import (ORDER_ASSIGNED_EMAIL)

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
        LOGGER.error(f"Error sending email: {str(e)}")

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

def send_order_status_email(request, STATUS_EMAIL_TEMPLATE):
    try:
        from services.users import fetch_user_by_id, fetch_dealer_details_by_id
        db_connection = get_conn()

        order_id = request.data.get("order_id")
        staff_id = request.data.get("staff_id")

        if not order_id:
            return {"error": "Order ID is required"}

        # Fetch order
        order = fetch_order_by_id(db_connection, order_id)
        if not order:
            return {"error": "Order not found"}

        # Fetch user
        user = fetch_user_by_id(db_connection, order["user_id"])
        if not user:
            return {"error": "User not found"}

        # Fetch user details (for address)
        user_details = fetch_dealer_details_by_id(db_connection, order["user_id"])
        if not user_details:
            return {"error": "User details not found"}

        # Extract shipping address
        address_payload = user_details.get("address_payload", "{}")
        shipping_address = format_address(address_payload)

        # Fetch staff only if needed (optional for some statuses)
        delivery_boy_name = ""
        delivery_boy_phone = ""
        if staff_id:
            staff = fetch_staff_by_id(db_connection, staff_id)
            if staff:
                delivery_boy_name = staff.get("name", "")
                delivery_boy_phone = staff.get("phone", "")

        # Format email message
        email_message = STATUS_EMAIL_TEMPLATE["MESSAGE"].format(
            customer_name=user["username"],
            order_id=order["order_id"],
            total_price=order["total_price"],
            shipping_address=shipping_address,
            delivery_boy_name=delivery_boy_name,
            delivery_boy_phone=delivery_boy_phone,
            company_name="Jayashree Food Products",  
        )

        # Send email
        send_email(
            subject=STATUS_EMAIL_TEMPLATE["SUBJECT"],
            message=email_message,
            recipient_list=[user["email"]]
        )

        return {"success": True, "message": f"{STATUS_EMAIL_TEMPLATE['STATUS']} email sent successfully"}

    except Exception as e:
        LOGGER.error(f"Error sending email: {str(e)}")
        return {"error": str(e)}
    finally:
        if db_connection:
            close_conn(db_connection)


def send_order_assignment_email(staff, order_id):
    
    try:
        from services.users import fetch_user_by_id, fetch_dealer_details_by_id
        db_connection = get_conn()

        if not order_id:
            return {"error": "Order ID is required"}

        # Fetch order
        order = fetch_order_by_id(db_connection, order_id)
        if not order:
            return {"error": "Order not found"}

        # Fetch user
        user = fetch_user_by_id(db_connection, order["user_id"])
        if not user:
            return {"error": "User not found"}

        # Fetch user details (for address)
        user_details = fetch_dealer_details_by_id(db_connection, order["user_id"])
        if not user_details:
            return {"error": "User details not found"}

        # Extract shipping address
        address_payload = user_details.get("address_payload", "{}")
        shipping_address = format_address(address_payload)
        
        message = ORDER_ASSIGNED_EMAIL["MESSAGE"].format(
            staff_name=staff['name'],
            order_id=order_id,
            shipping_address=shipping_address,
            staff_type=staff['staff_type'],
            company_name="Jayashree Food Products", 
        )

        send_mail(
            subject=ORDER_ASSIGNED_EMAIL["SUBJECT"],
            message=message,
            recipient_list=[staff["email"]]
        )
    
    except Exception as e:
        LOGGER.error(f"Error sending email: {str(e)}")
        return {"error": str(e)}
    finally:
        if db_connection:
            close_conn(db_connection)