from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Ticket(models.Model):
    PRIORITY_LOW = "low"
    PRIORITY_MED = "medium"
    PRIORITY_HIGH = "high"

    PRIORITY_CHOICES = (
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MED, "Medium"),
        (PRIORITY_HIGH, "High"),
    )

    STATUS_OPEN = "open"
    STATUS_IN_PROGRESS = "in-progress"
    STATUS_RESOLVED = "resolved"
    STATUS_CLOSED = "closed"
    STATUS_ESCALATED = "escalated"

    STATUS_CHOICES = (
        (STATUS_OPEN, "Open"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_RESOLVED, "Resolved"),
        (STATUS_CLOSED, "Closed"),
        (STATUS_ESCALATED, "Escalated"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_LOW)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)

    created_by = models.ForeignKey(User, related_name="created_tickets", on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        User, related_name="assigned_tickets", on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_updated_for_escalation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} [{self.priority}]"

