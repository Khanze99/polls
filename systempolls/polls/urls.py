from django.urls import path

from .views import PollView

urlpatterns = [
    path('', PollView.as_view())
]