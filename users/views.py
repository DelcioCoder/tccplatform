from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, status, permissions
from django.conf import settings
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserRegistrationSerializer

class AccountStatusView(generics.RetrieveAPIView):
    permission_classes = []
    def get(self, request):
        return Response({
            "username": request.user.username,
            "is_active": request.user.is_active,
        })

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # Gerar tokens
        refresh = RefreshToken.for_user(user)
        headers = self.get_success_headers(serializer.data)

        return Response({
            'message': 'Usuário registrado com sucesso!',
            'user': serializer.data['username'],
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Salva o usuário com is_active=False
        user = serializer.save()
        # Envia o email de confirmação
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request)
        # Construa a URL de ativação; 
        activation_link = f"{settings.FRONTEND_URL}/activate/?uidb64={uid}&token={token}"
        subject = "Confirmação de Cadastro"
        message = (
            f"Olá {user.username},\n\n"
            f"Para ativar sua conta, clique no link abaixo:\n{activation_link}\n\n"
            "Se você não se registrou na nossa plataforma, por favor, ignore este email."
        )
        # Envia o email 
        user.email_user(subject, message)




class ActivateUserView(generics.GenericAPIView):
    def get(self, request, uidb64, token, format=None):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Conta activada com sucesso!'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Link de ativação inválido!'}, status=status.HTTP_400_BAD_REQUEST)
        


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            'user_id': user.id,
            'username': user.username,
            'user_type': user.user_type #Student ou Advisor
        })

