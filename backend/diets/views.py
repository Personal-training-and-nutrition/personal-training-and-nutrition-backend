from rest_framework import viewsets

from .models import DietPlan
from .serializers import DietPlanSerializer


class DietPlanViewSet(viewsets.ModelViewSet):
    """
    Просмотр созданных ранее планов питания для конкретного клиента.
    """

    serializer_class = DietPlanSerializer
    pagination_class = None
    queryset = DietPlan.objects.all()

    def get_queryset(self):
        spec = self.request.user
        user_id = self.kwargs['user_id']

        return self.queryset.filter(specialist=spec, user=user_id)
