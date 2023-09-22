from django.urls import include, path
from rest_framework import routers

from .views import DietPlanViewSet, TrainingPlanViewSet, UsersViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    r'training-plans', TrainingPlanViewSet, basename='training-plans')
router.register(r'diet-plans', DietPlanViewSet, basename='diet-plans')
router.register(r'users', UsersViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'), name='auth'),
    path('auth/', include('djoser.social.urls'), name='social'),
]
