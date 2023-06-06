from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Question, Friendship, FriendshipRequests, FriendAnswer


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
        fields = ('user', 'category', 'question', 'question_urls', 'answer',
                  'answer_urls', 'created_at', 'used', 'used_for', 'visible_to_friends', 'id')
        extra_kwargs = {'user': {'required': False}}
        read_only_fields = ('user', 'created_at', 'id')

    def to_representation(self, data):
        data = super(QuestionSerializer, self).to_representation(data)
        username = User.objects.filter(pk=data['user']).first().username
        request = self.context['request']
        if len(str(request.path).split('/'))>=2:
            if (str((request.path)).split('/')[2]) == "friends":
                hide_fields = ['answer', 'answer_urls',
                             'used_for', 'used']
                for field in hide_fields:
                    data.pop(field)

        data['user'] = username
        return data


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('from_user', 'to_user', 'created_at', 'id')
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
        model = FriendshipRequests
        fields = '__all__'

    def to_representation(self, data):
        data = super(FriendshipRequestSerializer, self).to_representation(data)
        from_username = User.objects.get(pk=data['from_user']).username
        to_username = User.objects.get(pk=data['to_user']).username
        data['from_user'] = from_username
        data['to_user'] = to_username
        return data


class FriendAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendAnswer
        fields = ('question', 'answer_given','answerer', 'is_checked',
                  'is_correct', 'answered_at', 'id')
        extra_kwargs = {'answerer': {'required': False}}
        read_only_fields = ('answerer', 'question', 'answered_at', 'id','is_checked','is_correct')

    def to_representation(self, data):
        data = super(FriendAnswerSerializer, self).to_representation(data)
        username = User.objects.filter(pk=data['answerer']).first().username
        question_obj = Question.objects.get(id=data['question'])
        request = self.context['request']
        data['question'] = {"text": question_obj.question,
                            "id":question_obj.id,
                            "user":question_obj.user.username,
                            "make_answer_visible":question_obj.make_answer_visible}
        if((question_obj.make_answer_visible) or (str(request.path).split('/')[2] == "answers")):
            data['question']['answer']=question_obj.answer
        data['answerer'] = username
        return data
