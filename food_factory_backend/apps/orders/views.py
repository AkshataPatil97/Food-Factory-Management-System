from django.shortcuts import render
from config.connection import get_conn, close_conn
from services.orderService import (
    insert_order,insert_order_details
    # fetch_all_orders, fetch_order_by_id, 
    # update_order, delete_order
)
from rest_framework.views import APIView
from rest_framework.response import Response
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




# class FetchAllOrdersView(APIView):
#     def get(self, request):
#         db_connection = None
#         try:
#             db_connection = get_conn()
#             if not db_connection:
#                 return Response({"error": "Failed to connect to the database"}, status=500)
            
#             data = fetch_all_orders(db_connection)
#             if data:
#                 return Response({"message": "Orders fetched successfully", "data": data}, status=200)
#             else:
#                 return Response({"error": "Failed to fetch orders."}, status=500)
        
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)
        
#         finally:
#             if db_connection:
#                 close_conn(db_connection)

# class FetchOrderByIdView(APIView):
#     def get(self, request):
#         db_connection = None
#         try:
#             db_connection = get_conn()
#             if not db_connection:
#                 return Response({"error": "Failed to connect to the database"}, status=500)

#             order_id = request.GET.get('order_id')
#             if not order_id:
#                 return Response({"error": "Order ID parameter is required"}, status=400)

#             data = fetch_order_by_id(db_connection, order_id)
#             if data:
#                 return Response({"message": "Order fetched successfully", "data": data}, status=200)
#             else:
#                 return Response({"error": "Failed to fetch order."}, status=404)

#         except Exception as e:
#             return Response({"error": str(e)}, status=500)

#         finally:
#             if db_connection:
#                 close_conn(db_connection)

# class DeleteOrderByIdView(APIView):
#     def delete(self, request):
#         db_connection = None
#         try:
#             db_connection = get_conn()
#             if not db_connection:
#                 return Response({"error": "Failed to connect to the database"}, status=500)

#             order_id = request.GET.get('order_id')
#             if not order_id:
#                 return Response({"error": "Order ID parameter is required"}, status=400)

#             success = delete_order(db_connection, order_id)
#             if success:
#                 return Response({"message": "Order marked as deleted successfully"}, status=200)
#             else:
#                 return Response({"error": "Failed to delete order. It may not exist."}, status=404)

#         except Exception as e:
#             return Response({"error": str(e)}, status=500)

#         finally:
#             if db_connection:
#                 close_conn(db_connection)

# class UpdateOrderView(APIView):
#     def put(self, request):
#         db_connection = None
#         try:
#             db_connection = get_conn()
#             if not db_connection:
#                 return Response({"error": "Failed to connect to the database"}, status=500)

#             data = request.data
#             order_id = data.get("order_id")
#             if not order_id:
#                 return Response({"error": "Order ID is required for updating"}, status=400)

#             success = update_order(db_connection, request, order_id)

#             if success:
#                 return Response({"message": "Order updated successfully"}, status=200)
#             else:
#                 return Response({"error": "No changes made or order not found."}, status=404)

#         except Exception as e:
#             return Response({"error": str(e)}, status=500)

#         finally:
#             if db_connection:
#                 close_conn(db_connection)