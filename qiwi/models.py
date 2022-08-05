from django.db import models


class Code(models.Model):
    code = models.CharField(unique=True, max_length=200)
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    username = models.CharField(max_length=200)


class Qiwi(models.Model):
    code = models.TextField(unique=True)
