from django.shortcuts import render
from rest_framework import status
from config.connection import get_conn, close_conn
from services.staffService import (
    insert_staff, assign_order_to_delivery_boy
)
from rest_framework.views import APIView
from rest_framework.response import Response
import json

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