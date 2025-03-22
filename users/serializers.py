from rest_framework import serializers
from .models import CustomUser
from django.core.validators import RegexValidator



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com)$',
                message="Somente e-mails dos domínios 'gmail.com' ou 'yahoo.com' são permitidos.",
                code='invalid_email'
            )
        ]
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'user_type']
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        user.is_active = False # Necessário para que o usuário não esteja ativo até que ele confirme o e-mail
        user.save()
        return user

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value