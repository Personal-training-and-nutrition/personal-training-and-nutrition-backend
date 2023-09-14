from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DietPlanViewSet

router_v1 = DefaultRouter()
router_v1.register(r'dietplans', DietPlanViewSet, basename='dietplans')

urlpatterns = [
    path('', include(router_v1.urls)),
]

