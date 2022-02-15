from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.api.v1.viewsets import (
    PlanViewSet,
    SignupViewSet,
    LoginViewSet,
    AppViewSet,
    SubscriptionViewSet,
)

router = DefaultRouter()
router.register("apps", AppViewSet, basename="app")
router.register("plans", PlanViewSet, basename="plan")
router.register("subscriptions", SubscriptionViewSet, basename="subscription")
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")

urlpatterns = [
    path("", include(router.urls)),
]
