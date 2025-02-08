from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.user.users import insert_user, fetchall_users, fetch_user_by_email, send_otp_email
from config.connection import get_conn, close_conn
from apps.users.auth_backend import CustomAuthBackend
import json
import jwt
import datetime
from food_factory_backend.settings import JWT_SECRET_KEY

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
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)
            else:
                data = request.data
                print('User data - ',data)
                if not all([data.get('username'), data.get('email'), data.get('password'), data.get('role')]):
                    return Response({"error": "Missing required fields."}, status=400)

                isUserInsert = insert_user(db_connection, data)
                if isUserInsert == "email already exists":
                    return Response({"error": "Email already exists."}, status=400)
                elif isUserInsert:
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
            print(request)
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
