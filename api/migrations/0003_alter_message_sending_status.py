# Generated by Django 4.1.4 on 2023-02-01 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_alter_message_sending_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="sending_status",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
