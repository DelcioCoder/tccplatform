from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer, AdvisorSearchSerializer, StudentSearchSerializer
from .filters import AdvisorFilter, StudentFilter
# Create your views here.


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    def get_object(self):
        # Garante que o usuário só acesse o seu próprio perfil
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    


class AdvisorSearchView(generics.ListAPIView):
    serializer_class = AdvisorSearchSerializer
    filterset_class = AdvisorFilter


    def get_queryset(self):
        # Retorna somente perfis de orientadores
        return Profile.objects.filter(user__user_type='advisor')
    


class StudentSearchView(generics.ListAPIView):
    serializer_class = StudentSearchSerializer
    filterset_class = StudentFilter



    def get_queryset(self):
        # Retorna somente perfis de estudantes
        return Profile.objects.filter(user__user_type='student')

