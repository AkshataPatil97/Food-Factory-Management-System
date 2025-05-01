from django.shortcuts import render
from rest_framework import status
from config.connection import get_conn, close_conn
from services.staffService import (
    insert_staff, assign_order_to_delivery_boy, fetch_all_delivery_staff, fetch_all_staff, update_staff,
    delete_staff, send_otp_email
)
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from apps.users.auth_backend import CustomAuthBackend
import jwt
import datetime
from food_factory_backend.settings import JWT_SECRET_KEY
from services.users import verify_otp
from services.orderService import update_order_status

def generate_jwt(user):
    """Generate a JWT token for the user or staff"""
    payload = {
        "user_id": user["id"],
        "user_name": user.get("username", user.get("name", "")),  
        "email": user.get("email", ""), 
        "order_id": user.get("order_id"), 
        "phone": user.get("phone", ""),  
        "role": user.get("role", user.get("staff_type", "staff")),  
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),  
        "iat": datetime.datetime.utcnow()
    }
   
    try:
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
        return token
    except Exception as e:
        print("JWT Encoding Error:", e)
        raise e  # Re-raise the error for full traceback


class StaffInsertView(APIView):
    def post(self, request):
        db_connection = None
        try:
            # Establish database connection
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Insert staff into the database
            response_data, status_code = insert_staff(db_connection, request)

            return Response(response_data, status=status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            if db_connection:
                close_conn(db_connection)

class AssignOrderToDeliveryBoyView(APIView):
    def post(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            data = request.data
            staff_id = data.get("staff_id")
            order_id = data.get("order_id")

            # Validate input
            if not staff_id or not order_id:
                return Response({"error": "staff_id and order_id are required"}, status=status.HTTP_400_BAD_REQUEST)

            response_data, status_code = assign_order_to_delivery_boy(db_connection, staff_id, order_id)

            return Response(response_data, status=status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            if db_connection:
                close_conn(db_connection)
                
class FetchAllDeliveryStaffView(APIView):
    def get(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            staff_members = fetch_all_delivery_staff(db_connection)

            if not staff_members:
                return Response({"message": "No staff members found", "staff": []}, status=status.HTTP_200_OK)

            return Response({"staff": staff_members}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            if db_connection:
                close_conn(db_connection)

class FetchAllDStaffView(APIView):
    def get(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            staff_members = fetch_all_staff(db_connection)

            if not staff_members:
                return Response({"message": "No staff members found", "staff": []}, status=status.HTTP_200_OK)

            return Response({"staff": staff_members}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            if db_connection:
                close_conn(db_connection)
                
class StaffUpdateView(APIView):
    def put(self, request):
        db_connection = None
        try:
            # Establish database connection
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Update staff in the database
            data = request.data
            staff_id = data.get("id")
            response_data, status_code = update_staff(db_connection, staff_id, request)

            return Response(response_data, status=status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            if db_connection:
                close_conn(db_connection)

class StaffDeleteView(APIView):
    def put(self, request):
        db_connection = None
        try:
            # Establish database connection
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Update staff in the database
            data = request.data
            staff_id = data.get("id")
            
            response_data, status_code = delete_staff(db_connection, staff_id)

            return Response(response_data, status=status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            if db_connection:
                close_conn(db_connection)

class StaffSignInView(APIView):
    def post(self, request):
        # LOGGER.info("Inside StaffSignInView!")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                # LOGGER.error("Failed to connect to the database")
                return Response({"error": "Failed to connect to the database"}, status=500)

            data = json.loads(request.body)
            phone_number = data.get('number')
            
            if not phone_number:
                return Response({"error": "Phone number is required"}, status=400)

            user, error_message = CustomAuthBackend().authenticate_staff(request, db_connection, phone_number=phone_number)

            if error_message:
                # LOGGER.error("Error in authentication: %s", error_message)
                return Response({"error": error_message}, status=401)
            
            if user:
                token = generate_jwt(user)
                # LOGGER.info("StaffSignInView END...")
                return Response({"message": "Login successful", "token": token}, status=200)

        except Exception as e:
            # LOGGER.error("Error in StaffSignInView: %s", str(e))
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class SendOTPToDealerView(APIView):
     def post(self, request):
        # LOGGER.info("Inside StaffSignInView!")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                # LOGGER.error("Failed to connect to the database")
                return Response({"error": "Failed to connect to the database"}, status=500)

            data = json.loads(request.body)
            email = data.get('email')
            print(email)
            otp , error = send_otp_email(db_connection, email)
            
            if otp:
                return Response({"message": "OTP sent successfully"}, status=200)

            if error:
                return Response({"message": error}, status=500)
            
        except Exception as e:
            # LOGGER.error("Error in StaffSignInView: %s", str(e))
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
                
class VerifyOTPView(APIView):
    def post(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"success": False, "message": "Database connection failed"}, status=500)

            isVerified = verify_otp(db_connection, request)

            if not isVerified:
                return Response({"success": False, "message": "Invalid OTP or OTP expired. Try again!"}, status=400)

            update_order_status(db_connection, request)

            staff_id = request.data.get('staff_id')
            if not staff_id:
                return Response({"success": False, "message": "Staff ID is required"}, status=400)

            assign_order_to_delivery_boy(db_connection, staff_id, None)  # This sets order_id to NULL

            db_connection.commit()  # Ensure all changes are committed together
            return Response({"success": True, "message": "OTP verified successfully!"}, status=200)

        except Exception as e:
            db_connection.rollback()  # Rollback on error
            return Response({"success": False, "message": "An error occurred.", "error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
