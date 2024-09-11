# blog_api/urls.py
from django.urls import path
from .views import RegisterView
from .views import BlogEntryView, SearchView, RegisterView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('submit/', BlogEntryView.as_view(), name='blog-submit'),
    path('search/', SearchView.as_view(), name='blog-search'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
]
