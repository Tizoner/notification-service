import json
from datetime import datetime
from typing import List

import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from pydantic import BaseModel

from .models import Client, Distribution, Message


class Task(BaseModel):
    distribution_id: int
    client_id: int
    message_text: str
    phone_number: int
    stop_at: datetime


def get_distribution_tasks(
    distribution: Distribution, now: datetime = timezone.now()
) -> List[Task]:
    filter = distribution.client_properties_filter
    clients = Client.objects.all()
    key = "mobile_operator_code"
    if key in filter:
        clients = clients.filter(mobile_operator_code=filter[key])
    key = "tag"
    if key in filter:
        clients = clients.filter(tag=filter[key])
    for client in clients:
        if (
            timezone.localtime(distribution.start_at, client.timezone)
            < timezone.localtime(now, client.timezone)
            < timezone.localtime(distribution.stop_at, client.timezone)
        ):
            yield Task(
                distribution_id=distribution.id,
                client_id=client.id,
                message_text=distribution.message_text,
                phone_number=client.phone_number,
                stop_at=distribution.stop_at,
            )


def get_distributions_tasks(interval: int = 1) -> List[Task]:
    now = timezone.now()
    tasks = []
    for distribution in Distribution.objects.all():
        for task in get_distribution_tasks(distribution, now):
            tasks.append(task)
    return tasks


class Msg(BaseModel):
    id: int
    phone: int
    text: str


@shared_task
def notify_client(task_data: str):
    """Send single message for a client.

    Args:
        task_data (str): JSON string with task data
    """
    task = Task.parse_obj(json.loads(task_data))
    message = Message(
        distribution=Distribution(task.distribution_id),
        client=Client(task.client_id),
    )
    message.save()
    msg = Msg(id=message.id, phone=task.phone_number, text=task.message_text)
    try:
        response = requests.post(
            f"https://probe.fbrq.cloud/v1/send/{msg.id}",
            headers={"Authorization": f"Bearer {settings.JWT}"},
            json=msg.dict(),
            timeout=3,
        )
        message.sending_status = response.status_code
    except requests.Timeout:
        message.sending_status = 504
    message.save(update_fields=["sending_status"])


#     INVALID_SERVICE_RESPONSE = 502
#     SERVICE_RESPONSE_TIMEOUT = 504


def add_sending_tasks(tasks: List[Task]):
    """Adds a batch of tasks to the queue.

    Args:
        tasks (List): List of Task instances
    """
    for task in tasks:
        notify_client.apply_async(args=[task.json()], expires=task.stop_at)


@shared_task
def check_active_distributions():
    """Scheduled task for CELERY_BEAT_SCHEDULE. Search for clients to send at the current time"""
    add_sending_tasks(
        get_distributions_tasks(interval=settings.CELERY_SCHEDULE_INTERVAL)
    )


@shared_task
def process_active_distribution(distribution_id: str):
    """Search for clients to send by a given distribution"""
    add_sending_tasks(
        get_distribution_tasks(Distribution.objects.get(id=distribution_id))
    )
