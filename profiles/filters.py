from django_filters import rest_framework as filters
from .models import Profile


class AdvisorFilter(filters.FilterSet):
    specialization = filters.CharFilter(field_name='specialization', lookup_expr='icontains')


    class Meta:
        model = Profile
        fields = ['specialization']



class StudentFilter(filters.FilterSet):
    course = filters.CharFilter(field_name='course', lookup_expr='icontains')
    graduation_year = filters.NumberFilter(field_name='graduation_year')
    tcc_interest = filters.CharFilter(field_name='tcc_interest', lookup_expr='icontains')


    class Meta:
        model = Profile
        fields = ['course', 'graduation_year', 'tcc_interest']