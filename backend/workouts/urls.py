from rest_framework import routers

from workouts.views import TrainingPlanViewSet

router = routers.DefaultRouter()

router.register(
    r'training-plans', TrainingPlanViewSet, basename='training-plans')
