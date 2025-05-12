from django.shortcuts import render
from config.connection import get_conn, close_conn
from constants.constant import  (
    SHIPPED_EMAIL,
    ORDER_PLACED_EMAIL,
    ORDER_CANCELLED_EMAIL,
    ORDER_PROCESSING_EMAIL,
    ORDER_PROCESSED_EMAIL,
    DELIVERED_EMAIL
)
from services.orderService import (
    insert_order,insert_order_details,fetch_orders_by_userId,
    cancel_order, update_order, update_order_items, fetch_all_order,
    update_order_status, fetch_delivered_order, fetch_canceled_order,
    update_shipped_order_status, fetch_order_by_id
)
from services.invoiceService import invoice_details, fetch_invoices_user_id, fetch_all_invoices, update_invoice_status_to_paid
from services.sendemail import send_order_status_email
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

            # Call insert_order and check response
            order_response = insert_order(db_connection, request)
            
            if not order_response.get("success"):
                # Return the exact error message from insert_order
                return Response({"error": order_response.get("message")}, status=400)

            order_id = order_response.get("order_id")
            user_id = request.data.get('user_id')

            order_details_response = insert_order_details(db_connection, order_id, request)
            if "error" in order_details_response:
                return Response(order_details_response, status=500)
            
            invoice_id = invoice_details(db_connection, order_id, user_id)
            if invoice_id:
                return Response({"message": "Order inserted successfully", "order_id": order_id}, status=201)
            
            return Response({"error": "Failed to generate invoice"}, status=500)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            if db_connection:
                close_conn(db_connection)

class FetchAllOrdersIdView(APIView):
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
            if db_connection is not None:
                close_conn(db_connection)

                
class CancelOrderView(APIView):
    def post(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)

            result = cancel_order(db_connection, request)
            update_invoice_status_to_paid(db_connection, "Cancelled", request.data.get("order_id"))
            STATUS_EMAIL_MAP = {
                "Placed": ORDER_PLACED_EMAIL,
                "Cancelled": ORDER_CANCELLED_EMAIL,
                "Processing": ORDER_PROCESSING_EMAIL,
                "Processed": ORDER_PROCESSED_EMAIL,
                "Shipped": SHIPPED_EMAIL,
                "Delivered": DELIVERED_EMAIL
            }
            email_template = STATUS_EMAIL_MAP.get("Cancelled")
            if email_template:
                    send_order_status_email(request, email_template)
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

class FetchAllOrdersView(APIView):
    def get(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)

            data = fetch_all_order(db_connection)
            if data:
                return Response({
                    "message": "Orders fetched successfully",
                    "data": data
                }, status=200)
            else:
                return Response({
                    "message": "No orders found",
                    "data": []
                }, status=200)

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
            if not status:
                return Response({"error": "Order status is required"}, status=400)

            # Map status to corresponding email templates
            STATUS_EMAIL_MAP = {
                "Placed": ORDER_PLACED_EMAIL,
                "Cancelled": ORDER_CANCELLED_EMAIL,
                "Processing": ORDER_PROCESSING_EMAIL,
                "Processed": ORDER_PROCESSED_EMAIL,
                "Shipped": SHIPPED_EMAIL,
                "Delivered": DELIVERED_EMAIL
            }

            email_template = STATUS_EMAIL_MAP.get(status)

            if status == "Shipped":
                success = update_shipped_order_status(db_connection, request)
            else:
                success = update_order_status(db_connection, request)

            if success.get("success"):
                # If an email template exists for the status, send email
                if email_template:
                    send_order_status_email(request, email_template)

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
                return Response({
                    "message": "Orders fetched successfully",
                    "data": data
                }, status=200)
            else:
                return Response({
                    "message": "No delivered orders found",
                    "data": []
                }, status=200)

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
                return Response({"error": "Database connection failed"}, status=500)

            data = fetch_canceled_order(db_connection)
            if data:
                return Response({
                    "message": "Orders fetched successfully",
                    "data": data
                }, status=200)
            else:
                return Response({
                    "message": "No canceled orders found",
                    "data": []
                }, status=200)

        except Exception as e:
            return Response({"error": f"Server error: {str(e)}"}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
                
                
class FetchDeliveryOrdersView(APIView):
    def post(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Database connection failed"}, status=500)

            # Parsing the JSON body of the request
            try:
                data = json.loads(request.body)  # Parse raw request body to JSON
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON in request body"}, status=400)

            order_id = data.get("order_id")
            if not order_id:
                return Response({"error": "order_id is required"}, status=400)

            # Fetch the order using the order_id
            order_data = fetch_order_by_id(db_connection, order_id)

            if order_data:
                return Response({
                    "message": "Orders fetched successfully",
                    "data": order_data
                }, status=200)
            else:
                return Response({
                    "message": "No orders found",
                    "data": {}
                }, status=404)

        except Exception as e:
            return Response({"error": f"Server error: {str(e)}"}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

                
class FetchUserInvoicesView(APIView):
    def post(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Database connection failed"}, status=500)

            invoices = fetch_invoices_user_id(db_connection, request)

            if invoices:
                return Response({
                        "message": "Invoices fetched successfully",
                        "data": invoices
                    }, status=200)
            
            return Response({
                    "message": "Invoices fetched successfully",
                    "data": []
                }, status=200)

        except Exception as e:
            return Response({"error": f"Server error: {str(e)}"}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
                
class FetchAllInvoices(APIView):
    def get(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Database connection failed"}, status=500)

            invoices = fetch_all_invoices(db_connection,)

            if invoices:
                return Response({
                        "message": "Invoices fetched successfully",
                        "data": invoices
                    }, status=200)
            
            return Response({
                    "message": "Invoices fetched successfully",
                    "data": []
                }, status=200)

        except Exception as e:
            return Response({"error": f"Server error: {str(e)}"}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)