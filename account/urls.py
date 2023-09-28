from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('delete_account/', DeleteAccountView.as_view()),
    path('admin_delete_user/', AdminDeleteUserView.as_view()),
    path('upload_profile/', UpdateUserView.as_view()),
    path('profile/<str:pk>/', ProfileView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password/complete/', ForgotPasswordCompleteView.as_view()),
    # path('follow/', FollowAPIView.as_view()),
]

