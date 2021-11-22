from dotenv import load_dotenv
from bitnob import Customer, Lightning, Onchain
import uuid
import requests
import os
import environ

env = environ.Env()
environ.Env.read_env()

load_dotenv()

# print(os.environ(BITNOB_API_KEY))
"""
so here is how it works on the Lightning network
To Receive bitcoin via Lightning Network
1. Create Invoice
2. Send to the person

"""

"""
sign up
when you sign up, you'll get a QR code 


"""


customer = Customer()
lightning = Lightning()
onchain = Onchain()


# print(customer.get_customer_by_email("to@gmail.com"))

# print(customer.get_customer_by_email(email="godsstar360@gmail.com"))

"""
d28eb63b-c981-4965-ac54-4b04920001eb
"""


class Racks:
    def __init__(self):
        self.customer_url = "https://sandboxapi.bitnob.co/api/v1/customers/"

    def get_customer(self, id):

        url = self.customer_url + str(id)

        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + env("BITNOB_API_KEY"),
        }

        response = requests.request("GET", url, headers=headers)

        print(response.text)

    def fetch_transaction_status(self, id):
        url = "https://sandboxapi.bitnob.co/api/v1/transactions/" + str(id)
        # url = "https://sandboxapi.bitnob.co/api/v1/transactions/8bdeb417-dfb8-4ad1-b822-aa56e59e625b"

        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + env("BITNOB_API_KEY"),
        }

        response = requests.request("GET", url, headers=headers)

        try:
            status_list = []
            count = 0
            while True:

                status = response.json()["data"]["status"]
                if status not in status_list:
                    status_list.append(status)
                else:
                    break
                print(status_list)

        except:
            pass

        return status_list[0]

    def get_customer_by_email(self, email):

        url = self.customer_url + "/fetch_customer"

        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + env("BITNOB_API_KEY"),
        }
        body = {"email": +str(email)}

        response = requests.request("POST", url, headers=headers, body=body)

        print(response.text)

    def send_onchain_bitcoin(self, satoshis, address, customerEmail, description):

        body = {
            "satoshis": satoshis,
            "address": address,
            "customerEmail": str(customerEmail),
            "description": str(description),
            "priorityLevel": "high",
        }
        data = onchain.send_bitcoin(body=body)

        return data

    def generate_onchain_address_bitcoin(self, label, customerEmail):

        body = {
            "label": label,
            "customerEmail": str(customerEmail),
        }
        data = onchain.generate_address(body=body)

        return data

    def create_lightning_invoice_for_user(self, email, sats):
        payload = {
            "description": "receiving " + str(sats),
            "tokens": sats,
            "private": False,
            "is_including_private_channels": False,
            "is_fallback_included": False,
            "customerEmail": email,
        }
        data = lightning.create_invoice(body=payload)
        return data

    def pay_lightning_invoice(self, request, email):
        payload = {
            "request": request,
            "reference": str(uuid.uuid4()),
            "customerEmail": email,
        }
        data = lightning.pay_invoice(body=payload)
        return data

    def initiate_ligtning_payment(self, invoice_id):
        data = lightning.initiate_payment(invoice_id)
        return data


client_htlc_wallet_address = "3d57b733-eaed-4954-9a24-d4e032e11535"
rack = Racks()
user_email = "nathan@gmail.com"
sats = 5000

body = {
    "email": "acustomer@gmail.com",
    "firstName": "aCustomerfirstName",
    "lastName": "aCustomerlastName",
    "phone": "9xxxxxxxx",
    "countryCode": "+234",
}

# print(rack.fetch_transaction(id="d54c6f41-5ca2-47ee-9f0f-1917a16ac18a"))

# print(customer.create_customer(body=body))
# print()

"generate address for customer"
# generate_btc_address = rack.generate_onchain_address_bitcoin(
#     label="car wash business", customerEmail="carwash@gmail.com"
# )
# customer_address = generate_btc_address["data"]["address"]

"""
receive/request for funds by creating an invoice (create_lightning_invoice_for_user) 

"""
# request = rack.create_lightning_invoice_for_user(email=user_email, sats=sats)["data"][
#     "request"
# ]
# print(request)

customer_address = "tb1qlacujns46w0l9swf85hgay74dgmwe7k7ce2qmh"


