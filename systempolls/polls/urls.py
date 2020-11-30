from django.urls import path

from .views import PollView

urlpatterns = [
    path('active/polls/', PollView.as_view(), name='get_active_polls'),
    path('completed/polls/<int:uid>/', PollView.as_view(), name='get_completed_polls'),
    path('take/poll/', PollView.as_view(), name='post_poll')
]