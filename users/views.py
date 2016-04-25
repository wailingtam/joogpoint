from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, filters
from .serializers import UserSerializer#, UserProfileSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
# from .models import UserProfile


# def index(request):
#     # the minus sign means in a descendant order
#     ul = get_list_or_404(User)
#     # users_list = UserProfile.objects.order_by('-id')
#     output = ', '.join([u.email for u in ul])
#     return HttpResponse(output)
#
#
# def detail(request, username):
#     u = get_object_or_404(User, username=username)
#     # try:
#     #     u = User.objects.get(username=username)
#     # except User.DoesNotExist:
#     #     raise Http404("User does not exist")
#     return HttpResponse("You're looking at user %s profile." % username)


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer


# We'd like to just use read-only views for the user representations,
# so we'll use the ListAPIView and RetrieveAPIView generic class based views.

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('username',)


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


# class UserProfileList(generics.ListCreateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#
#
# class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
