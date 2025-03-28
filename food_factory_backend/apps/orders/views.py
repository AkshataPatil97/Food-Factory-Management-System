from django.shortcuts import render
from config.connection import get_conn, close_conn
from constants.constant import SHIPPED_EMAIL
from services.orderService import (
    insert_order,insert_order_details,fetch_orders_by_userId,
    cancel_order, update_order, update_order_items, fetch_all_order,
    update_order_status, fetch_delivered_order, fetch_canceled_order,
    update_shipped_order_status
)
from services.sendemail import send_shipped_email
from rest_framework.views import APIView
from rest_framework.response import Response
import json

class OrderInsertView(APIView):
    def post(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)

            order_id = insert_order(db_connection, request)
            if order_id:
                order_details_response = insert_order_details(db_connection, order_id, request)
                if "error" in order_details_response:
                    return Response(order_details_response, status=500)
                
                return Response({"message": "Order inserted successfully", "order_id": order_id}, status=201)
            else:
                return Response({"error": "Failed to insert order"}, status=500)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            if db_connection:
                close_conn(db_connection)

class FetchAllOrdersView(APIView):
    def post(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)
            
            data = fetch_orders_by_userId(db_connection, request)
            if data:
                return Response({"message": "Orders fetched successfully", "data": data}, status=200)
            else:
                return Response({"message": "No orders found", "data": {"orders": []}}, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
        finally:
            if db_connection:
                close_conn(db_connection)
                
class CancelOrderView(APIView):
    def post(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)

            result = cancel_order(db_connection, request)

            if "error" in result:
                return Response(result, status=400)
            return Response(result, status=200)

        finally:
            if db_connection:
                close_conn(db_connection)


class OrderUpdateView(APIView):
    def put(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)

            data = json.loads(request.body)
            order_id = data.get("order_id")

            if not order_id:
                return Response({"error": "Order ID is required for update"}, status=400)

            update_order_response = update_order(db_connection, data)
            if "error" in update_order_response:
                return Response(update_order_response, status=500)

            update_order_items_response = update_order_items(db_connection, order_id, data)
            if "error" in update_order_items_response:
                return Response(update_order_items_response, status=500)

            return Response({"message": "Order updated successfully"}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class FetchAllOrdersIdView(APIView):
    def get(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)

            data = fetch_all_order(db_connection)
            if data:
                return Response({"message": "Orders fetched successfully", "data": data}, status=200)
            else:
                return Response({"error": "Failed to fetch order."}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class UpdateOrderStatusView(APIView):
    def put(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)

            status = request.data.get("status")

            if status == "Shipped":
                success = update_shipped_order_status(db_connection, request)
                if success.get("success"):
                    send_shipped_email(request, SHIPPED_EMAIL)
            else:
                success = update_order_status(db_connection, request)

            if success.get("success"):
                return Response({"message": success["message"]}, status=200)
            else:
                return Response({"error": success.get("error", "No changes made or order not found.")}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
                
class FetchAllDeleiveredOrdersView(APIView):
    def get(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)

            data = fetch_delivered_order(db_connection)
            if data:
                return Response({"message": "Orders fetched successfully", "data": data}, status=200)
            else:
                return Response({"error": "Failed to fetch order."}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
                
class FetchAllCanceledOrdersView(APIView):
    def get(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)

            data = fetch_canceled_order(db_connection)
            if data:
                return Response({"message": "Orders fetched successfully", "data": data}, status=200)
            else:
                return Response({"error": "Failed to fetch order."}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
                