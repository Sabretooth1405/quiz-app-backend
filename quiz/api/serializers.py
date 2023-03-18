from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Question


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

    

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('user', 'category', 'question', 'question_urls','answer','answer_urls','created_at','used','id')
        extra_kwargs = {'user': {'required': False}}
        read_only_fields = ('user','created_at','id')


    def to_representation(self, data):
        data = super(QuestionSerializer, self).to_representation(data)
        username = User.objects.filter(pk=data['user']).first().username
        data['user'] = username
        return data
