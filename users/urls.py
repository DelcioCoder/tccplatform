from django.urls import path
from .views import UserRegistrationView, ActivateUserView  

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='user-activation'),
]
