from django.urls import path
from .views import WebhookPaymentView, PaymentEventsView

urlpatterns = [
    path('webhook/payments', WebhookPaymentView.as_view()),
    path('payments/<str:payment_id>/events', PaymentEventsView.as_view()),
]