from django.contrib.auth import get_user_model, login, logout
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from users.enums import AuthActions
from users.serializers import RegisterSerializer, LoginSerializer, MeSerializer

User = get_user_model()


class AuthViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    def get_serializer(self, *args, **kwargs) -> ModelSerializer:
        actions = {
            AuthActions.REGISTER: RegisterSerializer,
            AuthActions.LOGIN: LoginSerializer,
            AuthActions.ME: MeSerializer,
            AuthActions.LOGOUT: MeSerializer
        }
        serializer = actions.get(self.action)
        if serializer is None:
            return None
        return serializer(*args, **kwargs)

    def get_permissions(self) -> tuple[BasePermission]:
        if self.action in [AuthActions.REGISTER, AuthActions.LOGIN]:
            NotAuthenticated = ~IsAuthenticated
            return (NotAuthenticated(), )
        elif self.action in [AuthActions.ME, AuthActions.LOGOUT]:
            return (IsAuthenticated(),)
        return ()

    @action(["post"], detail=False)
    def register(self, request: Request, *_args, **_kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)

    @action(["post"], detail=False)
    def login(self, request: Request, *_args, **_kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.instance
        login(request=request, user=user)
        return Response(serializer.data)

    @action(["post"], detail=False)
    def me(self, request: Request, *_args, **_kwargs) -> Response:
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(["post"], detail=False)
    def logout(self, request: Request, *_args, **_kwargs) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)
