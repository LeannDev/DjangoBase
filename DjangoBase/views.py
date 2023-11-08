from django.views import View
from django.shortcuts import render

from payments.api import create_paypal_payment

class HomeView(View):
    # Define the name of the template to be used
    template_name = 'home.html'

    def get(self, request):
        
        # Create a dictionary of variables to be used in the template
        context = {

        }

        # Render the template with the context variables
        return render(request, self.template_name, context)
    
    def post(self, request):

        form = request.POST

        print(form)

        # Create a dictionary of variables to be used in the template
        context = {

        }

        return render(request, self.template_name, context)