from django.db import models
from django.utils import timezone

from user.models import User

class PaypalModel(models.Model):

    app_id = models.CharField(max_length=25)
    access_token = models.CharField(max_length=100)
    expires_in = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PayPal'
        verbose_name_plural = 'PayPal'

    def __str__(self):
        return f"app ID: {self.app_id}"
    
class SinglePaymentModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    payment_method = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    is_successful = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Set the expiration date 30 days after the payment date
        if self.is_successful and not self.expiration_date:
            self.expiration_date = self.payment_date + timezone.timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {self.payment_date}"
    