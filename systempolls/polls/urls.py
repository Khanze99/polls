from django.urls import path

from .views import PollView

urlpatterns = [
    path('active/polls/', PollView.as_view()),
    path('completed/polls/<int:uid>/', PollView.as_view())
]