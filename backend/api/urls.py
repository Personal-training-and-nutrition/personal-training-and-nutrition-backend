from django.urls import include, path
from rest_framework import routers

from .views import TrainingPlanViewSet, TrainingViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    r'training-plans', TrainingPlanViewSet, basename='training-plans')
router.register(
    r'trainings', TrainingViewSet, basename='trainings')

urlpatterns = [
    path('', include(router.urls)),
]
