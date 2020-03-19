import requests

class OpenIDClient:
    def __init__(self,method='GET', scope = None, acces_token = None, response_type=None, client_id=None, redirect_uri=None):
        #param client_id: Client id obtained during registration
        #param token: Token dictionary, must include access_token
        client_id = '6779ef20e75817b79602'; #GitHub ClientID
        response_type = 'code'
    def testLib(self):
        print('Lets do some requests')

