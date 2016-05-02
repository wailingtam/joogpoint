from re import sub
from rest_framework.authtoken.models import Token


class OrganizationMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        if header_token is not None:
            try:
                token = sub('Token ', '', request.META.get('HTTP_AUTHORIZATION', None))
                token_obj = Token.objects.get(key = token)
                request.user = token_obj.user
            except Token.DoesNotExist:
                pass
        # This is now the correct user
        # print (request.user)
