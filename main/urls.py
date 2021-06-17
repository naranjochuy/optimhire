from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CurrentExchangeRateAPIView


router = DefaultRouter()

urlpatterns = [
    path('current-exchange-rate/', CurrentExchangeRateAPIView.as_view())
]

urlpatterns += router.urls
