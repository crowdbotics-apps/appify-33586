from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from home.models import App, Plan, Subscription
from django.http import JsonResponse

from home.api.v1.serializers import (
    SignupSerializer,
    UserSerializer,
    AppSerializer,
    PlanSerializer,
    SubscriptionSerializer,
)


class AppViewSet(ModelViewSet):
    serializer_class = AppSerializer
    http_method_names = ["post", "get", "put", "patch", "delete"]
    queryset = ''

    def get_queryset(self, *args, **kwargs):
        super(AppViewSet, self).get_queryset(*args, **kwargs)
        queryset = App.objects.all()
        return queryset


class PlanViewSet(ModelViewSet):
    serializer_class = PlanSerializer
    http_method_names = ["get", "post"]
    queryset = ''

    def get_queryset(self, *args, **kwargs):
        super(PlanViewSet, self).get_queryset(*args, **kwargs)
        queryset = Plan.objects.all()
        return queryset


class SubscriptionViewSet(ModelViewSet):
    serializer_class = SubscriptionSerializer
    http_method_names = ["post", "get", "put", "patch", "delete"]
    queryset = ''

    def get_queryset(self, *args, **kwargs):
        super(SubscriptionViewSet, self).get_queryset(*args, **kwargs)
        queryset = Subscription.objects.all()
        return queryset


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})
