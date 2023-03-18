from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls
urlpatterns=[
    path('auth/', obtain_auth_token),
    path('login-test/', views.apiLoginTest),
    path('register/', views.UserCreateAPIView.as_view()),
    path('create/', views.TaskCreateView.as_view()),
    path('list/', views.TaskList),
    path('detail/<int:pk>', views.TaskRetriveUpdateDestroyView.as_view()),
    path('docs/', include_docs_urls(title='TODO Api'),name='docs'),
    path('logout/', views.Logout.as_view()),
]