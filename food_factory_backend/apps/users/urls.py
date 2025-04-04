from django.urls import path
from .views import (
    UserInsertView, FetchAllUserView, FetchUserByEmailView, SignInUserView, ForgotPasswordView, VerifyOTPView, 
    ResetPasswordView, DBConfigView, UpdateDBConfigView, FetchDealerDetailsView, UpdateDealerDetailsView, FetchUserDetailsView,
    FetchComapnyDetailsView, InsertCompanyDetailView, UpdateCompanyDetailView, DeleteCompanyDetailView
)

urlpatterns = [
    path('insert/', UserInsertView.as_view(), name='user-insert'),
    path('fetchall/', FetchAllUserView.as_view(), name='fetchall-users'),
    path('fetchuser/', FetchUserByEmailView.as_view(), name='fetchuser-byemail'),
    path('signIn/', SignInUserView.as_view(), name='sigin-user'),
    path('forgotPassword/sendOtp/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verifyOTP/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resetPassword/', ResetPasswordView.as_view(), name='reset-password'),
    path('fetchDbConfig/', DBConfigView.as_view(), name='fetch_db_config'),
    path('updateDbConfig/', UpdateDBConfigView.as_view(), name='update_db_config'),
    path('fetchDealerDetails/', FetchDealerDetailsView.as_view(), name='fetch_dealer_details'),
    path('updateDealerDetails/', UpdateDealerDetailsView.as_view(), name='update_dealer_details'),
    path('fetchUserById/', FetchUserDetailsView.as_view(), name='fetch_user_byId'),
    path('fetchCompanyDetails/', FetchComapnyDetailsView.as_view(), name='fecth-company-details'),
    path('insertCompany/', InsertCompanyDetailView.as_view(), name='insert-company'),
    path('updateCompany/', UpdateCompanyDetailView.as_view(), name='update-company'),
    path('deleteCompany/', DeleteCompanyDetailView.as_view(), name='delete-company')
]
