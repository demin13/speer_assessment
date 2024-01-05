from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from Auth.utility.utils import Validator, handle_exceptions
from .serializers import UserSerializer, UserSignInSerializer

class CreateUserView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @handle_exceptions
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    @handle_exceptions
    def post(request):
        serializer = UserSignInSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['email'],
                                password=serializer.validated_data['password'])
            if user:
                refresh = RefreshToken.for_user(user)
                return Response(data={
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }, status=status.HTTP_200_OK)
            return Response(data={'message': 'Invalid credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response(data={"message": Validator.TrimSerializerError(serializer.errors)},
                        status=status.HTTP_400_BAD_REQUEST)
