from django.urls import path
from .views import send_test_sms, send_test_mms, receive_sms, sms_status_callback

urlpatterns = [
    path("send-sms/", send_test_sms),               # Send SMS
    path("send-mms/", send_test_mms),               # Send MMS
    path("receive-sms/", receive_sms),             # Receive incoming SMS (Webhook)
    path("sms-status/", sms_status_callback),       # Message status callback
]


