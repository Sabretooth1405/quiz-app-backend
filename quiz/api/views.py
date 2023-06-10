from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer, QuestionSerializer, FriendshipSerializer, FriendshipRequestSerializer,FriendAnswerSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Question,Friendship,FriendshipRequests,FriendAnswer
from django.shortcuts import render, redirect, get_object_or_404
from .permissions import IsOwner,IsFriend,IsQuestionCreatorOrFriend,IsAnswerer,IsFriendInRequest
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.views import APIView
from http import HTTPStatus
from django.db.models import Q,QuerySet

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def apiLoginTest(req):
    user = User.objects.get(username=req.user)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


class QuestionCreateView(generics.CreateAPIView):
    def get_queryset(self):
        return Question.objects.filter(user__username=self.request.user)
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        id = User.objects.get(username=self.request.user)
        serializer.save(user=id)
        return serializer.validated_data
    permission_classes = (IsAuthenticated,)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def QuestionList(req):
    context = {'request': req}
    questions = Question.objects.filter(user__username=req.user)
    q=req.query_params.get('q')
    if q is not None:
        questions=questions.filter(Q(question__icontains=q)|Q(category__icontains=q))
    serializer = QuestionSerializer(questions, many=True,context=context)
    return Response(serializer.data)



class QuestionRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = QuestionSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        return Question.objects.filter(id=self.kwargs.get('pk'))

    def perform_update(self, serializer):
        id = User.objects.get(username=self.request.user)
        serializer.save(user=id)
        return serializer.validated_data
    permission_classes=(IsOwner,)


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FriendList(req):
    friends=Friendship.objects.filter(from_user=req.user).order_by("-created_at")
    serializer = FriendshipSerializer(friends, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FriendRequests(req):
    requests =  FriendshipRequests.objects.filter(
            to_user=req.user, rejected=False, accepted=False
        ).order_by("-created")

    serializer = FriendshipRequestSerializer(requests, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SendFriendshipRequestView(request, username):
    
    recipient = User.objects.get(username=username)
    fr, created = FriendshipRequests.objects.get_or_create(
        from_user=request.user, to_user=recipient
    )
    if not created:
        return Response(status=HTTPStatus.ALREADY_REPORTED)
    return Response({"message: request sent"},status=HTTPStatus.ACCEPTED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ProcessFriendRequestView(request, pk):
    fr: FriendshipRequests = get_object_or_404(FriendshipRequests, pk=pk)
    if request.method == "POST" and fr.to_user == request.user:
        if request.data["action"] == "accept":
            Friendship.objects.get_or_create(
                from_user=fr.from_user, to_user=fr.to_user)
            Friendship.objects.get_or_create(
                from_user=fr.to_user, to_user=fr.from_user)
            fr.accepted = True
            fr.save()
            return Response({"message":"Request accepted succesfully"},status=HTTPStatus.ACCEPTED)

        if request.data["action"] == "reject":
            fr.rejected = True
            fr.save()
            return Response({"message":"Request rejected succesfully"},status=HTTPStatus.ACCEPTED)

class FriendQuestionRetrive(generics.RetrieveAPIView):
    
    serializer_class = QuestionSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        return Question.objects.filter(id=self.kwargs.get('pk'))

    
    permission_classes=(IsFriend,)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FriendQuestionList(req):
    friends=Friendship.objects.filter(from_user=req.user).values("to_user")
    questions=Question.objects.filter(user__in=friends,visible_to_friends=True)
    context = {'request': req}
    serializer = QuestionSerializer(questions, many=True,context=context)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsQuestionCreatorOrFriend])
def QuestionAnswerList(req,**kwargs):
    id=kwargs.get('pk')
    context = {'request': req}
    answers=FriendAnswer.objects.filter(question__id=id)
    serializer=FriendAnswerSerializer(answers,many=True,context=context)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserAnswerList(req):
    answers = FriendAnswer.objects.filter(answerer=req.user)
    serializer = FriendAnswerSerializer(answers, many=True)
    return Response(serializer.data)

class AnswerRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = FriendAnswerSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        return FriendAnswer.objects.filter(id=self.kwargs.get('pk'))

    def perform_update(self, serializer):
        id = User.objects.get(username=self.request.user)
        pk=FriendAnswer.objects.get(id=self.kwargs.get('pk')).question.pk
        question = Question.objects.get(pk=pk)
        serializer.save(answerer=id, question=question,is_checked=False)
        return serializer.validated_data
    permission_classes=(IsAnswerer,)

class AnswerCreateView(generics.CreateAPIView):
    def get_queryset(self):
        return FriendAnswer.objects.filter(user__username=self.request.user)
    serializer_class = FriendAnswerSerializer

    def perform_create(self, serializer):
        id = User.objects.get(username=self.request.user)
        question=Question.objects.get(pk=self.kwargs.get('pk'))
        serializer.save(answerer=id,question=question)
        return serializer.validated_data
    permission_classes = (IsAuthenticated,)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def processAnswer(req,**kwargs):
    id=kwargs.get('pk')
    answer:FriendAnswer=FriendAnswer.objects.get(pk=id)
    questioner=answer.question.user
    
    if req.method == "POST" and req.user == questioner:
        if req.data.get('action')=="correct":
            answer.is_checked=True
            answer.is_correct=True
            answer.save()
            return Response({"message": "Corrected succesfully"}, status=HTTPStatus.ACCEPTED)
        elif req.data.get('action') == "incorrect":
            answer.is_checked=True
            answer.is_correct=False
            answer.save()
            return Response({"message": "Corrected succesfully"}, status=HTTPStatus.ACCEPTED)
        else:
            return Response({"message":"You are not allowed to perform this action"},status=HTTPStatus.FORBIDDEN)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userObjectList(req,**kwargs):
    id=kwargs.get('username')
    context={"username":id}
    users=User.objects.all()
    q=req.query_params.get('q')
    if q is not None:
        users=users.filter(Q(username__icontains=q))
    serializer=UserSerializer(users,many=True,context=context)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteFriendships(req,**kwargs):
    user1=str(req.user)
    user2=kwargs.get('username')
    fr1:Friendship=get_object_or_404(Friendship,from_user__username=user1,to_user__username=user2)
    print(user1)
    fr2:Friendship=get_object_or_404(Friendship,from_user__username=user2,to_user__username=user1)
    fr1.delete()
    fr2.delete()
    return Response({"message: succesfully deleted friendship"},HTTPStatus.ACCEPTED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userStats(req,**kwargs):
    current_user=str(req.user)
    friends:QuerySet=Friendship.objects.filter(Q(to_user__username=current_user))
    questions:QuerySet=Question.objects.filter(user__username=current_user)
    answers:QuerySet=FriendAnswer.objects.filter(answerer__username=current_user)
    requested_user=kwargs.get('username')
    if (current_user==requested_user):
        response={
            "answer_count":answers.count(),
            "question_count":questions.count(),
            "friends_count":friends.count(),
            "is_same_user": True,
        }
        return Response(response,HTTPStatus.OK)
    requested_user_friends:QuerySet=Friendship.objects.filter(Q(to_user__username=requested_user))
    requeted_user_questions:QuerySet=Question.objects.filter(user__username=requested_user)
    requested_user_answers:QuerySet=FriendAnswer.objects.filter(answerer__username=requested_user)
    common_friends=QuerySet.intersection(friends.values_list('from_user'),requested_user_friends.values_list('from_user'))
    is_friend:QuerySet=Friendship.objects.filter(to_user__username=requested_user,from_user__username=current_user).exists()
    current_user_questions_answered:QuerySet=FriendAnswer.objects.filter(question__user__username=current_user,answerer__username=requested_user)
    response={
            "answer_count":requested_user_answers.count(),
            "question_count":requeted_user_questions.count(),
            "friends_count":requested_user_friends.count(),
            "is_same_user": False,
            "is_friend":is_friend,
            "common_friends_count":common_friends.count(),
            "current_user_questions_answered_count":current_user_questions_answered.count()
        }
    return Response(response,HTTPStatus.OK)