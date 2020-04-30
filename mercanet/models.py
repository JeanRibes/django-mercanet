from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

secret = settings.MERCANET["SECRET_KEY"]
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$',
                              'Only alphanumeric characters are allowed.')  # merci @martijns-peter https://stackoverflow.com/a/17165415/12643213


class TransactionMercanet(models.Model):
    """
    Représente une transaction 'immutable'
    Comme les références de transaction sont uniques, une transaction ne peut être 'rejouée', il faut donc
    en créer une nouvelle si celle-ci échoue

    les noms des champs ne sont pas en snake_case pour faciliter la correspondance avec l'API Mercanet
    """

    class Meta:
        verbose_name = "Transaction MercaNET"
        verbose_name_plural = "Transactions MercaNET"

    transactionReference = models.CharField(
        unique=True,
        max_length=35,
        validators=[alphanumeric])  # format : AN35 -> alphanumérique
    amount = models.IntegerField(verbose_name="Montant (centimes)")
    orderId = models.IntegerField(verbose_name="ID de l'adhésion")  # MercaNET le passe sans modifications
    returnContext = models.CharField(
        verbose_name="Données de contexte adhésion",
        max_length=255,
    )  # MercaNET le passe sans modifications
    normalReturnUrl = models.URLField(verbose_name="URL de retour client", max_length=1023)  # on peut le faire varier

    # ces champs suivants sont remplis par la réponse auto MercaNET
    transactionDateTime = models.DateTimeField(null=True, verbose_name="Date du paiement")
    responseCode = models.CharField(null=True, verbose_name="Code de réponse", max_length=3)  # "00"->good

    def to_mercanet_request(self):
        self.merchantId: str = settings.MERCANET["MERCHANT_ID"]
        self.automaticResponseUrl: str = settings.MERCANET["REPONSE_AUTO_URL"]
        self.orderChannel: str = "INTERNET"
        self.currencyCode: str = "978"  # code pour euros (€)
        self.interfaceVersion: str = settings.MERCANET["INTERFACE_VERSION"]
        self.keyVersion: int = settings.MERCANET['KEY_VERSION']
        del self.responseCode  # on les enlève car Mecanet n'en veut pas à l'émission
        del self.transactionDateTime
        del self.id
        return self

    def __str__(self):
        return f"Transaction #{self.id or 0} commande #{self.orderId} de {self.amount / 100.0} €"

    @property
    def payed(self):
        return self.responseCode == "00"

    @property
    def terminated(self):
        return self.responseCode is not None and self.responseCode != ""
