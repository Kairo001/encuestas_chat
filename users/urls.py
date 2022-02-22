""" Urls para la app de usuarios. """

# Django
from django.urls import path

# Vistas
from users import views

urlpatterns = [
    path('', views.InitView.as_view(), name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('updateuser/<pk>/', views.UpdateUserView.as_view(), name='updateuser'),
    path('forgotpassword/', views.ForgotPasswordView.as_view(), name="forgot_password"),
    path('resetpassword_validate/<uidb64>/<token>/', views.ResetPasswordValidateView.as_view(), name="reset_password_validate"),
    path('resetpassword/', views.ResetPasswordView.as_view(), name="reset_password"),
]