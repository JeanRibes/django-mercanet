import hashlib
from datetime import datetime

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


def genId(id):
    return (
        (datetime.now().strftime("%Y%m%d%H")
         + hashlib.sha1(bytearray(id.encode("UTF-8"))).hexdigest())[:34]
    )
