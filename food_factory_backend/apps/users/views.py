from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.user.users import insert_user, fetchall_users ,fetch_user_by_email
from config.connection import get_conn, close_conn


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
            print(request)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)


