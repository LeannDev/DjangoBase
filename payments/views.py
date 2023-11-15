from django.shortcuts import render, redirect
from django.views import View

from DjangoBase.settings import PP_API_URL, PP_CLIENT_ID, PP_SECRET
from .api import get_access_token, create_paypal_payment

class PaymentsView(View):
    
    template_name = 'payments.html'

    def get(self, request, price):
        
        def validate_price(price, price_list):
            return price in price_list
        
        prices = [5, 10, 15, 20]

        validated_price = validate_price(price, prices)
        
        if validated_price:
            access_token = get_access_token(PP_API_URL, PP_CLIENT_ID, PP_SECRET)

            if access_token:
                payment_link = create_paypal_payment(PP_API_URL, access_token, price)
                if payment_link:
                    return redirect(payment_link)
        
        else:
            
            context = {

            }

            return render(request, self.template_name, context)
        
class PaymentSuccessView(View):

    template_name = 'success.html'

    def get(self, request):

        context = {

        }

        return render(request, self.template_name, context)
    
class CancelledSuccessView(View):

    template_name = 'cancelled.html'

    def get(self, request):

        context = {

        }

        return render(request, self.template_name, context)