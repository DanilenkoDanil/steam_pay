from django.db import models
from django.contrib.auth.models import User


class Code(models.Model):
    code = models.CharField(unique=True, max_length=200)
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    username = models.CharField(max_length=200)
    error = models.TextField()
    date = models.DateTimeField(auto_created=True, null=True, blank=True)


class UserLimitation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    now_balance = models.FloatField(default=0)


class Payment(models.Model):
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    username = models.CharField(max_length=200)
    error = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True, blank=True)


class Setting(models.Model):
    qiwi_limit = models.FloatField(default=100000)
    digi_code = models.TextField(unique=True)
    seller_id = models.IntegerField()
    auto_course = models.BooleanField(default=False)
    course = models.FloatField()


class Qiwi(models.Model):
    qiwi_code = models.TextField(unique=True)
    current_counter = models.FloatField(default=0)
    timer = models.DateTimeField(auto_created=True, auto_now_add=True)


class Interhub(models.Model):
    token = models.TextField(unique=True)
    balance = models.FloatField(default=0)
