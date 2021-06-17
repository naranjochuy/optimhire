from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import LoginAPIView


router = DefaultRouter()

urlpatterns = [
    path('login/', LoginAPIView.as_view())
]

urlpatterns += router.urls
