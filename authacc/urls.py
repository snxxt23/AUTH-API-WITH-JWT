from django.urls import path,include
from . import views


urlpatterns = [
    path('registration/',views.UserRegistrationView.as_view(),name='registration')
]
