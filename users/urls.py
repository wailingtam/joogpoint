from django.conf.urls import url
from . import views
#
#
# urlpatterns = [
#     # url(r'^$', views.index, name='index'),
#     # url(r'^$', views.UserProfileList.as_view()),
#     # url(r'^(?P<pk>[0-9]+)/$', views.UserProfileDetail.as_view()),
#     # url(r'^(?P<username>[a-zA-Z0-9._]+)/$', views.detail, name='detail'),
#     url(r'^$', views.UserList.as_view(), name='user-list'),
#     url(r'^(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
#
# ]


from users.views import UserViewSet
from rest_framework import renderers

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    # url(r'^login/$', views.user_login),
    # url(r'^logout/$', views.user_logout),
]