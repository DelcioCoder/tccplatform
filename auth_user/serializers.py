from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Adiciona o campo user_type ao payload do token
        token['user_type'] = user.user_type
        return token
