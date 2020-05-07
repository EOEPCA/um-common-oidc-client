#!/usr/bin/env python3
import requests
import json
from requests.exceptions import HTTPError
import unittest
import mock
from eoepca_oidc import OpenIDClient

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, content ,json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.content = content

        def json(self):
            return self.json_data
        def content(self):
            return self.content
    obj = {"access_token": "SlAV32hkKG", "token_type": "Bearer", "refresh_token": "8xLOxBtZp8", "expires_in": 3600, "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjFlOWdkazcifQ.ewogImlzcyI6ICJodHRwOi8vc2VydmVyLmV4YW1wbGUuY29tIiwKICJzdWIiOiAiMjQ4Mjg5NzYxMDAxIiwKICJhdWQiOiAiczZCaGRSa3F0MyIsCiAibm9uY2UiOiAibi0wUzZfV3pBMk1qIiwKICJleHAiOiAxMzExMjgxOTcwLAogImlhdCI6IDEzMTEyODA5NzAKfQ.ggW8hZ1EuVLuxNuuIJKX_V8a_OMXzR0EHR9R6jgdqrOOF4daGU96Sr_P6qJp6IcmD3HP99Obi1PRs-cwh3LO-p146waJ8IhehcwL7F09JdijmBqkvPeB2T9CJNqeGpe-gccMg4vfKjkM8FcGvnzZUN4_KSP0aAp1tOJ1zZwgjxqGByKHiOtX7TpdQyHE5lcMiKPXfEIQILVq0pc_E2DzL7emopWoaoZTF_m0_N0YzFC6g6EJbOEoRoSK5hoDalrcvRYLSrQAZZKflyuVCyixEoV9GfNQC3_osjzw2PAithfubEEBLuVVk4XUVrWOLrLl0nx7RkKU8NXNHq-rvKMzqg"}
    obj2={"access_token":"2YotnFZFEjr1zCsicMWpAA","token_type":"example","expires_in":3600,"example_parameter":"example_value"}
    if 'application/x-www-form-urlencoded' in list(kwargs.get('headers').items())[0] and 'code' in kwargs.get('data') and 'client_id' in kwargs.get('data') and 'client_secret' in kwargs.get('data') and 'redirect_uri' in kwargs.get('data'):
        return MockResponse('HTTP/1.1 200 OK Content-Type: application/json Cache-Control: no-store Pragma: no-cache ',obj, 200)
    elif ('authorization' in list(kwargs.get('headers').items())[1] or'authorization' in list(kwargs.get('headers').items())[0])  and 'client_credentials' in list(kwargs.get('data').items())[0]:
        return MockResponse('HTTP/1.1 200 OK Content-Type: application/json;charset=UTF-8 Cache-Control: no-store Pragma: no-cache ',obj2, 200)
    return MockResponse(None, None, 404)

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, content ,json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.content = content

        def json(self):
            return self.json_data
        def content(self):
            return self.content

    with open('tests/tst.json', 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data)
    
    # add json data if provided
    if '/.well_known/openid-configuration' in args[0]:
        return MockResponse(None,obj, 200)
    elif kwargs.get('headers') and 'scope' in kwargs.get('data') and 'response_type' in kwargs.get('data') and 'client_id' in kwargs.get('data') and 'redirect_uri' in kwargs.get('data'):
        return MockResponse('HTTP/1.1 302 Found Location: https://client.example.org/cb?code=SplxlOBeZQQYbYS6WxSbIA&state=af09ure9urf',None, 200)
    elif not kwargs.get('headers') and 'scope' in kwargs.get('data') and 'response_type' in kwargs.get('data') and 'client_id' in kwargs.get('data') and 'redirect_uri' in kwargs.get('data'):
        return MockResponse('HTTP/1.1 302 Found Location: https://client.example.org/cb?code=AIIEHGSKIUOIFNKLOSIUOI&state=af09ure9urf',None, 200)
    return MockResponse(None, 404)



class OIDC_Unit_Test(unittest.TestCase):
    

    # First, mock has to simulate http response, therefore a patch of get and post methods from requests library will be needed.
    
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_code_auth(self, mock_get,raise_for_status=None):
        mock_resp = mock.Mock()
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        oidc = OpenIDClient()
        oidc.scope = 'openid'
        url_list={'issuer': '[APIDOMAIN]', 'authorization_endpoint': '[APIDOMAIN]/oxauth/restv1/authorize', 'token_endpoint': '[APIDOMAIN]/oxauth/restv1/token', 'userinfo_endpoint': '[APIDOMAIN]/oxauth/restv1/userinfo', 'clientinfo_endpoint': '[APIDOMAIN]/oxauth/restv1/clientinfo', 'end_session_endpoint': '[APIDOMAIN]/oxauth/restv1/end_session', 'registration_endpoint': '[APIDOMAIN]/oxauth/restv1/register', 'id_generation_endpoint': '[APIDOMAIN]/oxauth/restv1/id'}
        scope_list=['openid', 'controlled_client', 'jira_groups', 'user_name', 'profile', 'email', 'permission', 'geoss_user', 'OpenAccess', 'jira_mail', 'mobile_phone', 'phone', 'address', 'geoss_management', 'clientinfo']
        #testing the endpoints retrieval and supported scopes
        [uris,scopes] = oidc.getEndpointInformation('[APIDOMAIN]')
        self.assertEqual(scopes, scope_list)
        self.assertEqual(uris, url_list)
        #check the input parameters to get request
        self.assertIn(mock.call('[APIDOMAIN]/.well_known/openid-configuration',verify=True), mock_get.call_args_list)

        #provider_config={"scope": 'openid',"response_type": 'code', "client_id": 'randomClient',"redirect_uri": 'http://url/callback'}
        oidc.getRequestCode(uris,token=None, verify=False)        
        self.assertEqual(oidc._code, 'AIIEHGSKIUOIFNKLOSIUOI')
        oidc._authType='Bearer '
        oidc.getRequestCode(uris,token = 'aslf;alksjkekeke', verify=False)
        self.assertEqual(oidc._code, 'SplxlOBeZQQYbYS6WxSbIA')

    
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_token_retrieval(self, mock_get,raise_for_status=None):
        mock_resp = mock.Mock()
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        oidc = OpenIDClient()
        oidc.scope = 'openid'
        oidc._code = 'SplxlOBeZQQYbYS6WxSbIA'
        oidc.client_id = 'Default client'
        oidc.client_secret= 'itsASecret'
        oidc.method = 'POST'
        url_list={'issuer': '[APIDOMAIN]', 'authorization_endpoint': '[APIDOMAIN]/oxauth/restv1/authorize', 'token_endpoint': '[APIDOMAIN]/oxauth/restv1/token', 'userinfo_endpoint': '[APIDOMAIN]/oxauth/restv1/userinfo', 'clientinfo_endpoint': '[APIDOMAIN]/oxauth/restv1/clientinfo', 'end_session_endpoint': '[APIDOMAIN]/oxauth/restv1/end_session', 'registration_endpoint': '[APIDOMAIN]/oxauth/restv1/register', 'id_generation_endpoint': '[APIDOMAIN]/oxauth/restv1/id'}
         #POST example of access token retrieval. 
        oidc.postRequestToken(url_list, token = None, verify=True)
        self.assertEqual(oidc._token['access_token'], 'SlAV32hkKG')
        oidc._authType='Bearer '
        oidc.postRequestToken(url_list, token = 'SlAV32hkKG', verify=True)
        self.assertEqual(oidc._token['access_token'], '2YotnFZFEjr1zCsicMWpAA')
       

if __name__ == '__main__':
    unittest.main()


