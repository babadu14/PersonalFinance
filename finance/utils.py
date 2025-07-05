from django.core.mail import send_mail
from django.conf import settings


def create_budget_and_notify(user_email, feedback_url):
    send_mail(
        subject="✅ Your Budget Has Been Created!",
        message=f"Hello!\n\nYour budget has been successfully created. You can view the budget here:\n\n{feedback_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )