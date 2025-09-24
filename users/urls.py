from django.urls import path
from .views import RegisterView, UserListView, UserMeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('backend/register/', RegisterView.as_view(), name='register'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/me/', UserMeView.as_view(), name='user-me'),
]
