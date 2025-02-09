from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.user.users import insert_user, fetchall_users, fetch_user_by_email, send_otp_email, verify_otp, password_reset
from services.db_config.dbConfigService import fetch_db_config_data
from config.connection import get_conn, close_conn
from apps.users.auth_backend import CustomAuthBackend
import json
import jwt
import datetime
from constants.constant import TRUE, FALSE
from food_factory_backend.settings import JWT_SECRET_KEY
from constants.bd_config import REGISTER_AS_ADMIN

def generate_jwt(user):
    """Generate a JWT token for the user"""
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),  # Token expires in 2 hours
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


class UserInsertView(APIView):
    def post(self, request):
        db_connection = get_conn()
        if not db_connection:
            return Response({"error": "Failed to connect to the database"}, status=500)

        try:
            data = request.data
            required_fields = ['username', 'email', 'password', 'role']

            # Check if required fields are missing
            if not all(data.get(field) for field in required_fields):
                return Response({"error": "Missing required fields."}, status=400)

            # Handle Admin role verification
            if data['role'] == 'Admin' and fetch_db_config_data(db_connection, REGISTER_AS_ADMIN) == FALSE:
                return Response({"error": "Failed to create user. Need Admin Permission."}, status=403)

            # Insert user logic
            user_insert_result = insert_user(db_connection, data)

            if user_insert_result == "email already exists":
                return Response({"error": "Email already exists."}, status=400)
            elif user_insert_result:
                return Response({"message": "User created successfully."}, status=201)
            else:
                return Response({"error": "Failed to create user."}, status=500)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class FetchAllUserView(APIView):
    def get(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)
            else:
                data = fetchall_users(db_connection)
                if data:
                    return Response({"message": "User fetched successfully", "data": data}, status=200)
                else:
                    return Response({"error": "Failed to fetch users."}, status=500)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class FetchUserByEmailView(APIView):
    def get(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)
            else:
                email = request.GET.get('email')
                if not email:
                    return Response({"error": "Email parameter is required"}, status=400)
                data = fetch_user_by_email(db_connection,email)
                if data:
                    return Response({"message": "User fetched successfully", "data": data}, status=200)
                else:
                    return Response({"error": "Failed to fetch users."}, status=500)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class SignInUserView(APIView):
    def post(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)

            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            user, error_message = CustomAuthBackend().authenticate(request, db_connection, email=email, password=password)

            if error_message:
                return Response({"error": error_message}, status=401)  # ✅ Return specific error messages

            if user: 
                token = generate_jwt(user)
                return Response({"message": "Login successful", "token": token}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class ForgotPasswordView(APIView):
    def post(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)
            
            email = request.data.get("email")
            
            user = fetch_user_by_email(db_connection,email)
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            otp, error_msg = send_otp_email(db_connection, email)
            if error_msg:
                return Response({"error": error_message}, status=401)

            return Response({"message": "OTP sent successfully", "OTP": otp}, status=status.HTTP_200_OK)
        
        except Exception as e:
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

            return Response({"success": True, "message": "OTP verified successfully!"}, status=200)

        except Exception as e:
            return Response({"success": False, "message": "An error occurred.", "error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
                
class ResetPasswordView(APIView):
    def post(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"success": False, "message": "Database connection failed"}, status=500)
            
            isPasswordReset = password_reset(db_connection, request)

            if not isPasswordReset:
                return Response({"success": False, "message": "Something went wrong. Try again later!"}, status=400)

            return Response({"success": True, "message": "Password reset successfully!"}, status=200)
            
        except Exception as e:
            return Response({"success": False, "message": "An error occurred.", "error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

        