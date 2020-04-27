from dataclasses import dataclass
from django.conf import settings
from django.db import models

# Create your models here.
from mercanet.serializers import MercanetTransactionRequestSerialier
from mercanet.utils import compute_seal, seal_hmac_sha256_from_string

secret = settings.MERCANET["SECRET_KEY"]


@dataclass
class BaseTransactionMercanet:
    transactionReference: str
    amount: int
    normalReturnUrl: str
    orderId: int
    returnContext: str


class MercanetTransactionRequest(BaseTransactionMercanet):
    """
    Objet représentant ce qui est envoyé à MercaNET
    """

    # billingContact 	email, firstname, gender, lastname, mobile, phone, title, (à rajouter ?)

    merchantId: str = settings.MERCANET["MERCHANT_ID"]
    automaticResponseUrl: str = settings.MERCANET["REPONSE_AUTO_URL"]
    orderChannel: str = "INTERNET"
    currencyCode: str = "978"
    interfaceVersion: str = settings.MERCANET["INTERFACE_VERSION"]
    keyVersion: int = 1

    @property
    def seal(self) -> str:
        json_data = MercanetTransactionRequestSerialier(self).data
        return compute_seal(json_data, secret, seal_hmac_sha256_from_string)
        # return seal_sha256_from_dict(json_data, secret)

    @property
    def sealed_data(self) -> dict:
        sealed_data = MercanetTransactionRequestSerialier(self).data
        sealed_data["seal"] = self.seal
        sealed_data["sealAlgorithm"] = "HMAC-SHA-256"  # ça marche si je mets rien
        # sealed_data['sealAlgorithm'] = "SHA-256"
        sorted(sealed_data)

        return sealed_data


@dataclass
class MercanetTransactionResponse(MercanetTransactionRequest):
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
