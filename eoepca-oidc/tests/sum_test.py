#!/usr/bin/env python3
import json
def func(x):
    return x + 1

def retrieveCode(k):
    code = k.split('code=')[-1].split('&')
    return code[0]

def retrieveDiscoveryInfo():
    q={}
    with open('tst.json', 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data)
    scope_list=[]
    for k, v in obj.items():
        if "scopes_supported" in k:
            scope_list=v
        elif "endpoint" in k[-8:]:
            q[k]=v
        else:
            continue
    return q, scope_list

def test_answer():
    assert func(3) == 4
    assert retrieveCode('HTTP/1.1 302 Found Location: https://client.example.org/cb?code=SplxlOBeZQQYbYS6WxSbIA&state=af0ifjsldkj') ==  'SplxlOBeZQQYbYS6WxSbIA'
    scope_list=['openid', 'controlled_client', 'jira_groups', 'user_name', 'profile', 'email', 'permission', 'geoss_user', 'OpenAccess', 'jira_mail', 'mobile_phone', 'phone', 'address', 'geoss_management', 'clientinfo']
    url_list={'authorization_endpoint': '[APIDOMAIN]/oxauth/restv1/authorize', 'token_endpoint': '[APIDOMAIN]/oxauth/restv1/token', 'userinfo_endpoint': '[APIDOMAIN]/oxauth/restv1/userinfo', 'clientinfo_endpoint': '[APIDOMAIN]/oxauth/restv1/clientinfo', 'end_session_endpoint': '[APIDOMAIN]/oxauth/restv1/end_session', 'registration_endpoint': '[APIDOMAIN]/oxauth/restv1/register', 'id_generation_endpoint': '[APIDOMAIN]/oxauth/restv1/id'}
    [a,b]=retrieveDiscoveryInfo()
    assert a == url_list
    assert b == scope_list


test_answer()