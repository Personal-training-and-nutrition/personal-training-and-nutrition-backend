from django.urls import include, path
from rest_framework import routers

from .views import (ActivateUser, ClientsViewSet, CustomUserViewSet,
                    DietPlanViewSet, NewUserListCreateView,
                    NewUserRetrieveUpdateDeleteView, ParamsListView,
                    SpecialistViewSet, TrainingPlanViewSet,)

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    r'training-plans', TrainingPlanViewSet, basename='training-plans')
router.register(r'diet-plans', DietPlanViewSet, basename='diet-plans')
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'specialists', SpecialistViewSet,
                basename='users-specialists')
router.register(r'clients', ClientsViewSet, basename='clients')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.social.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<uid>/<token>',
         ActivateUser.as_view({'get': 'activation'}), name='activation'),
    path("params", ParamsListView.as_view(),
         name="params"),
    path("newuser/", NewUserListCreateView.as_view(), name="newuser"),
    path("newuser/<uuid:pk>/", NewUserRetrieveUpdateDeleteView.as_view(),
         name="newuser-details"),
]
