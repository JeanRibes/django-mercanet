from rest_framework import serializers


class MercanetTransactionRequestSerialier(serializers.Serializer):
    transactionReference = serializers.CharField(required=True)
    amount = serializers.CharField(required=True)
    normalReturnUrl = serializers.CharField(required=True)

    merchantId = serializers.CharField(required=True)
    automaticResponseUrl = serializers.CharField(required=True)
    orderChannel = serializers.CharField(required=True)
    currencyCode = serializers.CharField(required=True)
    interfaceVersion = serializers.CharField(required=True)
    keyVersion = serializers.CharField(required=True)
