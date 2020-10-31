from django.db import models

# Create your models here.
class Transaction(models.Model):
	transaction_type = models.TextField(blank = False, null = False)
	amount = models.PositiveIntegerField(default=0)
	parent_id = models.PositiveIntegerField()