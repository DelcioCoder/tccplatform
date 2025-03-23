from django.urls import path
from .views import (
    ConnectionRequestCreateView,
    ConnectionRequestListView,
    ConnectionRequestResponseView
)

urlpatterns = [
    path('create/', ConnectionRequestCreateView.as_view(), name='connection-create'),
    path('advisor/requests/', ConnectionRequestListView.as_view(), name='advisor-requests'),
    path('response/<int:pk>/', ConnectionRequestResponseView.as_view(), name='connection-response'),
]