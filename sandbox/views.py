from django.contrib.auth import authenticate, login, logout
from django.forms import model_to_dict
from rest_framework.exceptions import AuthenticationFailed

from sandbox.helpers import (JSONResponse,
                             SandboxGenericView, )
from sandbox.models import User
from sandbox.serializers import AuthSerializer
from sandbox.utils.roles import IsAuthorized


class AuthAPI(SandboxGenericView):
    serializer_class_receive = AuthSerializer
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = self.validated_data['username']
        password = self.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            response_data = {
                'last_name': request.user.last_name,
                'first_name': request.user.first_name,
                'session_id': request.session.session_key,
            }
            response = JSONResponse(response_data)

            return response

        else:
            raise AuthenticationFailed

    def delete(self, request, *args, **kwargs):
        logout(request)

        return JSONResponse()


class UsersAPI(SandboxGenericView):
    permission_classes = (IsAuthorized, )

    def get(self, *args, **kwargs):
        users_data = []
        for user in User.objects.all():
            users_data.append(model_to_dict(user))

        return JSONResponse(users_data)
