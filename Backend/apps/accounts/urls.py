from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (RegisterView, LoginView, UserProfileViewSet, 
                   SavedSearchViewSet, CurrentUserView)

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'saved-searches', SavedSearchViewSet, basename='savedsearch')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
]