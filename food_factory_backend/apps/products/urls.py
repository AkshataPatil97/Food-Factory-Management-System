from django.urls import path
from .views import ProductInsertView, FetchAllProductView, FetchProductByCodeView, UpdateProductView, DeleteProductByCodeView

urlpatterns = [
    path('insert/', ProductInsertView.as_view(), name='product-insert'),
    path('fetchall/', FetchAllProductView.as_view(), name='fetchall-product'),
    path('fetchproduct/', FetchProductByCodeView.as_view(), name='fetchproduct-bycode'),
    path('update/', UpdateProductView.as_view(), name='update-product'),
    path('delete/', DeleteProductByCodeView.as_view(), name='delete_product')
]
