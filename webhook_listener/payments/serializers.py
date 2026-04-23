from rest_framework import serializers
from .models import PaymentEvent

class PaymentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentEvent
        fields = ['event_type', 'received_at']