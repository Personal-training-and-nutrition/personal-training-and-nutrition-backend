from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from diets.models import DietPlan
from diets.serializers import DietPlanLinkSerializer, DietPlanSerializer


class DietPlanViewSet(viewsets.ModelViewSet):
    """Функции для работы с планами питания"""
    serializer_class = DietPlanSerializer
    queryset = DietPlan.objects.all()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']

    @action(detail=True, methods=['post'])
    def send_link(self, request, pk=None):
        """Генерация ссылки и отправка плана питания."""
        diet_plan = self.get_object()
        link = "http://127.0.0.1:8000/api/diet-plans/{0}".format(diet_plan.pk)
        # В этой части нужно реализовать логику отправки, например,
        # отправку письма или сообщения
        serializer = DietPlanLinkSerializer(data={'diet_plan_id': diet_plan.pk,
                                                  'link': link})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
