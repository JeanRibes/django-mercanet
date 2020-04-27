import hashlib
import hmac

from dataclasses import dataclass
from django.conf import settings
from django.db import models

# Create your models here.
from mercanet.serializers import MercanetTransactionRequestSerialier

secret = bytearray(settings.MERCANET["SECRET_KEY"].encode("utf-8"))


@dataclass
class BaseTransactionMercanet:
    transactionReference: str
    amount: int
    normalReturnUrl: str


class MercanetTransactionRequest(BaseTransactionMercanet):
    """
    Objet représentant ce qui est envoyé à MercaNET
    """

    merchantId: str = settings.MERCANET["MERCHANT_ID"]
    automaticResponseUrl: str = settings.MERCANET["REPONSE_AUTO_URL"]
    orderChannel: str = "INTERNET"
    currencyCode: str = "978"
    interfaceVersion: str = "IR_WS_2.20"
    keyVersion: int = 1

    @property
    def seal(self) -> str:
        json_data = MercanetTransactionRequestSerialier(self).data
        json_data.pop("keyVersion", None)
        json_data.pop("sealAlgorithm", None)
        sorted(json_data)  # les clés doivent être en ordre alphabétique

        str_concat = ""
        for key in sorted(json_data.keys()):
            str_concat += str(json_data[key])

        seal = hmac.new(
            key=secret,
            msg=bytearray(str_concat.encode("utf-8")),
            digestmod=hashlib.sha256,
        ).hexdigest()
        return seal

    @property
    def sealed_data(self) -> dict:
        sealed_data = MercanetTransactionRequestSerialier(self).data
        sealed_data["seal"] = self.seal
        sealed_data['sealAlgorithm'] = "HMAC-SHA-256"
        sorted(sealed_data)

        return sealed_data


@dataclass
class MercanetTransctionResponse(MercanetTransactionRequest):
    """
    Réponse automatique de MercaNET
    """

    pass


class Transaction(models.Model):
    order_data = models.TextField(verbose_name="Données de la commande (JSON)")
    mercanet_data = models.TextField(verbose_name="Données de MercaNET (JSON)")

    transaction_reference = models.CharField(
        max_length=35, verbose_name="UUID (Référence MercaNET)"
    )

    amount = models.IntegerField(verbose_name="Montant (centimes)")
