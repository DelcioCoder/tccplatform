from rest_framework import status, generics, permissions
from django.db.models import Q
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class GetOrCreateConversationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    def post(self, request, *args, **kwargs):
        advisor_id = request.data.get("advisor")
        student_id = request.data.get("student")

        if not advisor_id or not student_id:
            return Response({"error": "IDs de orientador e estudante são necessários."}, status=status.HTTP_400_BAD_REQUEST)

        conversation, created = Conversation.objects.get_or_create(advisor_id=advisor_id, student_id=student_id)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            Q(advisor=user) | Q(student=user)
        ).order_by('-updated_at'
                                        )
    


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id).order_by('-timestamp')
        return Message.objects.none() # Se não houver conversa, retorna vazio
    
    def perform_create(self, serializer):
        # Define o usuário autenticado como sender automaticamente.
        serializer.save(sender=self.request.user)