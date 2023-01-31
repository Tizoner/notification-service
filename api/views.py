from drf_spectacular.plumbing import build_basic_type, build_object_type
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Client, Distribution, Message
from .serializers import (
    ClientSerializer,
    DistributionGeneralStatisticsSerializer,
    DistributionSerializer,
    MessageSerializer,
)
from .utils import detail


class ClientCreate(generics.CreateAPIView):
    serializer_class = ClientSerializer


class ClientUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ["put", "patch", "delete"]


class DistributionCreate(generics.CreateAPIView):
    serializer_class = DistributionSerializer


@extend_schema_view(
    get=extend_schema(
        summary="получение общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                DistributionGeneralStatisticsSerializer,
                description="Отчёт успешно сформирован",
            )
        },
    )
)
class DistributionGeneralStatisticsView(generics.ListAPIView):
    queryset = Distribution.objects.all()
    serializer_class = DistributionGeneralStatisticsSerializer


class DistributionDetailedStatisticsView(generics.GenericAPIView):
    @extend_schema(
        summary="получение детальной статистики отправленных сообщений по конкретной рассылке",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                MessageSerializer(many=True),
                description="Отчёт успешно сформирован",
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                build_object_type(detail(build_basic_type(str))),
                description="Рассылка не найдена",
            ),
        },
    )
    def get(self, request, pk):
        distribution = get_object_or_404(Distribution, id=pk)
        messages = Message.objects.filter(distribution=distribution)
        serialized_messages = MessageSerializer(messages, many=True).data
        return Response(serialized_messages, status.HTTP_200_OK)


class DistributionUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer
    http_method_names = ["put", "patch", "delete"]
