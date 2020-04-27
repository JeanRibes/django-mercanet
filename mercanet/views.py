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
from mercanet.utils import genId


def mercanet_request(request):
    """
    Fonction qui va envoyer le client vers MercaNET
    """
    mrd = MercanetTransactionRequest(amount=100, transactionReference=genId(str(random.randint(1, 99))),
                                     normalReturnUrl="https://perdu.com/")  # request.build_absolute_uri(reverse("auto"))

    request_data = OrderedDict(mrd.sealed_data)
    print(request_data)
    print(json.dumps(request_data))
    # 858005903b91ae3b3a076e29aca7dc6314c05aa6f929c439ecfce1de17ea7e39
    # 20200427088de23aaaec61b2cba81bd155e
    mercanet_response = requests.post(settings.MERCANET['URL'], json=request_data)
    print('response', str(mercanet_response.content))
    print('json', str(mercanet_response.json()))

    mercanet_response_data = mercanet_response.json()

    return render(request, template_name="mercanet_redirect.html", context={
        'redirectionUrl': mercanet_response_data['redirectionUrl'],
        'interfaceVersion': mrd.interfaceVersion,
        'redirectionData': mercanet_response_data['redirectionData']
    })


@csrf_exempt
def mercanet_response(request):
    """
    Appelée par MercaNET lui-même lors de la réponse automatique
    """
    print(request.body)
    return HttpResponse()
