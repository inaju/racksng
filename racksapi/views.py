import requests
from users.models import RacksUser, TransactionInfo
from .serializers import UserDetailSerializer, TransactionInfoSerializer
from rest_framework import generics
from mainracks import Racks
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from decimal import Decimal

#

racks = Racks()


class UserDetailList(generics.ListCreateAPIView):

    queryset = RacksUser.objects.all()
    serializer_class = UserDetailSerializer


# @csrf_exempt
@api_view(["POST"])
def send_btc_again(request):
    data = request.POST

    current_user = request.user
    print(current_user.email)
    send_onchain = racks.send_onchain_bitcoin(
        satoshis=int(data["amount"]),
        address=data["address"],
        customerEmail=str(current_user.email),
        description="sending funds",
    )

    print(send_onchain["data"])
    racks_user = RacksUser.objects.get(email=current_user.email)
    racks_user.btc_balance -= float(0.00000001) * float(data["amount"])
    print(racks_user.btc_balance)

    # print(float(0.00000001), type(float(data["amount"])))
    # print(float(data["amount"]), type(float(data["amount"])))
    print(Decimal(0.00000001) * Decimal(data["amount"]))
    print(racks_user.naira_balance, racks_user.btc_balance)
    # print(
    #     racks_user.btc_balance
    #     - (float("0.00000001") * float(data["amount"]) * float(23305515.26))
    # )
    abs_sum_amount = abs(
        racks_user.btc_balance
        - (float(0.00000001) * float(data["amount"]) * float(23305515.26))
    )
    print(abs_sum_amount)
    racks_user.naira_balance -= abs_sum_amount

    print(racks_user.naira_balance)
    racks_user.save()
    print()
    print(racks_user.id)
    payload = {
        "racks_user": racks_user.id,
        "reference": send_onchain["data"]["reference"],
        "address": send_onchain["data"]["address"],
        "transaction_id": send_onchain["data"]["id"],
        "btc_amount": send_onchain["data"]["btcAmount"],
        "amount": send_onchain["data"]["amount"],
    }
    if request.method == "POST":
        serializer = TransactionInfoSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # print(request.POsST)
    return Response(request.POST)


@api_view(["GET"])
def transaction_info(request):
    count = 0
    return_data = []
    user_id = request.user.id
    transaction_info = TransactionInfo.objects.filter(racks_user=user_id)
    for info in transaction_info:
        data = {
            "amount": info.amount,
            "reference": info.reference,
            "address": info.address,
            "transaction_id": info.transaction_id,
            "btc_amount": info.btc_amount,
            "status": racks.fetch_transaction_status(id=str(info.transaction_id)),
        }
        return_data.append(data)
        count += 1

    return Response(return_data)

    # data = request.POST
