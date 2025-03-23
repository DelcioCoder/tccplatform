from django.urls import path
from .views import ProfileDetailView, AdvisorSearchView, StudentSearchView

urlpatterns = [
    path('', ProfileDetailView.as_view(), name='profile-detail'),
    path('advisors/', AdvisorSearchView.as_view(), name='advisor-search'),
    path('students/', StudentSearchView.as_view(), name='student-search'),
]