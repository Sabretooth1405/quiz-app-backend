from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username', 'password',)
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    
#test commit

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('user', 'title', 'description', 'date', 'created_at','id')
        extra_kwargs = {'user': {'required': False}}
        read_only_fields = ('user','created_at','id')


    def to_representation(self, data):
        data = super(TaskSerializer, self).to_representation(data)
        username = User.objects.filter(pk=data['user']).first().username
        data['user'] = username
        return data
