from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer
# Create your views here.


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    def get_object(self):
        # Garante que o usuário só acesse o seu próprio perfil
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile