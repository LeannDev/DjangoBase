from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ProfileModel

class ProfileView(LoginRequiredMixin, View):

    login_url = '/registration/login/'

    def get(self, request):

        profile = ProfileModel.objects.get(user=request.user)

        context = {
            'profile': profile
        }

        return render(request, 'profile.html', context)