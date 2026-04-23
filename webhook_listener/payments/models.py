from django.db import models

class PaymentEvent(models.Model):
    event_id = models.CharField(max_length=100, unique=True)
    event_type = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)

    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_id} - {self.event_type}"