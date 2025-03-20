from rest_framework import generics
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    #API endpoint for user registration.
    #Accepts POST requests with username, email, password, and password2.
    serializer_class = UserRegistrationSerializer
