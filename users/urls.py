from django.urls import path
from .views import RegisterView, UserListView, UserMeView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/me/', UserMeView.as_view(), name='user-me'),
]
