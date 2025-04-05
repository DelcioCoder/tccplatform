from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import ConnectionRequest
from .serializers import (
    ConnectionRequestCreateSerializer,
    ConnectionRequestResponseSerializer,
    ConnectionRequestSerializer
)


# Permissão customizada para garantir que somente estudantes possam criar solicitações
class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'student'
    
class IsAdvisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'advisor'
    

class ConnectionRequestCreateView(generics.CreateAPIView):
    """Permite que um estudante crie uma solicitação de conexão"""
    serializer_class = ConnectionRequestCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_serializer(self, *args, **kwargs):
        # Adiciona o contexto ao serializador
        context = super().get_serializer_context()
        context.update({'request': self.request})
        kwargs['context'] = context  # Passa o contexto atualizado para o serializador
        return super().get_serializer(*args, **kwargs)  # Retorna o serializador


class ConnectionRequestListView(generics.ListAPIView):
    """Lista todas as solicitações de conexão recebidas pelo orientador"""
    queryset = ConnectionRequest.objects.all()
    serializer_class = ConnectionRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdvisor]

    def get_queryset(self):
        """Retorna apenas as solicitações direcionadas ao orientador autenticado"""
        return ConnectionRequest.objects.filter(advisor=self.request.user)

class ConnectionRequestStudentListView(generics.ListAPIView):
    """Lista todas as solicitações de conexão recebidas pelo estudante"""
    serializer_class = ConnectionRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        """Retorna apenas as solicitações direcionadas ao estudante autenticado"""
        return ConnectionRequest.objects.filter(student=self.request.user)

class ConnectionRequestResponseView(generics.UpdateAPIView):
    """View para que o orientador responda a uma solicitação de conexão"""
    serializer_class = ConnectionRequestResponseSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdvisor]
    queryset = ConnectionRequest.objects.all()

    def get_queryset(self):
        """Retorna apenas as solicitações direcionadas ao orientador autenticado"""
        return ConnectionRequest.objects.filter(advisor=self.request.user)