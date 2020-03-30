import requests
from requests.exceptions import HTTPError
class OpenIDClient:
    '''
    implementation of an OIDC Client module in order to provide Client authentication and End-User authentication functionality according to the OpenIDConnect Authentication Code Flow
        Input params:
            <string>issuer
            <string>authType: Bearer(token auth), Basic(client credentials) or None(New auth). It must be set when the user has login parameters.
            <string>method: Shall be GET by default in order to fulfill an authentication
    
    '''
    def __init__(self, issuer = None, scope = 'openid', acces_token = None, response_type=None, client_id=None, client_secret=None, redirect_uri=None, authType = None):
        self._token = {}
        self.scope = []
        self.scope.append(scope)
        self.redirect_uri = redirect_uri
        self._client_id = client_id
        self.response_type = response_type
        self._client_secret = client_secret
        self._code = None
        self._token['token_hint'] = acces_token
        self._method = 'GET'
        self.issuer = issuer
        self.state = None
        self._authType= authType
        if self.issuer:
            self.getEndpointInformation(self.issuer)
    
    def authorized(self):
        '''
        Boolean method that returns true in case the client an authorization token
        '''
        try:
            for k,v in _token:
                a = bool(self._token['token_hint'])
            return bool(self._token)
        except Exception as err:
            return False
            
    def _supportedScopes(self, supportedScopes):
        '''
        Method that returns error in case the scopes provided by the RP doesn't satisfy the host's supported scopes.
        '''
        
        if isinstance(self.scope, str) and 'openid' in self.scope:
            pass
            
        elif 'openid' in self.scope:
            for i in self.scope:
                if i in supportedScopes:
                    continue
                else:
                    self.scope.remove(i)
        else:
            raise Exception('Scope error, could not find the required scopes for OIDC Connect auth')

    def requestAuth(self,  issuer, method='GET',verify = True):
        '''
        The logic implemented on this webpage should retrieve the token from the URL in case the user is not authenticated
        If a token_hint is given the OP should response a succesfully authentication
        '''
        try:
            uri_dict_supported, scope_list_supported = self.getEndpointInformation(issuer, verify)
            if method == 'GET':
                #Retrieve Code or Login
                self.getRequestCode(uri_dict,self.token_hint, verify)
                #Retrieve Token
                self.postRequestToken(uri_dict,self.token_hint, verify)
            elif method == 'POST':
                self.postRequestToken(uri_dict,self.token_hint, verify)
            else:
                raise Exception('The request must have a method defined')
        except Exception as err:
            raise Exception('Other error occurred: '+ str({err}))
            
    def getEndpointInformation(self, sso_node, verify = True):
        '''
        Method that retrieves information from the openid configuration of the host by GET method. It is used to verify the scopes and endpoint inputs
        Input
            <String>sso_node: The domain of the issuer must be given
            <Bool>verify: set as True by default in order to secure the connection against Man in the middle attacks
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
        self._supportedScopes(scope_list)
        return url_dict, scope_list

    def getRequestCode(self, uri_list, token = None, verify=True):
        '''
        Method that retrieves information from the authorization endpoint in order to retrieve the authorization code
        The response of the get request is parsed in order to retrieve the authentication code  
        '''
        try:
            self.getEndpointInformation(self.issuer)
            headers = None
            if token:
                headers = {'authorization': self._authType+str(token)}
                provider_config={"scope": self.scope,"response_type": 'code', "client_id": self.client_id,"redirect_uri": self.redirect_uri,"prompt":'login'}
            else:
                provider_config={"scope": self.scope,"response_type": 'code', "client_id": self.client_id,"redirect_uri": self.redirect_uri}
            

            response=requests.get(uri_list["authorization_endpoint"], data=provider_config, headers = headers, verify=verify)
            response.encoding = 'utf-8'
            #shall be defined a status_code for each response
            self._code = self._retrieveCode(response.content)
        except HTTPError as http_error_msg:
            raise Exception('HTTP error occurred: '+str(response.status_code)+': ' + str({http_error_msg}))
        except Exception as err:
            raise Exception('Other error occurred: '+ str({err}))
        
    def _retrieveCode(self, response):
        '''
        The input parameter content is parsed in order to retrieve and return the authentication code
        '''
        code = response.split('code=')[-1].split('&')
        return code[0]

    def postRequestToken(self,uri_list, token = None, verify=True):
        '''
        Method that retrieves information from the token endpoint in order to retrieve the authorization token 
        '''
        headers = None
        if token:
            headers = {'authorization': self._authType+str(token),'content-type': "application/x-www-form-urlencoded" }
            provider_config={"grant_type": 'client_credentials'}
        else: 
            headers = { 'content-type': "application/x-www-form-urlencoded" }
            provider_config={"grant_type": 'authorization_code', "code": self._code, "redirect_uri": self.redirect_uri, "scope": self.scope, "client_id": self.client_id, "client_secret": self.client_secret}
        
        if self.client_id and self.client_secret:
            try:
                response = requests.post(uri_list["token_endpoint"], data=provider_config, headers=headers, verify = verify)
                response.encoding = 'utf-8'
                #shall be defined a status_code for each response
                #edit token dictionary with the response values
                self._token=self._retrieveToken(response.json().items())
                
            except HTTPError as http_error_msg:
                raise Exception('HTTP error occurred: ' + str({http_error_msg}))
            except Exception as err:
                raise Exception('Other error occurred: '+ str({err}))
            
    def _retrieveToken(self, response):
        '''
        The retrieved token will be set as dictionary where the keys are the token parameters recived in the body

        '''
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
        return tkn

    def validateToken():
        '''
        Method that retrieves information from the authorization endpoint in order to retrieve the authorization code 
        In order to validate the recived token, some steps must be accomplished according to Authentication Flow.
        In the current usage stage there is no need to validate it as it's only needed the acces_token
        '''
        
        pass

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
    
    @property
    def authType(self): 
        return self._authType
         
    @authType.setter 
    def authType(self, a): 
        self._authType = a 
  
    @property
    def method(self): 
        return self._method
         
    @method.setter 
    def method(self, a): 
        self._method = a 