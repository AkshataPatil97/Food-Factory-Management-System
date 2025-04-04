from django.urls import path
from .views import( 
    OrderInsertView, FetchAllOrdersView,CancelOrderView,OrderUpdateView,
    FetchAllOrdersIdView,UpdateOrderStatusView,FetchAllCanceledOrdersView,FetchAllDeleiveredOrdersView,
    FetchUserInvoicesView, FetchDeliveryOrdersView, FetchAllInvoices
)

urlpatterns = [
    path('insert/', OrderInsertView.as_view(), name='order-insert'),
    path('fetchall/userOrders/', FetchAllOrdersIdView.as_view(), name='fetchall-user-orders'),
    path('fetchAllOrder/', FetchAllOrdersView.as_view(), name='fetchorder-byid'),
    path('updateOrder/', OrderUpdateView.as_view(), name='update-order'),
    path('cancelOrder/', CancelOrderView.as_view(), name='cancel-order'),
    path('updateOrderStatus/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('fetchAllDeliveredOrder/', FetchAllDeleiveredOrdersView.as_view(), name='fetch-all-delivered-order'),
    path('fetchAllCancelledOrder/', FetchAllCanceledOrdersView.as_view(), name='fetch-all-cancelled-order'),
    path('fetchUserInvoices/', FetchUserInvoicesView.as_view(), name='fetch-user-invoices'),
    path('fetchDelivery/', FetchDeliveryOrdersView.as_view(), name='fetch-delivery-order'),
    path('fetchAllInvoices/', FetchAllInvoices.as_view(), name='fetch-all-invoices')
]
