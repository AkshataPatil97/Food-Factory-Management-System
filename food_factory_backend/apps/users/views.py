from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.users import insert_user, fetchall_users, fetch_user_by_email, send_otp_email, verify_otp, password_reset, insert_dealer_details, fetch_dealer_details, update_dealer_details, fetch_user_details, insert_admin_details
from services.dbConfigService import fetch_db_config_data, update_db_config_data
from config.connection import get_conn, close_conn
from apps.users.auth_backend import CustomAuthBackend
import json
import jwt
import datetime
from constants.constant import TRUE, FALSE
from food_factory_backend.settings import JWT_SECRET_KEY
from constants.bd_config import REGISTER_AS_ADMIN
from logger import LOGGER

def generate_jwt(user):
    """Generate a JWT token for the user"""
    payload = {
        "user_id": user["id"],
        "user_name": user["username"],
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),  # Token expires in 2 hours
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


class UserInsertView(APIView):
    def post(self, request):
        LOGGER.info("Inside UserInsertView")
        db_connection = get_conn()
        if not db_connection:
            LOGGER.error("Failed to connect to the database")
            return Response({"error": "Failed to connect to the database"}, status=500)

        try:
            data = request.data
            required_fields = ['username', 'email', 'password', 'role']

            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                return Response({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

            user_insert_result = insert_user(db_connection, data)

            if not user_insert_result["success"]:
                error_message = user_insert_result.get("error", "Failed to create user.")
                if error_message == "email already exists":
                    return Response({"error": "Email already exists."}, status=400)
                return Response({"error": error_message}, status=500)

            LOGGER.info(f"User_id -- ", user_insert_result.get("user_id"))
            user_id = user_insert_result.get("user_id")

            if data.get("role") == "Dealer" and user_id:
                insert_dealer_details(db_connection, user_id)

            if data.get("role") == "Admin" and user_id:
                insert_admin_details(db_connection, user_id)

            return Response({"message": "User created successfully.", "user_id": user_id}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            close_conn(db_connection)


class FetchAllUserView(APIView):
    def get(self, request):
        LOGGER.info("Inside FetchAllUserView")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                LOGGER.error("Failed to connect to the database")
                return Response({"error": "Failed to connect to the database"}, status=500)
            else:
                data = fetchall_users(db_connection)
                if data:
                    LOGGER.info("FetchAllUserView END...")
                    return Response({"message": "User fetched successfully", "data": data}, status=200)
                else:
                    return Response({"error": "Failed to fetch users."}, status=500)
        except Exception as e:
            LOGGER.error("Error in FetchAllUserView",{"error": str(e)})
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class FetchUserByEmailView(APIView):
    def get(self, request):
        LOGGER.info("Inside FetchUserByEmailView!")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                LOGGER.error("Failed to connect to the database")
                return Response({"error": "Failed to connect to the database"}, status=500)
            else:
                email = request.GET.get('email')
                if not email:
                    LOGGER.error("Error in authentication : ", error_message)
                    return Response({"error": "Email parameter is required"}, status=400)
                data = fetch_user_by_email(db_connection,email)
                if data:
                    LOGGER.info("FetchUserByEmailView END...")
                    return Response({"message": "User fetched successfully", "data": data}, status=200)
                else:
                    return Response({"error": "Failed to fetch users."}, status=500)
        except Exception as e:
            LOGGER.error("Error in FetchUserByEmailView",{"error": str(e)})
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class SignInUserView(APIView):
    def post(self, request):
        LOGGER.info("Inside SignInUserView!")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                LOGGER.error("Failed to connect to the database")
                return Response({"error": "Failed to connect to the database"}, status=500)

            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            user, error_message = CustomAuthBackend().authenticate(request, db_connection, email=email, password=password)

            if error_message:
                LOGGER.error("Error in authentication : ", error_message)
                return Response({"error": error_message}, status=401)  # ✅ Return specific error messages

            if user: 
                token = generate_jwt(user)
                LOGGER.info("SignInUserView END...")
                return Response({"message": "Login successful", "token": token}, status=200)

        except Exception as e:
            LOGGER.error("Error in SignInUserView",{"error": str(e)})
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class ForgotPasswordView(APIView):
    def post(self, request):
        LOGGER.info("Inside ForgotPasswordView!")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                LOGGER.error("Failed to connect to the database")
                return Response({"error": "Failed to connect to the database"}, status=500)
            
            email = request.data.get("email")
            
            user = fetch_user_by_email(db_connection,email)
            if not user:
                LOGGER.info("ForgotPasswordView END...")
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            otp, error_msg = send_otp_email(db_connection, email)
            if error_msg:
                LOGGER.error("Error in authentication : ", error_message)
                return Response({"error": error_message}, status=401)

            return Response({"message": "OTP sent successfully", "OTP": otp}, status=status.HTTP_200_OK)
        
        except Exception as e:
            LOGGER.error("Error in ForgotPasswordView",{"error": str(e)})
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class VerifyOTPView(APIView):
    def post(self, request):
        LOGGER.info("Inside VerifyOTPView!")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                LOGGER.error("Failed to connect to the database")
                return Response({"success": False, "message": "Database connection failed"}, status=500)

            isVerified = verify_otp(db_connection, request)

            if not isVerified:
                LOGGER.info("VerifyOTPView END...")
                return Response({"success": False, "message": "Invalid OTP or OTP expired. Try again!"}, status=400)

            return Response({"success": True, "message": "OTP verified successfully!"}, status=200)

        except Exception as e:
            LOGGER.error("Error in VerifyOTPView",{"error": str(e)})
            return Response({"success": False, "message": "An error occurred.", "error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
                
class ResetPasswordView(APIView):
    def post(self, request):
        LOGGER.info("Inside ResetPasswordView!")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                LOGGER.error("Failed to connect to the database")
                return Response({"success": False, "message": "Database connection failed"}, status=500)
            
            isPasswordReset = password_reset(db_connection, request)

            if not isPasswordReset:
                LOGGER.info("ResetPasswordView END...")
                return Response({"success": False, "message": "Something went wrong. Try again later!"}, status=400)

            return Response({"success": True, "message": "Password reset successfully!"}, status=200)
            
        except Exception as e:
            LOGGER.error("Error in ResetPasswordView",{"error": str(e)})
            return Response({"success": False, "message": "An error occurred.", "error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class DBConfigView(APIView):
    def post(self, request):
        LOGGER.info("Inside DBConfigView!")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                LOGGER.error("Failed to connect to the database")
                return Response({"error": "Failed to connect to the database"}, status=500)
            
            data = json.loads(request.body)
            db_config = data.get('db_config')
            dbValue = fetch_db_config_data(db_connection, db_config)
            
            if dbValue:
                LOGGER.info("DBConfigView END...")
                return Response({"message": "DB Value fetched successfully", "db_config": dbValue}, status=200)
            
        except Exception as e:
            LOGGER.error("Error in DBConfigView : ", str(e))
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class UpdateDBConfigView(APIView):
    def post(self, request):
        LOGGER.info("Inside UpdateDBConfigView!")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                LOGGER.error("Failed to connect to the database")
                return Response({"error": "Failed to connect to the database"}, status=500)
            
            success = update_db_config_data(db_connection, request)
            LOGGER.info(success)
            if success:
                LOGGER.info("DB Config data updated successfully")
                return Response({"success": True, "message": "DB Config data updated successfully"}, status=200)
            else:
                LOGGER.info("No changes made")
                return Response({"success": False, "error": "No changes made"}, status=404)
            
        except Exception as e:
            LOGGER.error("Error in DBConfigView : ", str(e))
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
                
class FetchDealerDetailsView(APIView):
    def post(self, request):
        LOGGER.info("Inside FetchDealerDetailsView!")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                LOGGER.error("Failed to connect to the database")
                return Response({"error": "Failed to connect to the database"}, status=500)
            
            fetchedDealerDetails = fetch_dealer_details(db_connection, request)
            fetchedUserDetails = fetch_user_details(db_connection, request) 
            fetchedDetails = {**fetchedDealerDetails, **fetchedUserDetails}

            if fetchedDetails:
                return Response({"message": "Dealer fetched successfully.", "dealer_details": fetchedDetails }, status=201)
        except Exception as e:
            LOGGER.error("Error in DBConfigView : ", str(e))
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
                
class UpdateDealerDetailsView(APIView):
    def post(self, request):
        LOGGER.info("Inside UpdateDealerDetailsView!")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                LOGGER.error("Failed to connect to the database")
                return Response({"error": "Failed to connect to the database"}, status=500)
            
            # if request.body.get('email')
            updateDetails = update_dealer_details(db_connection, request)
            if updateDetails:
                LOGGER.info("Dealer details updated successfully.")
                return Response({"message": "Dealer details updated successfully.", "user_id": updateDetails}, status=200)
        except Exception as e:
            LOGGER.error("Error in DBConfigView : ", str(e))
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
        
class FetchUserDetailsView(APIView):
    def post(self, request):
        LOGGER.info("Inside FetchUserDetailsView!")
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                LOGGER.error("Failed to connect to the database")
                return Response({"error": "Failed to connect to the database"}, status=500)
            
            fetchedUserDetails = fetch_user_details(db_connection, request) 

            if fetchedUserDetails:
                return Response({"message": "User feached successfully.", "user_details": fetchedUserDetails }, status=201)
        except Exception as e:
            LOGGER.error("Error in DBConfigView : ", str(e))
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)