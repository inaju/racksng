# models.py in the users Django app
from django.db import models
from django.contrib.auth.models import AbstractUser
from mainracks import Racks, customer


GENDER_SELECTION = [
    ("M", "Male"),
    ("F", "Female"),
    ("NS", "Not Specified"),
]
ACCOUNT_TYPE_SELECTION = [
    ("Business", "Business"),
    ("Personal", "Personal"),
]


class RacksUser(AbstractUser):
    bitnob_id = models.CharField(max_length=100)
    username = models.CharField(max_length=20, unique=True)
    type_of_account = models.CharField(max_length=20, choices=ACCOUNT_TYPE_SELECTION)
    # We don't need to define the email attribute because is inherited from AbstractUser
    phone_number = models.CharField(max_length=30)
    btc_address = models.CharField(max_length=50)
    qr_code = models.ImageField()
    btc_balance = models.CharField(max_length=30)
    naira_balance = models.CharField(max_length=30)

    def __str__(self):
        return str(self.username) + " BTC:" + str(self.btc_balance)


class TransactionInfo(models.Model):
    racks_user = models.ForeignKey(RacksUser, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    btc_amount = models.CharField(max_length=30)
    amount = models.CharField(max_length=30)

    def __str__(self):
        return str(self.racks_user) + " " + str(self.btc_amount)
