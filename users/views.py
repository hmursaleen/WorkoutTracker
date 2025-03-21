from rest_framework import generics
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny

class UserRegistrationView(generics.CreateAPIView):
    #API endpoint for user registration.
    #Accepts POST requests with username, email, password, and password2.
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
