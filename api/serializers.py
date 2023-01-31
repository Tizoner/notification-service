from drf_spectacular.plumbing import build_basic_type, build_object_type
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .fields import ClientPropertiesFilterSerializerField, TimeZoneSerializerField
from .models import Client, Distribution, Message


class ClientPropertiesFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "mobile_operator_code", "tag"
        extra_kwargs = {field: dict(required=False) for field in fields}


class DistributionSerializer(serializers.ModelSerializer):
    client_properties_filter = ClientPropertiesFilterSerializerField(default=dict)

    class Meta:
        model = Distribution
        fields = tuple(field.name for field in model._meta.fields)


class ClientSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()

    class Meta:
        model = Client
        fields = tuple(field.name for field in model._meta.fields)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class DistributionGeneralStatisticsSerializer(DistributionSerializer):
    sending_status = serializers.SerializerMethodField()

    @extend_schema_field(
        build_object_type(
            dict(
                string=build_object_type(
                    dict(sent_messages_count=dict(build_basic_type(int), minimum=1))
                )
            )
        )
    )
    def get_sending_status(self, distribution):
        statistics = {}
        messages = Message.objects.filter(distribution=distribution)
        for message in messages:
            if message.sending_status in statistics:
                statistics[message.sending_status]["sent_messages_count"] += 1
            else:
                statistics[message.sending_status] = dict(sent_messages_count=1)
        return statistics

    class Meta:
        model = Distribution
        fields = (
            *(field.name for field in model._meta.fields),
            "sending_status",
        )
