from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .utils import send_activation_code, send_activation_code_on_forgot_password
from .models import User
from django.db.models import F


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(min_length=5,required=False)


    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Эта почта уже зарегистрированна'
            )
        return email
    
    def validate_name(self, name):
        if User.objects.filter(name=name).exists():
            raise serializers.ValidationError(
                'Данный ник принадлежит другому пользователю'
            )
        return name

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)        
        return user
    
    def to_representation(self, instance):
        return {"message": "Аккаунт успешно создан"}


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            request.user.name = serializer.validated_data['name']
            request.user.save()
            return Response({'message': 'Ник изменён'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        return attrs
    
    
    def create(self, validated_data):
        user = User.objects.get(email=validated_data.get('email'))
        user.is_active = True
        user.activation_code = ''
        user.save()
        return user
    
    def to_representation(self, instance):
        return {"message": "Аккаунт активирован"}


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        return email
    
    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email,password=password,request=request)

            if not user:
                raise serializers.ValidationError(
                    'Не верный email или пароль'
                )
            
        else:
            raise serializers.ValidationError(
                'Email и password обязательны для заполнения'
            )
        
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=4, required=True)
    new_password = serializers.CharField(min_length=4, required=True)
    new_password_confirm = serializers.CharField(min_length=4, required=True)

    def validate_old_password(self, old_password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                'Введите корректный пароль'
            )
        return old_password
    
    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        if new_password == old_password:
            raise serializers.ValidationError(
                'Старый и новый пароли совпадают'
            )
        return attrs
    
    def set_new_password(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()


class DeleteAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class AdminDeleteUserSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'description', 'avatar', 'is_staff')
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     try:
    #         representation["followers"] = CustomUserSerializer(
    #             instance.followers.annotate(
    #                 email=F("user__email"), 
    #                 name=F("user__name"), 
    #                 description=F("user__description"), 
    #                 avatar=F("user__avatar"), 
    #                 is_staff=F("user__is_staff")
    #             ), 
    #             many=True
    #         ).data
    #         representation["follows"] = CustomUserSerializer(
    #             instance.follows.annotate(
    #                 email=F("follow__email"), 
    #                 name=F("follow__name"), 
    #                 description=F("follow__description"), 
    #                 avatar=F("follow__avatar"), 
    #                 is_staff=F("follow__is_staff")
    #             ), 
    #             many=True
    #         ).data
    #     except AttributeError:
    #         pass
    #     return representation


class UpdateUserSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'description', 'avatar')


class ForgotPassordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email does not exists")
        return email
    
    def send_code(self):
        user = User.objects.get(email=self.validated_data["email"])
        user.is_active = False
        user.create_activation_code()
        send_activation_code_on_forgot_password(user.email, user.activation_code)


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError("invalid code")
        return code
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("passwords do not match")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.get(activation_code=validated_data["code"])
        user.is_active = True
        user.set_password(validated_data["password"])
        user.save()
        return user


# class FollowerSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)

#     def validate_email(self, email):
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError("User with this email does not exists")
#         return email
    
#     def create(self, validated_data):
#         follower = User.objects.get(email=validated_data["email"])
#         user = self.context["request"].user
#         if Follower.objects.filter(user=user, follow=follower).exists():
#             Follower.objects.filter(user=user, follow=follower).delete()
#         else:
#             Follower.objects.create(user=user, follow=follower)
#         return user
