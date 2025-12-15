from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Ticket


@shared_task
def check_ticket_escalations():
    now = timezone.now()

    priority_times = {
        "high": timedelta(hours=1),
        "medium": timedelta(hours=4),
        "low": timedelta(hours=24)
    }

    tickets = Ticket.objects.filter(status__in=["open", "in-progress"])

    for ticket in tickets:
        threshold = priority_times[ticket.priority]

        if ticket.updated_at < now - threshold:
            if ticket.status != "escalated":  # avoid repeating escalation
                ticket.status = "escalated"
                ticket.save()

                # email alert
                send_mail(
                    subject=f"Ticket Escalated: {ticket.title}",
                    message=f"Ticket #{ticket.id} has been escalated due to inactivity.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[
                        ticket.created_by.email,
                        "admin@example.com"
                    ],
                )
