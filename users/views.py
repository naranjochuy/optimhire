from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from .models import User
from .serializers import LoginSerializer


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.object.get('email')
        password = serializer.object.get('password')
        credentials = {'email': email, 'password': password}

        try:
            user = User.objects.select_related().get(email=email)
        except User.DoesNotExist:
            msg = f"The email '{email}' is not registered."
            return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_active:
            msg = f"The email '{email}' is inactive."
            return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

        auth = authenticate(**credentials)

        if not auth:
            msg = 'Incorrect password.'
            return Response({'error': msg}, status=status.HTTP_401_UNAUTHORIZED)

        payload = jwt_payload_handler(auth)

        response = {
            'email': email,
            'token': jwt_encode_handler(payload),
            'full_name': f'{user.first_name} {user.last_name}'
        }

        return Response(response, status=status.HTTP_200_OK)
