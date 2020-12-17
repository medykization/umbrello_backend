from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authenticate.views import RegisterView,LogoutView


app_name="authenticate"

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', LogoutView.as_view(), name='auth_logout'),
    path('register', RegisterView.as_view()),
]