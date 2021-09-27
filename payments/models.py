from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Transaction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False,null=True) 
    order_id = models.CharField(max_length=30, blank=False, null=True)
    txn_id = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=30, blank=True, null=True)
    amount_initiated = models.FloatField(blank=True, null=True)
    was_success = models.BooleanField(default=False)
    status = models.CharField(max_length=30, blank=True, null=True)
    log = models.TextField(null=True, blank=True)
    registered_for = models.TextField(null=True, blank=True)
    txn_date = models.DateTimeField(default=timezone.now, blank=True)
    ru_date = models.DateTimeField(blank=True, null=True)
    s2s_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.owner.id} [{self.order_id}]'


class Amount(models.Model):
	amount = models.FloatField()

	def __str__(self):
		return str(self.amount)
