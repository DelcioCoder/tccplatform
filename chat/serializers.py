from rest_framework import serializers
from .models import Conversation, Message

class ConversationSerializer(serializers.ModelSerializer):
    advisor_username = serializers.CharField(source='advisor.username', read_only=True)
    student_username = serializers.CharField(source="student.username", read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'advisor',
            'advisor_username',
            'student',
            'student_username',
            'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    recipient_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id',
            'conversation',
            'sender',
            'sender_username',
            'recipient_username',
            'content',
            'timestamp',
            'read'
        ]
        read_only_fields = ['id', 'sender', 'timestamp', 'read']

    def get_recipient_username(self, obj):
        # Lógica para determinar o nome do destinatário
        # Exemplo: se o request.user for o remetente, o destinatário é o outro participante
        request = self.context.get('request')
        if request and request.user == obj.sender:
            return obj.conversation.student.username
        return obj.conversation.advisor.username
