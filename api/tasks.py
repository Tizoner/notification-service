import json
from datetime import datetime, timedelta
from typing import Generator, List

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


def get_distribution_clients(distribution_id: str) -> List[Task]:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:00")
    distribution = Distribution.objects.get(id=distribution_id)
    filter = distribution.client_properties_filter
    clients = Client.objects.all()
    key = "mobile_operator_code"
    if key in filter:
        clients = clients.filter(mobile_operator_code=filter[key])
    key = "tag"
    if key in filter:
        clients = clients.filter(tag=filter[key])
    return [
        Task(
            distribution_id=distribution_id,
            client_id=client.id,
            message_text=distribution.message_text,
            phone_number=client.phone_number,
            stop_at=distribution.stop_at,
        )
        for client in clients
        if timezone.localtime(distribution.start_at, client.timezone) < now
        and timezone.localtime(distribution.stop_at, client.timezone) > now
    ]


def get_tasks_by_time(since: datetime = None, interval: int = 1) -> List[Task]:
    now = since or datetime.utcnow().strftime("%Y-%m-%d %H:%M:00")
    distribution = Distribution.objects.get(id=distribution_id)
    filter = distribution.client_properties_filter
    clients = Client.objects.all()
    key = "mobile_operator_code"
    if key in filter:
        clients = clients.filter(mobile_operator_code=filter[key])
    key = "tag"
    if key in filter:
        clients = clients.filter(tag=filter[key])
    return [
        Task(
            distribution_id=distribution_id,
            client_id=client.id,
            message_text=distribution.message_text,
            phone_number=client.phone_number,
            stop_at=distribution.stop_at,
        )
        for client in clients
        if now
        < timezone.localtime(distribution.start_at, client.timezone)
        < now + timedelta(minutes=interval)
        and timezone.localtime(distribution.stop_at, client.timezone) > now
    ]


class Msg(BaseModel):
    id: int
    phone: int
    text: str


@shared_task
def notify_client(task_data: str):
    """Creates the task to send single message for a client.
    
    Args:
        task_data (str): JSON string with task data
    """
    task = Task.parse_obj(json.loads(task_data))
    message = Message(
        distribution=Distribution(task.distribution_id),
        client=Client(task.client_id),
    )
    message.save()
    msg = Msg(id=message.id, phone=task.phone_number, text=task.message)
    response = requests.post(
        f"https://probe.fbrq.cloud/v1/send/{msg.id}",
        headers={"Authorization": f"Bearer {settings.JWT}"},
        json=msg.dict(),
    )
    message.sending_status = response.status_code
    message.save(update_fields=["sending_status"])


def add_sending_tasks(tasks_generator: Generator):
    """Adds a batch of tasks to the queue.
    
    Args:
        tasks_generator (Generator): Generator of Task instances
    """
    while tasks := next(tasks_generator, None):
        for task in tasks:
            notify_client.apply_async(args=[task.json()], expires=task.stop_at)


@shared_task
def check_active_distributions():
    """Scheduled task for CELERY_BEAT_SCHEDULE. Search for clients to send at the current time"""
    add_sending_tasks(get_tasks_by_time(interval=settings.CELERY_SCHEDULE_INTERVAL))


@shared_task
def process_active_distribution(distribution_id: str):
    """Search for clients to send by a given distribution"""
    add_sending_tasks(get_distribution_clients(distribution_id))
