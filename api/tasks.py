from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_order_confirmation_mail(order_id, user_email):
    """
    Send an order confirmation email to the user.
    """
    subject = "Order Confirmation"
    message = f"Your order with ID {order_id} has been confirmed."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    return send_mail(subject, message, from_email, recipient_list)
