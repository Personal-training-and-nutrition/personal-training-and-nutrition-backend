from django.urls import include, path
from rest_framework import routers

from users.views import ActivateUser, ClientsViewSet, CustomUserViewSet

router = routers.DefaultRouter()


router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'clients', ClientsViewSet, basename='clients')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.social.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<uid>/<token>',
         ActivateUser.as_view({'get': 'activation'}), name='activation'),
]
