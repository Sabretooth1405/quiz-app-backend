from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer, QuestionSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Question
from django.shortcuts import render, redirect, get_object_or_404
from .permissions import IsOwner
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.views import APIView

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
    permission_classes = (IsOwner,)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def QuestionList(req):
    questions = Question.objects.filter(user__username=req.user)
    serializer = QuestionSerializer(questions, many=True)
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
