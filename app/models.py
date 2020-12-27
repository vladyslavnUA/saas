from django.db import models
from django.contrib.auth.models import AbstractUser
from djstripe.models import Customer, Subscription


class PayingPeople(models.Model):
    # person = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
	subscription = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.CASCADE)