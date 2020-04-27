# Create your tests here.
from unittest import TestCase

from mercanet.utils import seal_hmac_sha256_from_string, fromVomi, compute_seal


class SealTest(TestCase):
    def setUp(self):
        self.secret_key = "S9i8qClCnb2CZU3y3Vn0toIOgz3z_aBi79akR30vM9o"

    def tearDown(self) -> None:
        return super().tearDown()

    def test_hmac_string(self):
        """
        test du Seal dans le cadre de la réponse automatique
        """
        reponse_auto_data = "captureDay=0|captureMode=AUTHOR_CAPTURE|currencyCode=978|merchantId=211000021310001|orderChannel=INTERNET|responseCode=00|transactionDateTime=2020-04-27T13:52:04+02:00|transactionReference=2020042711d321d6f7ccf98b51540ec9d9|keyVersion=1|acquirerResponseCode=00|amount=100|authorisationId=121538|guaranteeIndicator=N|panExpiryDate=202101|paymentMeanBrand=VISA|paymentMeanType=CARD|complementaryCode=00|complementaryInfo=<RULE_RESULT CR=0 />,CARD_COUNTRY=FRA,<CARD_INFOS BDOM=LA BANQUE POSTALE COUNTRY=FRA PRODUCTCODE=F NETWORK=VISA BANKCODE=20041 PRODUCTNAME=VISA CLASSIC PRODUCTPROFILE=D />|customerIpAddress=81.67.170.120|maskedPan=5017##########01|orderId=2038|returnContext=test hé salut|scoreProfile=profil1|holderAuthentRelegation=N|holderAuthentStatus=NOT_ENROLLED|transactionOrigin=INTERNET|paymentPattern=ONE_SHOT|customerMobilePhone=null|mandateAuthentMethod=null|mandateUsage=null|transactionActors=null|mandateId=null|captureLimitDate=20200427|dccStatus=null|dccResponseCode=null|dccAmount=null|dccCurrencyCode=null|dccExchangeRate=null|dccExchangeRateValidity=null|dccProvider=null|statementReference=null|panEntryMode=MANUAL|walletType=null|holderAuthentMethod=NOT_SPECIFIED|holderAuthentProgram=3DS|paymentMeanId=null|instalmentNumber=null|instalmentDatesList=null|instalmentTransactionReferencesList=null|instalmentAmountsList=null|settlementMode=null|mandateCertificationType=null|valueDate=null|creditorId=null|acquirerResponseIdentifier=null|acquirerResponseMessage=null|paymentMeanTradingName=null|additionalAuthorisationNumber=null|issuerWalletInformation=null|s10TransactionId=273|s10TransactionIdDate=20200427|preAuthenticationColor=null|preAuthenticationInfo=null|preAuthenticationProfile=null|preAuthenticationThreshold=null|preAuthenticationValue=null|invoiceReference=null|s10transactionIdsList=null|cardProductCode=F|cardProductName=VISA CLASSIC|cardProductProfile=D|issuerCode=20041|issuerCountryCode=FRA|acquirerNativeResponseCode=00|settlementModeComplement=null|preAuthorisationProfile=null|preAuthorisationProfileValue=null|preAuthorisationRuleResultList=null|preAuthenticationProfileValue=null|preAuthenticationRuleResultList=null|paymentMeanBrandSelectionStatus=NOT_APPLICABLE|transactionPlatform=PROD|avsAddressResponseCode=null|avsPostcodeResponseCode=null|customerCompanyName=null|customerBusinessName=null|customerLegalId=null|customerPositionOccupied=null|paymentAttemptNumber=1|holderContactEmail=null"
        reponse_auto_seal = (
            "9001fa316e8afa4d0ea9dd7b1c790cb090d23a879736639896cb39d142d26d3a"
        )
        self.assertEqual(
            seal_hmac_sha256_from_string(reponse_auto_data, self.secret_key),
            reponse_auto_seal,
        )

    def test_seal_requete(self):
        data = {
            "amount": "2500",
            "automaticResponseUrl": "https://automatic-response-url.fr/",
            "normalReturnUrl": "https://normal-return-url/",
            "captureDay": "0",
            "captureMode": "AUTHOR_CAPTURE",
            "currencyCode": "978",
            "interfaceVersion": "IR_WS_2.22",
            "keyVersion": "1",
            "merchantId": "011223344550000",
            "orderChannel": "INTERNET",
            "orderId": "ORD101",
            "returnContext": "ReturnContext",
            "transactionOrigin": "SO_WEBAPPLI",
            "transactionReference": "TREFEXA2012",
        }  # données de SIPS Worldline

        self.assertEqual(compute_seal(data, 'secret123'),
                         'e4d75c6a779adee5850192d1ecc162ca0c85e960cb00d9923879609f89739152')

    def test_mercanet_reponse_auto_deserialize(self):
        reponse_auto_data = "captureDay=0|captureMode=AUTHOR_CAPTURE|currencyCode=978|merchantId=211000021310001|orderChannel=INTERNET|responseCode=00|transactionDateTime=2020-04-27T13:52:04+02:00|transactionReference=2020042711d321d6f7ccf98b51540ec9d9|keyVersion=1|acquirerResponseCode=00|amount=100|authorisationId=121538|guaranteeIndicator=N|panExpiryDate=202101|paymentMeanBrand=VISA|paymentMeanType=CARD|complementaryCode=00|complementaryInfo=<RULE_RESULT CR=0 />,CARD_COUNTRY=FRA,<CARD_INFOS BDOM=LA BANQUE POSTALE COUNTRY=FRA PRODUCTCODE=F NETWORK=VISA BANKCODE=20041 PRODUCTNAME=VISA CLASSIC PRODUCTPROFILE=D />|customerIpAddress=81.67.170.120|maskedPan=5017##########01|orderId=2038|returnContext=test hé salut|scoreProfile=profil1|holderAuthentRelegation=N|holderAuthentStatus=NOT_ENROLLED|transactionOrigin=INTERNET|paymentPattern=ONE_SHOT|customerMobilePhone=null|mandateAuthentMethod=null|mandateUsage=null|transactionActors=null|mandateId=null|captureLimitDate=20200427|dccStatus=null|dccResponseCode=null|dccAmount=null|dccCurrencyCode=null|dccExchangeRate=null|dccExchangeRateValidity=null|dccProvider=null|statementReference=null|panEntryMode=MANUAL|walletType=null|holderAuthentMethod=NOT_SPECIFIED|holderAuthentProgram=3DS|paymentMeanId=null|instalmentNumber=null|instalmentDatesList=null|instalmentTransactionReferencesList=null|instalmentAmountsList=null|settlementMode=null|mandateCertificationType=null|valueDate=null|creditorId=null|acquirerResponseIdentifier=null|acquirerResponseMessage=null|paymentMeanTradingName=null|additionalAuthorisationNumber=null|issuerWalletInformation=null|s10TransactionId=273|s10TransactionIdDate=20200427|preAuthenticationColor=null|preAuthenticationInfo=null|preAuthenticationProfile=null|preAuthenticationThreshold=null|preAuthenticationValue=null|invoiceReference=null|s10transactionIdsList=null|cardProductCode=F|cardProductName=VISA CLASSIC|cardProductProfile=D|issuerCode=20041|issuerCountryCode=FRA|acquirerNativeResponseCode=00|settlementModeComplement=null|preAuthorisationProfile=null|preAuthorisationProfileValue=null|preAuthorisationRuleResultList=null|preAuthenticationProfileValue=null|preAuthenticationRuleResultList=null|paymentMeanBrandSelectionStatus=NOT_APPLICABLE|transactionPlatform=PROD|avsAddressResponseCode=null|avsPostcodeResponseCode=null|customerCompanyName=null|customerBusinessName=null|customerLegalId=null|customerPositionOccupied=null|paymentAttemptNumber=1|holderContactEmail=null"

        sortie_voulue = {'captureDay': '0', 'captureMode': 'AUTHOR_CAPTURE', 'currencyCode': '978',
                         'merchantId': '211000021310001', 'orderChannel': 'INTERNET', 'responseCode': '00',
                         'transactionDateTime': '2020-04-27T13:52:04+02:00',
                         'transactionReference': '2020042711d321d6f7ccf98b51540ec9d9', 'keyVersion': '1',
                         'acquirerResponseCode': '00', 'amount': '100', 'authorisationId': '121538',
                         'guaranteeIndicator': 'N', 'panExpiryDate': '202101', 'paymentMeanBrand': 'VISA',
                         'paymentMeanType': 'CARD', 'complementaryCode': '00',
                         'complementaryInfo': ['<RULE_RESULT CR', '0 />,CARD_COUNTRY', 'FRA,<CARD_INFOS BDOM',
                                               'LA BANQUE POSTALE COUNTRY', 'FRA PRODUCTCODE', 'F NETWORK',
                                               'VISA BANKCODE', '20041 PRODUCTNAME', 'VISA CLASSIC PRODUCTPROFILE',
                                               'D />'], 'customerIpAddress': '81.67.170.120',
                         'maskedPan': '5017##########01', 'orderId': '2038', 'returnContext': 'test hé salut',
                         'scoreProfile': 'profil1', 'holderAuthentRelegation': 'N',
                         'holderAuthentStatus': 'NOT_ENROLLED', 'transactionOrigin': 'INTERNET',
                         'paymentPattern': 'ONE_SHOT', 'customerMobilePhone': 'null', 'mandateAuthentMethod': 'null',
                         'mandateUsage': 'null', 'transactionActors': 'null', 'mandateId': 'null',
                         'captureLimitDate': '20200427', 'dccStatus': 'null', 'dccResponseCode': 'null',
                         'dccAmount': 'null', 'dccCurrencyCode': 'null', 'dccExchangeRate': 'null',
                         'dccExchangeRateValidity': 'null', 'dccProvider': 'null', 'statementReference': 'null',
                         'panEntryMode': 'MANUAL', 'walletType': 'null', 'holderAuthentMethod': 'NOT_SPECIFIED',
                         'holderAuthentProgram': '3DS', 'paymentMeanId': 'null', 'instalmentNumber': 'null',
                         'instalmentDatesList': 'null', 'instalmentTransactionReferencesList': 'null',
                         'instalmentAmountsList': 'null', 'settlementMode': 'null', 'mandateCertificationType': 'null',
                         'valueDate': 'null', 'creditorId': 'null', 'acquirerResponseIdentifier': 'null',
                         'acquirerResponseMessage': 'null', 'paymentMeanTradingName': 'null',
                         'additionalAuthorisationNumber': 'null', 'issuerWalletInformation': 'null',
                         's10TransactionId': '273', 's10TransactionIdDate': '20200427',
                         'preAuthenticationColor': 'null', 'preAuthenticationInfo': 'null',
                         'preAuthenticationProfile': 'null', 'preAuthenticationThreshold': 'null',
                         'preAuthenticationValue': 'null', 'invoiceReference': 'null', 's10transactionIdsList': 'null',
                         'cardProductCode': 'F', 'cardProductName': 'VISA CLASSIC', 'cardProductProfile': 'D',
                         'issuerCode': '20041', 'issuerCountryCode': 'FRA', 'acquirerNativeResponseCode': '00',
                         'settlementModeComplement': 'null', 'preAuthorisationProfile': 'null',
                         'preAuthorisationProfileValue': 'null', 'preAuthorisationRuleResultList': 'null',
                         'preAuthenticationProfileValue': 'null', 'preAuthenticationRuleResultList': 'null',
                         'paymentMeanBrandSelectionStatus': 'NOT_APPLICABLE', 'transactionPlatform': 'PROD',
                         'avsAddressResponseCode': 'null', 'avsPostcodeResponseCode': 'null',
                         'customerCompanyName': 'null', 'customerBusinessName': 'null', 'customerLegalId': 'null',
                         'customerPositionOccupied': 'null', 'paymentAttemptNumber': '1', 'holderContactEmail': 'null'}
        self.assertDictEqual(
            fromVomi(reponse_auto_data),
            sortie_voulue
        )
