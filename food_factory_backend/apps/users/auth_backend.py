# from django.db import connection
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from constants.queries import FETCH_USER_BY_EMAIL
from services.user.users import fetch_user_by_email
from services.passwordencrypt.passwordencrypt import decrypt_password 
from logger import LOGGER

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, connection, email=None, password=None, **kwargs):
        LOGGER.info("Inside CustomAuthBackend!")
        if not connection:  
            LOGGER.info("Database connection is None!")
            return None, "Database connection failed"  

        with connection.cursor() as cursor:
            user = fetch_user_by_email(connection, email)

            if not user:
                LOGGER.info("User Not Found")
                return None, "User Not Found. Please sign up."  

            decrypted_password = decrypt_password(user["password"])

            if password != decrypted_password:
                LOGGER.info("Incorrect Password")
                return None, "Incorrect password. Please try again."  

            LOGGER.info("User Authenticated...")
            return user, None  
