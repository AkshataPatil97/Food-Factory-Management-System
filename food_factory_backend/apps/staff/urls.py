from django.urls import path
from .views import( 
    StaffInsertView, AssignOrderToDeliveryBoyView
)

urlpatterns = [
    path('insert/', StaffInsertView.as_view(), name='order-insert'),
    path('assignDeliveryBoy/', AssignOrderToDeliveryBoyView.as_view(), name='assign-delivery-boy'),
    # path('fetchAllOrder/', FetchAllOrdersIdView.as_view(), name='fetchorder-byid'),
    # path('updateOrder/', OrderUpdateView.as_view(), name='update-order'),
    # path('cancelOrder/', CancelOrderView.as_view(), name='cancel-order'),
    # path('updateOrderStatus/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    # path('fetchAllDeliveredOrder/', FetchAllDeleiveredOrdersView.as_view(), name='fetch-all-delivered-order'),
    # path('fetchAllCancelledOrder/', FetchAllCanceledOrdersView.as_view(), name='fetch-all-cancelled-order')
]
