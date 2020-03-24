import requests
from requests.exceptions import HTTPError

class OpenIDClient:
    def __init__(self, scope = None, acces_token = None, response_type=None, client_id=None, redirect_uri=None):
    
        self.token =acces_token
        self.scope = scope
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
        try:
            uri_dict, scope_list = self.getDiscoveryUrl(issuer)

            if method == 'GET':
                self.getRequestCode(uri_dict)
            elif method == 'POST':
                self.postRequestToken(uri_dict,self.code)
            else:
                print(method)
        except Exception as err:
            print('Other error occurred: '+ str({err}))
        else:
            print('Success!')
            
    def getDiscoveryUrl(self, sso_node):
        q = {}
        response=requests.get(str(sso_node)+'/.well_known/openid-configuration')
        response.encoding = 'utf-8'
        scope_list=[]
        url_list=[]
        
        for k , v in response.json().items():
            if "scopes_supported" in k:
                scope_list=v
            elif "endpoint" in k:
                q[k]=v
            else:
                continue
        return q, scope_list

    def getRequestCode(self, uri_list):
        provider_config={"scope": self.scope,"response_type": self.response_type, "client_id": self.client_id,"redirect_uri": self.redirect_uri}
        try:
            response=requests.get(uri_list["authorization_endpoint"], provider_config)
            response.encoding = 'utf-8'
            response.raise_for_status()
            self._code = self.retrieveCode(response.text())
        except HTTPError as http_error_msg:
            print('HTTP error occurred: ' + str({http_error_msg}))
        except Exception as err:
            print('Other error occurred: '+ str({err}))
        else:
            print('Success!')

    def retrieveCode(response):
        code = response.split('code=')[-1].split('&')
        return code[0]

    def retrieveCodeResponse(self, response):
        code = response.split('code=')[-1]
        print(code)

    def postRequestToken(self,uri_list, code):
     
        provider_config={"grant_type": 'authorization_code', "code": self._code, "redirect_uri": self.redirect_uri, "scope": self.scope}
        if self.client_id and self.client_secret:
            client_config = {"client_id": self.client_id, "client_secret": self.client_secret}
            try:
                response = requests.post(uri_list["token_endpoint"], provider_config, client_config)
                response.encoding = 'utf-8'
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
  