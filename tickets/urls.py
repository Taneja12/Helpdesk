from django.urls import path
from .views import (
    TicketListCreateView,
    TicketDetailView,
    AssignTicketView,
    AgentUpdateStatusView,
    TicketStatsView,
)

urlpatterns = [
    path("tickets/", TicketListCreateView.as_view()),
    path("tickets/<int:pk>/", TicketDetailView.as_view()),
    path("tickets/<int:pk>/assign/", AssignTicketView.as_view()),
    path("tickets/<int:pk>/status/", AgentUpdateStatusView.as_view()),
    path("reports/stats/", TicketStatsView.as_view()),
]
