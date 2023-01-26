from django.contrib import admin

from api.models import Client, Distribution, Message


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(CustomModelAdmin, self).__init__(model, admin_site)


@admin.register(Client)
class ClientAdmin(CustomModelAdmin):
    search_fields = "id", "phone_number"
    list_filter = "tag", "mobile_operator_code", "timezone"


@admin.register(Distribution)
class DistributionAdmin(CustomModelAdmin):
    search_fields = "id", "message_text"
    list_filter = "start_at", "stop_at", "client_properties_filter"


@admin.register(Message)
class MessageAdmin(CustomModelAdmin):
    search_fields = ("id",)
    list_filter = "created_at", "sending_status"
