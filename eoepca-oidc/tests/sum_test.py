#!/usr/bin/env python3
import requests
import json
from requests.exceptions import HTTPError
import unittest
from unittest import mock
import os, sys
sys.path.append(os.path.abspath('..'))
from OpenIDClient import OpenIDClient

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    with open('tst.json', 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data)
    print(type(obj))
    for i  in kwargs:
        print(kwargs.get(i))
    if '/.well_known/openid-configuration' in args[0]:
        return MockResponse(obj, 200)
    elif kwargs.get('header') and 'scope' in kwargs.get('data') and 'response_type' in kwargs.get('data') and 'client_id' in kwargs.get('data') and 'redirect_uri' in kwargs.get('data'):
        return MockResponse('HTTP/1.1 302 Found Location: https://client.example.org/cb?code=SplxlOBeZQQYbYS6WxSbIA&state=af0ifjsldkj', 200)
    return MockResponse(None, 404)



class OIDC_Unit_Test(unittest.TestCase):

    # First, mock has to simulate http response, therefore a patch of get and post methods from requests library will be needed.
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_fetch(self, mock_get,raise_for_status=None):
        mock_resp = mock.Mock()
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        
        oidc = OpenIDClient()
        oidc.scope = 'openid'
        url_list={'issuer': '[APIDOMAIN]', 'authorization_endpoint': '[APIDOMAIN]/oxauth/restv1/authorize', 'token_endpoint': '[APIDOMAIN]/oxauth/restv1/token', 'userinfo_endpoint': '[APIDOMAIN]/oxauth/restv1/userinfo', 'clientinfo_endpoint': '[APIDOMAIN]/oxauth/restv1/clientinfo', 'end_session_endpoint': '[APIDOMAIN]/oxauth/restv1/end_session', 'registration_endpoint': '[APIDOMAIN]/oxauth/restv1/register', 'id_generation_endpoint': '[APIDOMAIN]/oxauth/restv1/id'}
        scope_list=['openid', 'controlled_client', 'jira_groups', 'user_name', 'profile', 'email', 'permission', 'geoss_user', 'OpenAccess', 'jira_mail', 'mobile_phone', 'phone', 'address', 'geoss_management', 'clientinfo']
        #testing the endpoints retrieval and supported scopes
        [uris,scopes] = oidc.getDiscoveryUrl('[APIDOMAIN]')
        self.assertEqual(scopes, scope_list)
        self.assertEqual(uris, url_list)
        #check the input parameters to get request
        self.assertIn(mock.call('[APIDOMAIN]/.well_known/openid-configuration',verify=True), mock_get.call_args_list)

        provider_config={"scope": 'openid',"response_type": 'code', "client_id": 'randomClient',"redirect_uri": 'http://url/callback'}
        oidc.getRequestCode(uris,token = 'aslf;alksjkekeke', verify=False)
        self.assertEqual(oidc._code, 'SplxlOBeZQQYbYS6WxSbIA')
        
       
    
if __name__ == '__main__':
    unittest.main()


