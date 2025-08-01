from rest_framework import serializers
from .models import ConnectionRequest

class ConnectionRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequest
        fields = ['id', 'advisor', 'message']
        read_only_fields = ['id']
    

    def validate_advisor(self, value):
        """Garantir que o estudante não envie solicitação para si mesmo"""
        request = self.context.get('request')
        if value.user_type != 'advisor':
            raise serializers.ValidationError('A solicitação só pode ser enviado para um orientador.')
        
        # Verificar se já existe uma solicitação pendente para o orientador
        if ConnectionRequest.objects.filter(
            student=request.user,
            advisor=value,
            status='Pending'
        ).exists():
            raise serializers.ValidationError('Já existe uma solicitação pendente para este orientador.')
        
        return value
    
    def create(self, validated_data):
        """O estudante é obtido a partir do contexto da requisição"""
        request = self.context.get('request')
        validated_data['student'] = request.user
        return super().create(validated_data)
    


class ConnectionRequestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequest
        fields = ['id', 'response_message', 'status']
        read_only_fields = ['id']


    def validate_status(self, value):
        """Garantir que o status só pode ser alterado para 'Accepted' ou 'Rejected'"""
        if value not in ['Accepted', 'Rejected']:
            raise serializers.ValidationError('O status só pode ser alterado para "Accepted" ou "Rejected"')
        return value
    

    def update(self, instance, validated_data):
        """Actualiza a resposta e o status da solicitação"""
        instance.response_message = validated_data.get('response_message', instance.response_message)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class ConnectionRequestSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(source='student.id', read_only=True)
    advisor_id = serializers.IntegerField(source='advisor.id', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)
    advisor_username = serializers.CharField(source='advisor.username', read_only=True)

    class Meta:
        model = ConnectionRequest
        fields = [
            'id', 
            'student_id',
            'student_username', 
            'advisor_id',
            'advisor_username', 
            'message', 
            'response_message', 
            'status', 
            'created_at'
        ]
        read_only_fields = ['id']