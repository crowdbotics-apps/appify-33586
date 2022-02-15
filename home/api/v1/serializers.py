from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from allauth.account import app_settings as allauth_settings
from allauth.account.forms import ResetPasswordForm
from allauth.utils import email_address_exists, generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer
from home.models import App, Plan, Subscription

User = get_user_model()


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = ('id', 'name', 'description', 'type', 'framework', 'domain_name',
                  'screenshot', 'subscription', 'user', 'created_at', 'updated_at')
        read_only_fields = ('id', 'screenshot', 'subscription',
                            'user', 'created_at', 'updated_at')
        url_field_name = 'screenshot'

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def create(self, validated_data):
        app = App(
            name=validated_data.get('name'),
            description=validated_data.get('description'),
        )
        app.save()
        return app

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ('id', 'name', 'description',
                  'price', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def create(self, validated_data):
        plan = Plan(
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            price=validated_data.get('price'),
        )
        plan.save()
        return plan

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('id', 'user', 'plan', 'app',
                  'active', 'created_at', 'updated_at')
        extra_kwargs = {
            'plan': {
                'required': True
            },
            'app': {
                'required': True
            },
            'active': {
                'required': True
            }
        }
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def create(self, validated_data):
        subscription = Subscription(
            plan=validated_data.get('plan'),
            active=validated_data.get('active'),
            user=validated_data.get(
                'user'),
            app=validated_data.get('app'),
        )
        subscription.save()
        return subscription

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            }
        }

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            username=generate_unique_username([
                validated_data.get('name'),
                validated_data.get('email'),
                'user'
            ])
        )
        user.set_password(validated_data.get('password'))
        user.save()
        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class PasswordSerializer(PasswordResetSerializer):
    """Custom serializer for rest_auth to solve reset password error"""
    password_reset_form_class = ResetPasswordForm
