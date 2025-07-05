from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Budget
from .utils import create_budget_and_notify 

@receiver(post_save, sender=Budget)
def send_email_on_budget_create(sender,instance, created, **kwargs):
    if created:
        user = instance.user
        user_email = user.email
        feedback_url = f"http://127.0.0.1:8000/budgets/{instance.id}"
        create_budget_and_notify(user_email, feedback_url)
