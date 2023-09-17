from django.urls import include, path
from rest_framework import routers

from .views import TrainingPlanViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    r'training-plans', TrainingPlanViewSet, basename='training-plans')
# router.register(r'diet-plans', DietPlanViewSet, basename='diet-plans')

urlpatterns = [
    path('', include(router.urls)),
]
