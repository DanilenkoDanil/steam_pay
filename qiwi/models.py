from django.db import models


class Code(models.Model):
    code = models.CharField(unique=True, max_length=200)
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    username = models.CharField(max_length=200)
    error = models.TextField()


class Payment(models.Model):
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    username = models.CharField(max_length=200)
    error = models.TextField()


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
