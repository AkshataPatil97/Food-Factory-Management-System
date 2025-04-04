from django.urls import path
from .views import( 
    StaffInsertView, AssignOrderToDeliveryBoyView,FetchAllDeliveryStaffView, FetchAllDStaffView,
    StaffUpdateView, StaffDeleteView, StaffSignInView, SendOTPToDealerView, VerifyOTPView
)

urlpatterns = [
    path('insert/', StaffInsertView.as_view(), name='order-insert'),
    path('assignDeliveryBoy/', AssignOrderToDeliveryBoyView.as_view(), name='assign-delivery-boy'),
    path('fetchAllDeliveryStaff/', FetchAllDeliveryStaffView.as_view(), name='fetchorder-byid'),
    path('fetchAllStaff/', FetchAllDStaffView.as_view(), name='fetch-all-staff'),
    path('update/', StaffUpdateView.as_view(), name='staff-update'),
    path('delete/', StaffDeleteView.as_view(), name='staff-delete'),
    path('login/', StaffSignInView.as_view(), name='staff-login'),
    path('sendOtp/', SendOTPToDealerView.as_view(), name='send-otp-dealer'),
    path('verifyOTP/', VerifyOTPView.as_view(), name='verify-otp')
]
