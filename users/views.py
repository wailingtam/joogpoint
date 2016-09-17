from django.contrib.auth.models import User
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import list_route
from rest_framework import response, status
from .serializers import UserSerializer, ProfileSerializer
from .models import Profile
from users.permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.AllowAny,)
        return super(UserViewSet, self).get_permissions()

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('username',)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'DELETE':
            self.permission_classes = (permissions.IsAdminUser,)
        return super(ProfileViewSet, self).get_permissions()

    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('user__username',)

    # Associating profiles with users
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @list_route()
    def me(self, request):
        my_profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(my_profile, context={'request': request})
        return response.Response(serializer.data, status=status.HTTP_200_OK)
