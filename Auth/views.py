import traceback
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from Auth.utility.utils import Validator
from .serializers import UserSerializer, UserSignInSerializer

class CreateUserView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)      #logger info
            return Response(data={"message": f"Something went wrong."}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SignInView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        try:
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
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)      #logger info
            return Response({"message": f"Something went wrong."}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
