from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from  core.models import User

from user.serializers import UserSeralizer, AuthTokenSerializer

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSeralizer

class  ListUserView(generics.ListAPIView):
    serializer_class = UserSeralizer
    queryset = User.objects.all()   


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    print("***Serializer_Class***")
    print(serializer_class)
    print("***Renderer_Classes***")
    print(renderer_classes)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSeralizer
    authentication_classes = (authentication.TokenAuthentication,)    
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user
    
