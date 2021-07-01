from django.urls import path
from . import views
from .views import TweetDetailView, CommentDeleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_tweet, name='create'),
    path('search/', views.search, name='search'),
    path('retrieve_tweet/<int:tweet_id>/', views.retrieve_tweet, name='retrieve_tweet'),
    # path('tweet/<int:pk>/comment/', views.tweet_detail, name='add-comment'),
    path('tweet/<int:pk>/', TweetDetailView.as_view(), name='tweet-detail'),
    path('tweet/<int:tweet_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),

]

