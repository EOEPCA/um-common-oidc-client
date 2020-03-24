import requests
from requests.exceptions import HTTPError
 
class OpenIDClient:
    def __init__(self, scope = None, acces_token = None, response_type=None, client_id=None, redirect_uri=None):
    
        self.token =acces_token
        self.scope = 'openid%20profile%20email'
        self.redirect_uri = redirect_uri
        self._client_id = client_id
        self.response_type = 'code'
        self._client_secret = None
        self._code = None
        self._token = None
        self.method = 'GET'
 
    def authorized(self):
        '''
        Boolean method that returns true in case the client an authorization token
        '''
        return bool(self._token)


    def requestCodeAuth(self, issuer, method):
        '''
        The logic implemented on this webpage should retrieve the token from the URL
        '''
        uri_list = self.getDiscoveryUrl(issuer)
        print(uri_list)
        
        # if method == 'GET':
        #     self.getRequestCode(uri_list)
        # elif method == 'POST':
        #     self.postRequestToken(uri_list,self.code)
        # else:
        #     print(method)

    def getDiscoveryUrl(self, sso_node):
        q = {}
        response=requests.get(str(sso_node)+'/.well_known/openid-configuration', verify = './../mySecureKey.pem')
        response.encoding = 'utf-8'
        print(response.json())
        for k , v in response.json().items():
            q[k]=v

        return q
       

    def getRequestCode(self, uri_list):
        for url in uri_list:
            #/oxauth/restv1/authorize
            provider_config={"authorization_endpoint":"/oxauth/restv1/authorize", "scope": self.scope,"response_type": self.response_type, "client_id": self.client_id,"redirect_uri": 'app://test'}
            try:
                response=requests.get(str(url), provider_config)
                response.encoding = 'utf-8'
                print(response.headers['Content-Type'])
                print('---------------------------------------')
                response.raise_for_status()
            except HTTPError as http_error_msg:
                print('HTTP error occurred: ' + str({http_error_msg}))
            except Exception as err:
                print('Other error occurred: '+ str({err}))
            else:
                print('Success!')


    def postRequestToken(self,uri_list, code):
      
        for url in uri_list:
            provider_config={"token_endpoint":"/oxauth/restv1/token", "grant_type": 'authorization_code', "code": self._code, "redirect_uri": 'app://test', "scope": self.scope}
            if self.client_id and self.client_secret:
                client_config = {"client_id": self.client_id, "client_secret": self.client_secret}
                try:
                    response = requests.post(url, provider_config, client_config)
                    response.encoding = 'utf-8'
                    print(response.text)
                    print(response.json())
                    print('---------------------------------------')
                    print(response.headers['Content-Type'])
                    print('---------------------------------------')
                    response.raise_for_status()
                except HTTPError as http_error_msg:
                    print('HTTP error occurred: ' + str({http_error_msg}))
                except Exception as err:
                    print('Other error occurred: '+ str({err}))
                else:
                    print('Success!')
        

    def testLib(self):
        print('Lets do some requests')

    @property
    def client_id(self): 
        return self._client_id

    @client_id.setter 
    def client_id(self, a): 
        self._client_id = a 
  
    @property
    def client_secret(self): 
        return self._client_secret

    @client_secret.setter 
    def client_secret(self, a): 
        self._client_secret = a 
  
    @property
    def code(self): 
        return self._code
         
    @code.setter 
    def code(self, a): 
        self._code = a 
  