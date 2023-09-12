from django.urls import path,include
from . import views


urlpatterns = [
    path('registration/',views.UserRegistrationView.as_view(),name='registration'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('profile/',views.UserProfileView .as_view(),name='profile'),
    
    
]
