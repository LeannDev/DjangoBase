from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import HomeView, PricingView, ToolsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('tools/', ToolsView.as_view(), name='tools'),
    path('registration/', include('user.urls')),
    path('profile/', include('profiles.urls')),
    path('payments/', include('payments.urls')),
]

# Static files route
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)