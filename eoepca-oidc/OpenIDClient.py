import requests
from requests.exceptions import HTTPError
class OpenIDClient:
    def __init__(self, issuer = None, scope = None, acces_token = None, response_type=None, client_id=None, redirect_uri=None):
        self._token={}
        self.scope = scope
        self.redirect_uri = redirect_uri
        self._client_id = client_id
        self.response_type = 'code'
        self._client_secret = None
        self._code = None
        self._token['token_hint'] = acces_token
        self.method = 'GET'
        self.issuer = issuer
        self.state = None
    
    def authorized(self):
        '''
        Boolean method that returns true in case the client an authorization token
        '''
        try:
                
            for k,v in _token:
                print(bool(v))
            a = bool(self._token['token_hint'])
            print (self._token)
            
            print(bool(self._token))
            return bool(self._token)
        except Exception as err:
            return False
            
    def supportedScopes(self, supportedScopes):
        '''
        Method that returns error in case the scopes provided by the RP doesn't satisfy the host's supported scopes.
        '''
        if 'openid' in self.scopes and 'ogc_user' in self.scopes:
            for i in self.scope:
                if i in supportedScopes:
                    continue
                else:
                    self.scope.remove(i)
        else:
            raise Exception('Scope error, could not find the required scopes for OIDC Connect auth')

    def requestAuth(self, method, issuer, token = None, verify = True):
        '''
        The logic implemented on this webpage should retrieve the token from the URL
        '''
        try:
            uri_dict_supported, scope_list_supported = self.getDiscoveryUrl(issuer, verify)

            if method == 'GET':
                return self.getRequestCode(uri_dict,self.token_hint,verify)
            elif method == 'POST':
                return self.postRequestToken(uri_dict)
            else:
                raise Exception('The request must have a method defined')
        except Exception as err:
            raise Exception('Other error occurred: '+ str({err}))
            
    def getDiscoveryUrl(self, sso_node, verify = True):
        '''
        Method that retrieves information from the openid configuration of the host by GET method. It is used to verify the scopes and endpoint inputs
        Returns 
            <List>scope_list: List of all supported scopes by the host
            <Dict>url_dict: Dictionary with all host endpoints 
        '''
        url_dict = {}
        response=requests.get(str(sso_node)+'/.well_known/openid-configuration',verify = verify)
        response.encoding = 'utf-8'
        scope_list=[]
        url_list=[]
        
        for k , v in response.json().items():
            if "scopes_supported" in k:
                scope_list=v
            elif "endpoint" in k[-8:]:
                url_dict[k]=v
            elif "issuer" in k:
                url_dict[k]=v
            else:
                continue
        return url_dict, scope_list

    def getRequestCode(self, uri_list, token = False, verify=True):
        '''
        Method that retrieves information from the authorization endpoint in order to retrieve the authorization code   
        '''
        header = None
        if token:
            header = {'authorization': "Basic "+str(token)}
        provider_config={"scope": self.scope,"response_type": 'code', "client_id": self.client_id,"redirect_uri": self.redirect_uri}
        try:
            response=requests.get(uri_list["authorization_endpoint"], data=provider_config, header = header, verify=verify)
            response.encoding = 'utf-8'
            self._code = self.retrieveCode(response.json())
        except HTTPError as http_error_msg:
            raise Exception('HTTP error occurred: '+str(response.status_code)+': ' + str({http_error_msg}))
        except Exception as err:
            raise Exception('Other error occurred: '+ str({err}))
        
    def retrieveCode(self, response):
        code = response.split('code=')[-1].split('&')
        return code[0]

    def postRequestToken(self,uri_list):
        '''
        Method that retrieves information from the token endpoint in order to retrieve the authorization token 
        '''
        provider_config={"grant_type": 'authorization_code', "code": self._code, "redirect_uri": self.redirect_uri, "scope": self.scope, "client_id": self.client_id, "client_secret": self.client_secret}
        headers = { 'content-type': "application/x-www-form-urlencoded" }
        if self.client_id and self.client_secret:
            try:
                response = requests.post(uri_list["token_endpoint"], data=provider_config, headers=headers)
                response.encoding = 'utf-8'
                self.retrieveToken(response.json().items())
                response.raise_for_status()
            except HTTPError as http_error_msg:
                raise Exception('HTTP error occurred: ' + str({http_error_msg}))
            except Exception as err:
                raise Exception('Other error occurred: '+ str({err}))
            
    def retrieveToken(self, response):
        tkn = {}
        for k , v in response:
            if "access_token" in k:
                tkn[k]=v
            elif "token_type" in k:
                tkn[k]=v
            elif "refresh_token" in k:
                tkn[k]=v
            elif "id_token" in k:
                tkn[k]=v
            elif "expires_in" in k:
                tkn[k]=v
            else:
                continue
        self._token=tkn
  

    # def connectWithApi(self, url_dict):
    #     if self.authorized:
    #         headers = {'content-type': "application/x-www-form-urlencoded",'authorization': "Bearer "+ self._token}
    #         try:
    #             response = requests.get(uri_dict["issuer"], headers=headers)
    #             response.encoding = 'utf-8'
    #             token = {}
    #             self.retrieveToken(response.json().items())
    #             response.raise_for_status()
    #         except HTTPError as http_error_msg:
    #             print('HTTP error occurred: ' + str({http_error_msg}))
    #         except Exception as err:
    #             print('Other error occurred: '+ str({err}))
    #         else:
    #             print('Success!')
    #     else:
    #         print('Not authorized with token')
    #         pass

    def validateToken():
        '''
        Method that retrieves information from the authorization endpoint in order to retrieve the authorization code 
        '''
        pass
        
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

    @property
    def token(self): 
        return self._token
         
    @token.setter 
    def token(self, a): 
        self._token = a 
  