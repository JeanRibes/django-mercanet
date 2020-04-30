from collections import OrderedDict

from django.conf import settings
from rest_framework import serializers

from mercanet.models import TransactionMercanet
from mercanet.utils import compute_seal

secret = settings.MERCANET["SECRET_KEY"]


class TransactionMercanetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionMercanet
        exclude = ['transactionDateTime', 'responseCode']

    amount = serializers.CharField(required=True)
    orderId = serializers.CharField(required=True)

    merchantId = serializers.CharField(required=True)  # ces champs ne sont pas sauvegardé en DB
    automaticResponseUrl = serializers.CharField(required=True)
    orderChannel = serializers.CharField(required=True)
    currencyCode = serializers.CharField(required=True)
    interfaceVersion = serializers.CharField(required=True)
    keyVersion = serializers.CharField(required=True)


class TransactionMercanetSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['normalReturnUrl']
        model = TransactionMercanet

    transactionReference = serializers.CharField(required=True)  # il faut le redéfinir pour enlever le 'unique'


def seal_transaction(transaction: TransactionMercanet, secret=secret) -> dict:
    transaction.to_mercanet_request()  # rajoute les bons champs
    mercanet_data = TransactionMercanetRequestSerializer(transaction).data
    seal = compute_seal(mercanet_data, secret)

    mercanet_data = TransactionMercanetRequestSerializer(transaction).data
    mercanet_data['seal'] = seal  # on rajoute ce qui ne peut être inclus dans le Seal
    mercanet_data["sealAlgorithm"] = "HMAC-SHA-256"
    sorted(mercanet_data)  # je crois qu'il préfère comme ça
    return OrderedDict(mercanet_data)
