from django.urls import include, path
from rest_framework import routers

from .views import (ActivateUser, ClientsViewSet, DietPlanViewSet,
                    ParamsListView, SpecialistsListView, TrainingPlanViewSet,
                    UserListCreateView, UserRetrieveUpdateDeleteView,)

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    r'training-plans', TrainingPlanViewSet, basename='training-plans')
router.register(r'diet-plans', DietPlanViewSet, basename='diet-plans')
router.register(r'clients', ClientsViewSet, basename='clients')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.social.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<uid>/<token>',
         ActivateUser.as_view({'get': 'activation'}), name='activation'),
    path("params/", ParamsListView.as_view(), name="params"),
    path("specialists/", SpecialistsListView.as_view(), name="specialists"),
    path("users/", UserListCreateView.as_view(), name="users"),
    path("users/<uuid:pk>/", UserRetrieveUpdateDeleteView.as_view(),
         name="newuser-details"),
]