"""
Send BTC onChain

"""
# send_onchain = rack.send_onchain_bitcoin(
#     satoshis=sats,
#     address="tb1qrkasl8t0z7fqmhugy34vdgv59rxev7d25v6gay",
#     customerEmail="mitchel@gmail.com",
# )
# print(send_onchain)

"""
pay in btc by paying through a request

"""
# request = "lntb534u1pscaukapp5tul468x7qtl6vtmsvgxdxfxryjnv8kuaqf83qnwm7gages58p2zqdqqcqzpgxqyz5vqsp5pcam6hdfm99gvu9u4u2yrlsrqqwqesf3haqjcrw9njxpwhmvzpxq9qyyssq8x8khzxpwk02vq9440rryyqndnff0svu4mafetxskyqgqwlaedv82wxtg5jfu5sp2x98q7rraac3pe7sfgfmyavu69022prelc9nhscqjn7cqy"
# initiate_payment = rack.initiate_ligtning_payment(
#     # email="johndoe@gmail.com",
#     invoice_id=str(request),
# )

# print()
# print("initiate payment details")
# print(initiate_payment)
# print()

# create_invoice = rack.pay_lightning_invoice(
#     email="johndoe@gmail.com",
#     request=str(request),
# )["data"]

# print(create_invoice)


# print(request)
# request = "lntb350u1pscam4spp5csyaf9q4ywg32lwxaallxjpk9pf00va4cvlaw7g4kkecn7sdgv2sdqqcqzpgxqyz5vqsp5s4h7yzjskhwvzzad3x8asaz9n3llvlexc82y0zf3gkntxpld0rzq9qyyssqtty8pgzw6hj3xvy0pfjn7nnfwsfq4v0unyundzed8kepwu8vvrzytdy09f6hgl8k00a78kfwzvayxcgv3rhtkfwjdpyd7x4hctr85tgp3y90w6"


# print(initiate_payment)

# paymentRequest = create_invoice["paymentRequest"]
# invoiceId = create_invoice["invoiceId"]
# id = create_invoice["id"]
# address = create_invoice["address"]
# reference = create_invoice["reference"]

# # initiate_payment = rack.initiate_ligtning_payment(invoice_id=str(paymentRequest))

# print(create_invoice)
# print()
# print()
# print()
# print()
# print("paymentRequest:", paymentRequest)
# print("invoiceId:", invoiceId)
# print("id:", id)
# print("address:", address)
# print("reference:", reference)


class Tipping:
    def __init__(self):
        pass

    def get_user(self, email):
        user = customer.get_customer_by_email(email=email)
        return user

    def create_lightning_invoice_for_user(self, email, sats):
        payload = {
            "description": "money stops nonsense on sunday",
            "tokens": sats,
            "private": False,
            "is_including_private_channels": False,
            "is_fallback_included": False,
            "customerEmail": email,
        }
        data = lightning.create_invoice(body=payload)
        return data

    def generate_btc_address_for_user(self, email, label):
        payload = {
            "label": label,
            "customerEmail": email,
        }
        data = onchain.generate_address(body=payload)
        return data

    def tip_user(self, sats, email, label):
        invoice = self.create_lightning_invoice_for_user(email=email, sats=sats)
        address = self.generate_btc_address_for_user(email, label)
        data = {
            "address": address["data"]["address"],
            "invoice": invoice["data"]["request"],
        }
        return data


# tip = Tipping()
# invoice_id = "lntb50u1pscmq0kpp58w085c5t2djzg0nynlej56t633x2rh0cec4mtqywe5k5r3kraewqdpsd4hkueteypehgmmswvsxummwwdjkuum9yphkugrnw4hxgctecqzpgxqr23ssp500vf9nwdqc6grlclpar6vnkpzgw0mucd4p886llzay48fgm7tnlq9qyyssq63ywn2zeznpmrkjt5d0mnej4yz2wqct7w9qfxg7sc56nuskrj2f5xhmqasdapxq6puywuqfvlun2sy46rdfgfzj5d4ddja93cyz8hyqqtlttd0"
# print(lightning.get_invoice(invoice_id=invoice_id))

# # print(tip.tip_user(email="johnny@gmail.com", label="busd", sats=5000))
