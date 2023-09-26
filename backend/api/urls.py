from django.urls import include, path
from rest_framework import routers

from .views import (ActivateUser, CustomUserViewSet, DietPlanViewSet,
                    WorkoutListViewSet, DietListViewSet,
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
    path('users/<id>/program_workout_list/',
         WorkoutListViewSet.as_view({'get': 'get_list'}),
         name='program-workout-list'),
    path('users/<id>/program_diet_list/',
         DietListViewSet.as_view({'get': 'get_list'}),
         name='program-diet-list'),
]
