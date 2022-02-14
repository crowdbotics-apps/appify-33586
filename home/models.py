from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator


class App(models.Model):
    id = models.BigAutoField("ID", primary_key=True)
    name = models.CharField("Name", max_length=50)
    description = models.CharField("Description", max_length=255)
    type = models.CharField("Type", max_length=50, choices=(
        ('web', 'Web'), ('mobile', 'Mobile')))
    framework = models.CharField(
        "Framework", max_length=50, choices=(('django', 'Django'), ('react_native', 'React Native')))
    domain_name = models.CharField("Domain name", max_length=50)
    screenshot = models.URLField("Screenshot")
    ssubscription = models.IntegerField("Subscription")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Plan(models.Model):
    id = models.BigAutoField("ID", primary_key=True)
    name = models.CharField("Name", max_length=20)
    description = models.CharField("Description", max_length=255)
    price = models.FloatField("Price")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    id = models.BigAutoField("ID", primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,)

    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, verbose_name="Plan")
    sapp = models.ForeignKey(
        App, on_delete=models.CASCADE, verbose_name="App")
    active = models.BooleanField("Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
