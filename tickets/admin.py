from django.contrib import admin
from django.db import transaction
from django.http import HttpResponse
import csv
from django.contrib.auth import get_user_model

from .models import Ticket

User = get_user_model()


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "priority",
        "status",
        "created_by",
        "assigned_to",
        "created_at",
        "updated_at",
    )
    list_filter = ("priority", "status", "created_at", "assigned_to")
    search_fields = ("title", "description", "created_by__username", "created_by__email", "assigned_to__username")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    # allow quick edits for priority, status and assigned_to from changelist
    list_editable = ("priority", "status", "assigned_to")
    actions = [
        "mark_resolved",
        "mark_closed",
        "mark_escalated",
        "bulk_assign_to_first_agent",
        "export_as_csv",
    ]

    def _safe_update_status(self, queryset, status_value):
        """Helper to set status inside a transaction and update timestamps."""
        with transaction.atomic():
            queryset.update(status=status_value)

    @admin.action(description="Mark selected tickets as resolved")
    def mark_resolved(self, request, queryset):
        self._safe_update_status(queryset, Ticket.STATUS_RESOLVED)
        self.message_user(request, f"{queryset.count()} ticket(s) marked as resolved.")

    @admin.action(description="Mark selected tickets as closed")
    def mark_closed(self, request, queryset):
        self._safe_update_status(queryset, Ticket.STATUS_CLOSED)
        self.message_user(request, f"{queryset.count()} ticket(s) marked as closed.")

    @admin.action(description="Mark selected tickets as escalated")
    def mark_escalated(self, request, queryset):
        self._safe_update_status(queryset, Ticket.STATUS_ESCALATED)
        self.message_user(request, f"{queryset.count()} ticket(s) marked as escalated.")

    @admin.action(
        description=(
            "Assign selected tickets to the first available agent (convenience action). "
            "Prefer editing the 'Assigned to' field for specific assignment."
        )
    )
    def bulk_assign_to_first_agent(self, request, queryset):
        """
        Convenience action: assigns selected tickets to the first user found with role='agent'.
        This is a quick helper; in production you probably want a custom admin form to pick an agent.
        """
        first_agent = User.objects.filter(role="agent").first()
        if not first_agent:
            self.message_user(request, "No users with role='agent' found.", level="warning")
            return

        with transaction.atomic():
            updated = queryset.update(assigned_to=first_agent, status=Ticket.STATUS_IN_PROGRESS)
        self.message_user(request, f"{updated} ticket(s) assigned to {first_agent.username}.")

    @admin.action(description="Export selected tickets as CSV")
    def export_as_csv(self, request, queryset):
        """
        Export selected tickets to CSV. Downloads a CSV with basic ticket information.
        """
        meta = self.model._meta
        field_names = ["id", "title", "description", "priority", "status", "created_by", "assigned_to", "created_at", "updated_at"]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename={meta.verbose_name_plural}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([
                obj.id,
                obj.title,
                (obj.description or "").replace("\n", " "),
                obj.priority,
                obj.status,
                getattr(obj.created_by, "username", ""),
                getattr(obj.assigned_to, "username", "") if obj.assigned_to else "",
                obj.created_at.isoformat() if obj.created_at else "",
                obj.updated_at.isoformat() if obj.updated_at else "",
            ])

        return response
