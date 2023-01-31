import itertools

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from timezone_field import TimeZoneField
from ujson import dumps

from .utils import serialize_object


class BaseModel(models.Model):
    def __repr__(self):
        return dumps(
            self.to_dict(),
            indent=4,
            default=serialize_object,
            ensure_ascii=False,
            escape_forward_slashes=False,
        )

    def to_dict(self):
        data = {}
        options = self._meta
        for field in itertools.chain(options.concrete_fields, options.private_fields):
            data[field.name] = field.value_from_object(self)
        for field in options.many_to_many:
            data[field.name] = [i.id for i in field.value_from_object(self)]
        return data

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class Distribution(BaseModel):
    start_at = models.DateTimeField()
    client_properties_filter = models.JSONField(default=dict, blank=True)
    message_text = models.TextField()
    stop_at = models.DateTimeField()

    def clean(self):
        super().clean()
        from .serializers import ClientPropertiesFilterSerializer

        filter = self.client_properties_filter
        assert filter.keys() <= set(ClientPropertiesFilterSerializer.Meta.fields)
        ClientPropertiesFilterSerializer(data=filter).is_valid(raise_exception=True)


class Client(BaseModel):
    phone_number = models.PositiveBigIntegerField(
        validators=[MinValueValidator(70000000000), MaxValueValidator(79999999999)]
    )
    mobile_operator_code = models.PositiveIntegerField(
        validators=[MinValueValidator(900), MaxValueValidator(999)]
    )
    tag = models.CharField(max_length=60)
    timezone = TimeZoneField(choices_display="WITH_GMT_OFFSET")


class Message(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    sending_status = models.PositiveIntegerField()
    distribution = models.ForeignKey(Distribution, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
