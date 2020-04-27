# Create your views here.
import json
import random
from collections import OrderedDict

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from mercanet.models import MercanetTransactionRequest
from mercanet.serializers import MercanetTransactionResponseSerializer
from mercanet.utils import genId, fromVomi, seal_hmac_sha256_from_string


def mercanet_request(request):
    """
    Fonction qui va envoyer le client vers MercaNET
    """
    mrd = MercanetTransactionRequest(
        amount=100,
        transactionReference=genId(str(random.randint(1, 99))),
        normalReturnUrl="https://perdu.com/",
        returnContext="test hé salut",
        orderId=2038,
    )  # request.build_absolute_uri(reverse("auto"))

    request_data = OrderedDict(mrd.sealed_data)
    print(request_data)
    print(json.dumps(request_data))
    print()
    # 858005903b91ae3b3a076e29aca7dc6314c05aa6f929c439ecfce1de17ea7e39
    # 20200427088de23aaaec61b2cba81bd155e
    mercanet_response = requests.post(settings.MERCANET["URL"], json=request_data)
    print("response", str(mercanet_response.content))
    print("json", str(mercanet_response.json()))

    mercanet_response_data = mercanet_response.json()

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
    serializer = MercanetTransactionResponseSerializer(data=propre)
    print(data)
    print(propre)
    serializer.is_valid()
    print(serializer.validated_data)

    recalc_seal = seal_hmac_sha256_from_string(
        data, secret=settings.MERCANET["SECRET_KEY"]
    )  # on met non pas une concaténation des champs mais les données brutes (et moches) de mercanet
    print(f"secure: {recalc_seal == seal}")

    print(f"id:{propre['orderId']} {propre['returnContext']}")
    return HttpResponse()
