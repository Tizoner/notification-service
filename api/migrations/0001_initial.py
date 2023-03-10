# Generated by Django 4.1.4 on 2023-02-06 04:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone_number",
                    models.PositiveBigIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(70000000000),
                            django.core.validators.MaxValueValidator(79999999999),
                        ]
                    ),
                ),
                (
                    "mobile_operator_code",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(900),
                            django.core.validators.MaxValueValidator(999),
                        ]
                    ),
                ),
                ("tag", models.CharField(max_length=60)),
                (
                    "timezone",
                    timezone_field.fields.TimeZoneField(
                        choices_display="WITH_GMT_OFFSET"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Distribution",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_at", models.DateTimeField()),
                (
                    "client_properties_filter",
                    models.JSONField(blank=True, default=dict),
                ),
                ("message_text", models.TextField()),
                ("stop_at", models.DateTimeField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("sending_status", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="api.client"
                    ),
                ),
                (
                    "distribution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="api.distribution",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
