from django.contrib import admin

from .models import PaypalModel, SinglePaymentModel

admin.site.register(PaypalModel)
admin.site.register(SinglePaymentModel)