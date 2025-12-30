from django.urls import path
from .views import send_test_sms

urlpatterns = [
    path("send-sms/", send_test_sms),
]
