import hashlib
import hmac
from datetime import datetime
from typing import Callable

responseCodes = {
    "00": "Transaction acceptée",
    "02": "Demande d’autorisation par téléphone à la banque à cause d’un dépassement du plafond d’autorisation sur la carte, si vous êtes autorisé à forcer les transactions",
    "03": "Contrat commerçant invalide",
    "05": "Refus 3DSecure",
    "11": "Utilisé dans le cas d'un contrôle différé. Le PAN est en opposition",
    "12": "Transaction invalide, vérifier les paramètres transférés dans la requête",
    "14": "Coordonnées du moyen de paiement invalides (ex: n° de carte ou cryptogramme visuel de la carte) ou vérification AVS échouée",
    "17": "Annulation de l’acheteur",
    "30": "Erreur de format",
    "34": "Suspicion de fraude (seal erroné)",
    "54": "Date de validité du moyen de paiement dépassée",
    "75": "Nombre de tentatives de saisie des coordonnées du moyen de paiement sous Sips Paypage dépassé",
    "90": "Service temporairement indisponible",
    "94": "Transaction dupliquée : le transactionReference de la transaction est déjà utilisé",
    "97": "Délai expiré, transaction refusée",
    "99": "Problème temporaire du serveur de paiement.",
}


def genId(id: str) -> str:
    """
    Génère le transactionReference à partir de la date et d'un id
    :param id: l'id de la transaction en base de donnée
    :return:
    """
    return (
                   datetime.now().strftime("%Y%m%d%H")
                   + hashlib.sha1(bytearray(id.encode("UTF-8"))).hexdigest()
           )[
           :34
           ]  # limite = 35


def seal_hmac_sha256_from_string(string_data: str, secret: str) -> str:
    return hmac.new(
        key=bytearray(secret.encode("utf-8")),
        msg=bytearray(string_data.encode("utf-8")),
        digestmod=hashlib.sha256,
    ).hexdigest()


def seal_sha256_from_string(string: str, secret: str) -> str:
    raise DeprecationWarning("Cette fonction est encore moins sécurisée !")
    # content = string + secret
    # return hashlib.sha256(content.encode("utf-8")).hexdigest()


def compute_seal(
        dict_data: dict,
        secret: str,
        crypto_func: Callable[[str, str], str] = seal_hmac_sha256_from_string,
) -> str:
    dict_data.pop("keyVersion", None)
    dict_data.pop("seal", None)
    dict_data.pop("sealAlgorithm", None)
    sorted(dict_data)  # les clés doivent être en ordre alphabétique

    str_concat = ""
    for key in sorted(dict_data.keys()):
        if dict_data[key] == "null":
            continue
        str_concat += str(dict_data[key])
    # print(f"str concat go brr {str_concat}")
    return crypto_func(str_concat, secret)


def fromVomi(source: str) -> dict:
    ret = {}
    for elem in source.split("|"):
        try:
            key, value = elem.split("=")
            ret[key] = value
        except ValueError:
            key, *value = elem.split("=")
            # * car il peut y avoir plusieurs '=' dans le cas du XML nested chelou
            ret[key] = value
        except:
            continue
    return ret
