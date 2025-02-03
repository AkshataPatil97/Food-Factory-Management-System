from django.urls import path
from .views import UserInsertView, FetchAllUserView, FetchUserByEmailView

urlpatterns = [
    path('insert/', UserInsertView.as_view(), name='user-insert'),
    path('fetchall/', FetchAllUserView.as_view(), name='fetchall-users'),
    path('fetchuser/', FetchUserByEmailView.as_view(), name='fetchuser-byemail'),


]
