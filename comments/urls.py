from django.urls import path
from .views import CommentViewSet

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    path('tickets/<int:ticket_id>/comments/', comment_list, name='ticket-comments'),
]
