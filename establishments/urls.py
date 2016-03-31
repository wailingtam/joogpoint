# from django.conf.urls import url, include
# from rest_framework.urlpatterns import format_suffix_patterns
# from establishments import views
# 
# urlpatterns = [
#     url(r'^$', views.api_root),
#     url(r'^establishments/$', views.EstablishmentList.as_view(), name='establishment-list'),
#     url(r'^establishments/(?P<pk>[0-9]+)/$', views.EstablishmentDetail.as_view(), name='establishment-detail'),
# ]
# 
# urlpatterns = format_suffix_patterns(urlpatterns)
# 
# # Login and logout views for the browsable API
# # urlpatterns += [
# #     url(r'^api-auth/', include('rest_framework.urls',
# #                                namespace='rest_framework')),
# # ]

from establishments.views import EstablishmentViewSet
from rest_framework import renderers

establishment_list = EstablishmentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

establishment_detail = EstablishmentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})