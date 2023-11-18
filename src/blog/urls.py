from django.urls import path
from .views import IndexView, PostView, CreatePostView, DeletePostView, UpdatePostView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('post/<str:slug>', PostView.as_view(), name='postview'),
    path('delete/<str:slug>', DeletePostView.as_view(), name='delete'),
    path('create_post', CreatePostView.as_view(), name='creer'),
    path('update/<str:slug>', UpdatePostView.as_view(), name='update'),
]
