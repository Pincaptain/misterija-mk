from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .api import views

urlpatterns = [
    path('login/', obtain_auth_token),
    path('register/', views.CreateUserView.as_view()),
]
