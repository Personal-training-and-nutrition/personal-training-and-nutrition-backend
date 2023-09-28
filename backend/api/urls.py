from django.urls import include, path
from rest_framework import routers

from .views import (ActivateUser, CustomUserViewSet, DietPlanViewSet,
                    TrainingPlanViewSet,)

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    r'training-plans', TrainingPlanViewSet, basename='training-plans')
router.register(r'diet-plans', DietPlanViewSet, basename='diet-plans')
router.register(r'users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.social.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<uid>/<token>',
         ActivateUser.as_view({'get': 'activation'}), name='activation'),
    path('users/<int:pk>/profile/',
         CustomUserViewSet.as_view({'get': 'profile', 'put': 'update_profile'})),
]
