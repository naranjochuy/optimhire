from datetime import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from utils.exchange_rate import ER


class CurrentExchangeRateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs):
        today = datetime.today()
        er =ER()
        data = er.get_data(today)
        return Response(data, status=status.HTTP_200_OK)
