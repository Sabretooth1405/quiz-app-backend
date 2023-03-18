from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls
urlpatterns=[
    path('auth/', obtain_auth_token),
    path('login-test/', views.apiLoginTest),
    path('register/', views.UserCreateAPIView.as_view()),
    path('create/', views.QuestionCreateView.as_view()),
    path('list/', views.QuestionList),
    path('detail/<int:pk>', views.QuestionRetriveUpdateDestroyView.as_view()),
    path('docs/', include_docs_urls(title='Question Api'),name='docs'),
    path('logout/', views.Logout.as_view()),
]