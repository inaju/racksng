# serializers.py in the users Django app
from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from users.models import GENDER_SELECTION, ACCOUNT_TYPE_SELECTION
from mainracks import Racks, customer
from generate_qrcode import generate
import os
from decimal import Decimal

from users.models import RacksUser, TransactionInfo


racks = Racks()


class CustomRegisterSerializer(RegisterSerializer):
    # gender = serializers.ChoiceField()
    phone_number = serializers.CharField(max_length=30)
    username = serializers.CharField(max_length=20)
    type_of_account = serializers.ChoiceField(choices=ACCOUNT_TYPE_SELECTION)

    """        
  
        """

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        print(self.data.get("first_name"))
        if True:
            print(self.data.get("first_name"))
            payload = {
                "email": self.data.get("email"),
                "firstName": self.data.get("first_name"),
                "lastName": self.data.get("last_name"),
                "phone": self.data.get("phone_number"),
                "countryCode": "+234",
            }
            customer.create_customer(body=payload)

        user = super().save(request)
        user.username = self.data.get("username")
        user.type_of_account = self.data.get("type_of_account")
        user.phone_number = self.data.get("phone_number")

        user.btc_address = racks.generate_onchain_address_bitcoin(
            label="generating btc address for " + self.data.get("email"),
            customerEmail=self.data.get("email"),
        )["data"]["address"]
        generate(url=user.btc_address, user=self.data.get("username"))
        user.qr_code = os.path.join("static", str(self.data.get("username")) + ".png")
        user.btc_balance = Decimal(0.04)
        user.naira_balance = Decimal(1000000)
        # customer.get_customer_by_email(self.data.get("email"))
        user.bitnob_id = customer.get_customer_by_email(self.data.get("email"))["data"][
            "id"
        ]
        user.save()
        return user


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        data["user"] = user
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RacksUser
        fields = [
            "bitnob_id",
            "username",
            "type_of_account",
            "btc_address",
            "qr_code",
            "btc_balance",
            "naira_balance",
            "email",
        ]


class TransactionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionInfo
        fields = [
            "racks_user",
            "reference",
            "address",
            "transaction_id",
            "btc_amount",
            "amount",
        ]
