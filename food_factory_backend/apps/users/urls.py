from django.urls import path
from .views import UserInsertView, FetchAllUserView, FetchUserByEmailView, SignInUserView, ForgotPasswordView, VerifyOTPView, ResetPasswordView

urlpatterns = [
    path('insert/', UserInsertView.as_view(), name='user-insert'),
    path('fetchall/', FetchAllUserView.as_view(), name='fetchall-users'),
    path('fetchuser/', FetchUserByEmailView.as_view(), name='fetchuser-byemail'),
    path('signIn/', SignInUserView.as_view(), name='sigin-user'),
    path('forgotPassword/sendOtp/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verifyOTP/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resetPassword/', ResetPasswordView.as_view(), name='reset-password')
]
