from rest_framework import serializers
from .models import Profile



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']



class AdvisorSearchSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    user_id = serializers.IntegerField(source='user.id')
    class Meta:
        model = Profile
        fields = ['user_id', 'username', 'specialization', 'biography']
        read_only_fields = ['user_id']
        


class StudentSearchSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    user_id = serializers.IntegerField(source='user.id')
    class Meta:
        model = Profile
        fields = ['user_id', 'username', 'course', 'graduation_year', 'tcc_interest']
        read_only_fields = ['user_id']