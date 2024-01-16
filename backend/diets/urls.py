from rest_framework import routers

from diets.views import DietPlanViewSet

router = routers.DefaultRouter()

router.register(r'diet-plans', DietPlanViewSet, basename='diet-plans')
