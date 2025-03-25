from django.shortcuts import render
from config.connection import get_conn, close_conn
from services.productService import insert_product, fetchall_products, fetch_product_by_code, delete_product, update_product
from rest_framework.views import APIView
from rest_framework.response import Response

class ProductInsertView(APIView):
    def post(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)
            isProductInsert = insert_product(db_connection, request)
            if isProductInsert:
                return Response({"message": "Product inserted successfully."}, status=201)
            else:
                return Response({"error": "Failed to insert product."}, status=500)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

class FetchAllProductView(APIView):
    def get(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)
            else:
                data = fetchall_products(db_connection)
                if data:
                    return Response({"message": "Product fetched successfully", "data": data}, status=200)
                else:
                    return Response({"error": "Failed to fetch products."}, status=500)       
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)


class FetchProductByCodeView(APIView):
    def get(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)
            else:
                code = request.GET.get('code')
                if not code:
                    return Response({"error": "Code parameter is required"}, status=400)
                data = fetch_product_by_code(db_connection,code)
                if data:
                    return Response({"message": "Product fetched successfully", "data": data}, status=200)
                else:
                    return Response({"error": "Failed to fetch product."}, status=500)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
                
class DeleteProductByCodeView(APIView):
    def delete(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)

            code = request.GET.get('code')
            if not code:
                return Response({"error": "Code parameter is required"}, status=400)

            success = delete_product(db_connection, code)
            if success:
                return Response({"message": "Product marked as deleted successfully"}, status=200)
            else:
                return Response({"error": "Failed to delete product. It may not exist."}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)

                
class UpdateProductView(APIView):
    def put(self, request):
        db_connection = None
        try:
            db_connection = get_conn()
            if not db_connection:
                return Response({"error": "Failed to connect to the database"}, status=500)

            data = request.data
            product_code = data.get("product_code")
            if not product_code:
                return Response({"error": "Product code is required for updating"}, status=400)

            success = update_product(db_connection, request, product_code)

            if success:
                return Response({"message": "Product updated successfully"}, status=200)
            else:
                return Response({"error": "No changes made or product not found."}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        finally:
            if db_connection:
                close_conn(db_connection)
