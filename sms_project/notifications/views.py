import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from django.conf import settings
from twilio.twiml.messaging_response import MessagingResponse


# ------------------ Send SMS ------------------
@csrf_exempt
def send_test_sms(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    data = json.loads(request.body)
    to = data.get("to")
    message = data.get("message")

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    sms = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to
    )

    return JsonResponse({
        "success": True,
        "sid": sms.sid
    })


# ------------------ Send MMS ------------------
@csrf_exempt
def send_test_mms(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    data = json.loads(request.body)
    to = data.get("to")
    message = data.get("message")
    media_urls = data.get("media_urls", [])  # list of media URLs

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    sms = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to,
        media_url=media_urls
    )

    return JsonResponse({
        "success": True,
        "sid": sms.sid
    })


# ------------------ Receive SMS (Webhook) ------------------
@csrf_exempt
def receive_sms(request):
    """This will handle incoming SMS and auto-reply"""
    incoming_msg = request.POST.get("Body")
    from_number = request.POST.get("From")

    resp = MessagingResponse()
    resp.message(f"Thanks! You said: {incoming_msg}")

    return HttpResponse(str(resp), content_type="text/xml")


# ------------------ Message Status Callback ------------------
@csrf_exempt
def sms_status_callback(request):
    """Twilio sends POST to this endpoint on status update"""
    sid = request.POST.get("MessageSid")
    status = request.POST.get("MessageStatus")

    # For learning: just print to console
    print(f"Message {sid} status updated to {status}")

    return HttpResponse("OK")
