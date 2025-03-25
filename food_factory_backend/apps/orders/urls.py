from django.urls import path
from .views import OrderInsertView
# FetchAllOrdersView, FetchOrderByIdView, UpdateOrderStatusView, CancelOrderView

urlpatterns = [
    path('insert/', OrderInsertView.as_view(), name='order-insert'),
    # path('fetchall/', FetchAllOrdersView.as_view(), name='fetchall-orders'),
    # path('fetchorder/', FetchOrderByIdView.as_view(), name='fetchorder-byid'),
    # path('update/', UpdateOrderStatusView.as_view(), name='update-order'),
    # path('cancel/', CancelOrderView.as_view(), name='cancel-order')
]
