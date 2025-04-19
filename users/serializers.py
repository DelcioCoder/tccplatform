from rest_framework import serializers
from .models import CustomUser
from django.core.validators import RegexValidator



class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
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
        fields = ['username','last_name', 'email', 'password', 'password2', 'user_type']
        extra_kwargs = {
            'password2': {'write_only': True}
        }
    

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2') # Remove password2 antes de criar o usuário
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        user.is_active = False # Necessário para que o usuário não esteja ativo até que ele confirme o e-mail
        user.save()
        return user

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value