from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, filters, permissions
from .serializers import UserSerializer, ProfileSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .models import Profile
from users.permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('username',)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    # Associating profiles with users
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# def user_login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             # Redirect to a success page.
#             return HttpResponseRedirect("/account/loggedin/")
#         # else:
#             # Return a 'disabled account' error message
#     else:
#         # Return an 'invalid login' error message.
#         # Show an error page
#         return HttpResponseRedirect("/account/invalid/")
#
#
# def user_logout(request):
#     logout(request)
#     # Redirect to a success page.
#     return HttpResponseRedirect("/account/loggedout/")
