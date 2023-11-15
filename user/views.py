from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import UserCreationForm
from .models import User

class SignUpView(CreateView):

    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    # Override the form_valid method to customize user creation logic
    def form_valid(self, form):
        # Set the 'is_active' attribute of the user to False before saving the form
        form.instance.is_active = False

        # Call the parent class's form_valid method to save the form and obtain the response
        response = super().form_valid(form)

        # Display a success message after successful registration
        messages.success(self.request, f"User registered. \nConfirm your email")

        # Return the response
        return response

class LoginView(LoginView):
    # Specify the name of the template to be used for rendering the login page
    template_name = 'login.html'

    # Handle the POST request for user login
    def post(self, request):
        # Extract username and password from the POST data
        username = request.POST['username']
        password = request.POST['password']

        # Try to get a user object with the provided username
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            # Handle the case where the user does not exist
            messages.error(request, 'Incorrect username or password')
            return redirect('login')

        # Check if the user is active
        if user.is_active:
            try:
                # Authenticate the user with the provided username and password
                user = authenticate(username=username, password=password)
                login(request, user)
                # Display a success message and redirect to the home page
                messages.success(request, f"Welcome @{self.request.user.username}")
                return redirect('home')
            except Exception as e:
                # Handle authentication failure
                messages.error(request, 'Incorrect username or password')
                return redirect('login')
        else:
            # Handle the case where the user is not active
            messages.warning(request, "The user is not active.\nContact support for more information.")
            return redirect('home')
        
def logout_view(request):
    logout(request)

    return redirect('home')