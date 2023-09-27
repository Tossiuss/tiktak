from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .permissions import IsActivePermission
from rest_framework import status
from .serializers import (
    RegistrationSerializer, 
    ActivationSerializer, 
    LoginSerializer, 
    ChangePasswordSerializer, 
    DeleteAccountSerializer,
    AdminDeleteUserSerializer,
    UpdateUserSerizlizer,
    CustomUserSerializer,
    ForgotPassordSerializer,
    ForgotPasswordCompleteSerializer,
    FollowerSerializer,
)
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from .models import User, Follower


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer


class ActivationView(CreateAPIView):
    serializer_class = ActivationSerializer


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsActivePermission]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response(
            'Вы успешно вышли из своего аккаунта'
        )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer())
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response(
            'Пароль успешно обнавлен', status=200
        )


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=DeleteAccountSerializer())
    def post(self, request):
        serializer = DeleteAccountSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                user.delete()
                return Response({'message': 'Аккаунт успешно удален'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'Неверные почта и/или пароль'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AdminDeleteUserView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=AdminDeleteUserSerializer())
    def post(self, request):
        serializer = AdminDeleteUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            user.delete()
            return Response({'message': f'Пользователь с email {email} успешно удален'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'Пользователь с указанным email не найден'}, status=status.HTTP_404_NOT_FOUND)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UpdateUserSerizlizer())
    def patch(self, request):
        serializer = UpdateUserSerizlizer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class ProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPassordSerializer())
    def post(self, request):
        serializer = ForgotPassordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response("Проверье почту")


class ForgotPasswordCompleteView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordCompleteSerializer())
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Пароль успешно изменен")


class FollowAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer

