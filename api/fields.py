from drf_spectacular.plumbing import build_basic_type, build_object_type
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from timezone_field import TimeZoneField
from timezone_field.choices import with_gmt_offset


@extend_schema_field(
    build_object_type(
        dict(
            tag=build_basic_type(str),
            mobile_operator_code=dict(build_basic_type(int), minimum=900, maximum=999),
        )
    ),
)
class ClientPropertiesFilterSerializerField(serializers.JSONField):
    pass


class TimeZoneSerializerField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        super().__init__(
            with_gmt_offset(map(str, TimeZoneField.default_zoneinfo_tzs)), **kwargs
        )

    def to_representation(self, value):
        return str(super().to_representation(value))
