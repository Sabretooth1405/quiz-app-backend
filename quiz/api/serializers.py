from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Question,Friendship,FriendshipRequests


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
        fields = ('user', 'category', 'question', 'question_urls','answer','answer_urls','created_at','used','used_for','visible_to_friends','id')
        extra_kwargs = {'user': {'required': False}}
        read_only_fields = ('user','created_at','id')


    def to_representation(self, data):
        data = super(QuestionSerializer, self).to_representation(data)
        username = User.objects.filter(pk=data['user']).first().username
        request = self.context.get('request', None)
        if (str((request.path)).split('/')[2])=="friends":
            hide_fields=['answer','answer_urls','created_at','used_for','used']
            for field in hide_fields:
                data.pop(field)

    
        data['user'] = username
        return data

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model=Friendship
        fields=('from_user','to_user','created_at','id')
        # extra_kwargs = {'from_user': {'required': False},'to_user': {'required': False}}
        # read_only_fields = ('from_user', 'to_user','created_at', 'id')

    def to_representation(self, data):
        data = super(FriendshipSerializer, self).to_representation(data)
        from_username = User.objects.get(pk=data['from_user']).username
        to_username = User.objects.get(pk=data['to_user']).username
        data['from_user'] = from_username
        data['to_user'] = to_username
        return data

class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=FriendshipRequests
        fields='__all__'

    def to_representation(self, data):
        data = super(FriendshipRequestSerializer, self).to_representation(data)
        from_username = User.objects.get(pk=data['from_user']).username
        to_username = User.objects.get(pk=data['to_user']).username
        data['from_user'] = from_username
        data['to_user'] = to_username
        return data
