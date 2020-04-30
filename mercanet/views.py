# Create your views here.
import logging
import random

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from mercanet.models import TransactionMercanet
from mercanet.serializers import TransactionMercanetSerializer, seal_transaction
from mercanet.utils import genId, fromVomi, seal_hmac_sha256_from_string, responseCodes

logger = logging.getLogger('mercanet')

def mercanet_request(request):
    """
    Fonction qui va envoyer le client vers MercaNET
    """
    mrd = TransactionMercanet(
        amount=1000,
        transactionReference=genId(str(random.randint(1, 99))),
        normalReturnUrl="https://perdu.com/",
        returnContext="test hé salut",
        orderId=2038,
    )
    mrd.save()

    request_data = seal_transaction(mrd)
    # 858005903b91ae3b3a076e29aca7dc6314c05aa6f929c439ecfce1de17ea7e39
    # 20200427088de23aaaec61b2cba81bd155e
    print(request_data)

    mercanet_response = requests.post(settings.MERCANET["URL"], json=request_data)
    print("response", str(mercanet_response.content))
    print("json", str(mercanet_response.json()))

    mercanet_response_data = mercanet_response.json()

    print(responseCodes[mercanet_response_data['redirectionStatusCode']])

    return render(
        request,
        template_name="mercanet_redirect.html",
        context={
            "redirectionUrl": mercanet_response_data["redirectionUrl"],
            "interfaceVersion": mrd.interfaceVersion,
            "redirectionData": mercanet_response_data["redirectionData"],
        },
    )


@csrf_exempt
def mercanet_response(request):
    """
    Appelée par MercaNET lui-même lors de la réponse automatique
    """
    data = request.POST["Data"]
    propre = fromVomi(data)
    seal = request.POST["Seal"]

    logger.info(f"Receiving autoMercanet with seal {seal} : {propre} (from {data})")

    recalc_seal = seal_hmac_sha256_from_string(
        data, secret=settings.MERCANET["SECRET_KEY"]
    )  # on met non pas une concaténation des champs mais les données brutes (et moches) de mercanet
    if seal != recalc_seal:
        logger.warning("Seal error ! Bank servers may be under attack or we have a bad key")
        return HttpResponse()
    serializer = TransactionMercanetSerializer(data=propre)

    if serializer.is_valid():
        transaction_reference = serializer.validated_data['transactionReference']
        transaction = TransactionMercanet.objects.get(transactionReference=transaction_reference)
        if not settings.DEBUG and transaction.terminated:  # on n'enregistre pas une 2e fois la transaction
            return HttpResponse("vous avez répondu une 2e fois !")  # c'est arrivé une fois que mercanet réponde 2 fois
        serializer.update(transaction, serializer.validated_data)


    else:
        print(f" erreurs: {serializer.errors}")
        pass  # log ser

    recalc_seal = seal_hmac_sha256_from_string(
        data, secret=settings.MERCANET["SECRET_KEY"]
    )  # on met non pas une concaténation des champs mais les données brutes (et moches) de mercanet
    print(f"secure: {recalc_seal == seal}")

    print(f"id:{propre['orderId']} {propre['returnContext']}")
    return HttpResponse('merci et à bientôt')
