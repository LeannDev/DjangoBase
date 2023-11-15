from django.views import View
from django.views.generic import DetailView
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from .settings import PP_API_URL, PP_CLIENT_ID, PP_SECRET
from payments.api import create_paypal_payment, new_access_token, get_access_token
from user.models import User

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

        # form = request.POST
        link = get_access_token(PP_API_URL, PP_CLIENT_ID, PP_SECRET)
        print(link)

        # Create a dictionary of variables to be used in the template
        context = {

        }

        return render(request, self.template_name, context)
    
class PricingView(View):
    
    template_name = 'pricing.html'

    def get(self, request):
        
        context = {

        }

        return render(request, self.template_name, context)
    
class ToolsView(View):

    template_name = 'tools.html'

    def get(self, request):
        
        context = {
            'premium': request.user
        }

        return render(request, self.template_name, context)