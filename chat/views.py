# messaging/views.py
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Permite filtrar as mensagens entre o usuário e um destinatário específico
        recipient_id = self.request.query_params.get('recipient', None)
        if recipient_id:
            return Message.objects.filter(
                Q(sender=user, recipient__id=recipient_id) |
                Q(sender__id=recipient_id, recipient=user)
            ).order_by('timestamp')
        # Se não for passado um filtro, retorna todas as mensagens relacionadas ao usuário
        return Message.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).order_by('timestamp')

    def perform_create(self, serializer):
        # Define o usuário autenticado como remetente
        serializer.save(sender=self.request.user)
