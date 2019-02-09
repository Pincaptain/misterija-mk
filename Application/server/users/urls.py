from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .api import views

urlpatterns = [
    path('login/', obtain_auth_token),
    path('', views.ListUserView.as_view()),
    path('<pk>/', views.DetailUserView.as_view()),
    path('register/', views.CreateUserView.as_view()),
    path('update/<pk>/', views.UpdateUserView.as_view()),
    path('destroy/<pk>/', views.DestroyUserView.as_view()),
    path('current/', views.CurrentUserView.as_view()),
]
