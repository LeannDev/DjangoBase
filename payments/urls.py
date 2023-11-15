from django.urls import path

from .views import PaymentsView, PaymentSuccessView, CancelledSuccessView

urlpatterns = [
    path('<int:price>/', PaymentsView.as_view(), name='payments'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('cancelled/', CancelledSuccessView.as_view(), name='canceled'),
]