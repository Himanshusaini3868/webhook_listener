import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PaymentEvent
from .utils import verify_signature
from rest_framework.generics import ListAPIView
from .serializers import PaymentEventSerializer


class WebhookPaymentView(APIView):
    def post(self, request):
        raw_body = request.body
        signature = request.headers.get("X-Razorpay-Signature")
        
        #skipping signature verification temporary
        
        if signature:
            if not verify_signature(raw_body, signature):
                return Response({"error": "Invalid signature"}, status=403)
        
        try:
            data = json.loads(raw_body)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=400)

        events = data if isinstance(data, list) else [data]
        saved_events = []

        for event in events:
            try:
                event_type = event.get("event")
                event_id = event.get("id")
                payment_id = event.get("payload", {}).get("payment", {}).get("entity", {}).get("id")
                if not all([event_type, event_id, payment_id]):
                    return Response(
                        {"error": "Missing required fields"},
                        status=400
                    )

                # checking duplicacy
                duplicate_events = []
                if PaymentEvent.objects.filter(event_id=event_id).exists():
                    duplicate_events.append(event_id)
                    continue
                PaymentEvent.objects.create(
                    event_id=event_id,
                    event_type=event_type,
                    payment_id=payment_id,
                    payload=event
                )
                saved_events.append(event_id)

            except Exception as e:
                print(f"Error processing event: {str(e)}")
                continue

        return Response({
            "message": "Webhook processed",
            "saved_events": saved_events,
            "duplicate_events": duplicate_events
        }, status=200)
    
    
    
class PaymentEventsView(ListAPIView):
    serializer_class = PaymentEventSerializer

    def get_queryset(self):
        payment_id = self.kwargs['payment_id']
        return PaymentEvent.objects.filter(
            payment_id=payment_id
        ).order_by('received_at')