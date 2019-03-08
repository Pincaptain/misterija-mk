from django.urls import path

from .api import views

urlpatterns = [
    path('topics/<pk>/', views.DetailPostTopicView.as_view()),
    path('topics/', views.ListPostTopicView.as_view()),
    path('comments/create/', views.CreatePostCommentView.as_view()),
    path('comments/update/<pk>/', views.UpdatePostCommentView.as_view()),
    path('comments/destroy/<pk>/', views.DestroyPostCommentView.as_view()),
    path('comments/vote/<pk>/', views.VotePostCommentView.as_view()),
    path('<pk>/', views.DetailPostView.as_view()),
    path('', views.ListPostView.as_view()),
]
