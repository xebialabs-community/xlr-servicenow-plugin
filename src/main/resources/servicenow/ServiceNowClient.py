#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import urllib
import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest

SN_RESULT_STATUS       = 200
RECORD_CREATED_STATUS  = 201

class ServiceNowClient(object):
    def __init__(self, httpConnection, username=None, password=None): 
        self.headers = {}
        self.httpConnection = httpConnection
        self.accessToken = 'acccccc'
        self.refreshToken = 'reeeeeee'

        if username is not None:
           self.httpConnection['username'] = username
        if password is not None:
           self.httpConnection['password'] = password

        if self.httpConnection['useOAuth']  == True:
           tokenData = self.create_oauth_token(self.httpConnection)
           self.accessToken  = tokenData['access_token']
           self.refreshToken = tokenData['refresh_token']
           self.set_token_header(self.accessToken)

        self.httpRequest = HttpRequest(self.httpConnection, username, password)
        self.sysparms = 'sysparm_display_value=%s&sysparm_input_display_value=%s' % (self.httpConnection['sysparmDisplayValue'], self.httpConnection['sysparmInputDisplayValue'])

    @staticmethod
    def create_client(httpConnection, username=None, password=None):
        return ServiceNowClient(httpConnection, username, password)

    def get_change_request_states(self):
        servicenow_api_url = '/api/now/v1/table/%s?element=state&name=task&sysparm_fields=%s&%s' % ('sys_choice', 'value,label', self.sysparms)
        response = self.httpRequest.get(servicenow_api_url, contentType='application/json', headers = self.headers)
        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        self.throw_error(response)

    def get_change_request_with_fields(self, table_name, number, fields):
        servicenow_api_url = '/api/now/v1/table/%s?number=%s&sysparm_fields=%s&%s' % (table_name, number, ",".join(fields), self.sysparms)
        response = self.httpRequest.get(servicenow_api_url, contentType='application/json', headers = self.headers)
        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            if len(data['result']) == 1:
                return data['result'][0]
        self.throw_error(response)

    def get_change_request(self, table_name, sysId):
        servicenow_api_url = '/api/now/v1/table/%s/%s?%s' % (table_name, sysId, self.sysparms)
        response = self.httpRequest.get(servicenow_api_url, contentType='application/json', headers = self.headers)
        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        elif response.getStatus() == 401 and self.httpConnection['useOAuth'] == True :
             # Retry again, may be the token has expired
             tokenData = refresh_token(self.httpConnection, self.refreshToken)
             self.set_token_header(tokenData['access_token'])
             response = self.httpRequest.get(servicenow_api_url, contentType='application/json', headers = self.headers)
             if response.getStatus() == SN_RESULT_STATUS:
                data = json.loads(response.getResponse())
                return data['result']
        self.throw_error(response)

    def create_record(self, table_name, content):
        servicenow_api_url = '/api/now/v1/table/%s?%s' % (table_name, self.sysparms)
        response = self.httpRequest.post(servicenow_api_url, body=content, contentType='application/json', headers = self.headers)
       
        if response.getStatus() == RECORD_CREATED_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        else:
            self.throw_error(response)
            # End if

    # End create_record

    def update_record(self, table_name, sysId, content):
        servicenow_api_url = '/api/now/v1/table/%s/%s?%s' % (table_name, sysId, self.sysparms)
        response = self.httpRequest.put(servicenow_api_url, body=content, contentType='application/json', headers = self.headers)

        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        else:
            self.throw_error(response)
            # End if

    # End create_record

    def find_record(self, table_name, query):
        servicenow_api_url = '/api/now/v1/table/%s?%s&%s' % (table_name, query, self.sysparms)
        print "Servic Now URL = %s " % (servicenow_api_url)
        response = self.httpRequest.get(servicenow_api_url, contentType='application/json', headers = self.headers)

        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        else:
            print "find_record error %s" % (response)
            self.throw_error(response)
            # End if

    # End find_record

    def print_error(self, response):
        if type(response) is dict:
           outStr =   "| Status  | %s |\n" % ( response["status"] )
           outStr = "%s| Message | %s |\n" % ( outStr, response["error"]["message"] )
           outStr = "%s| Detail  | %s |\n" % ( outStr, response["error"]["detail"] )
           return outStr
        # End if
        return response
    #End  print_error

    def print_table(self, headers, rows):
        print "\n|", "|".join(headers), "|"
        print "|", " ------ |" * len(headers)
        for r in rows:
            print "| ", "  |".join(r), " |"
        print "\n"

    def print_record(self, myObj, outStr="", prefix="", header=True):
        if header:
            outStr = "%s| Key | Value |\n" % (outStr)
            outStr = "%s| --- | --- |\n" % (outStr)
        if type(myObj) is dict:
            for key in myObj.iterkeys():
                value = myObj[key]
                if type(value) is dict or type(value) is list:
                    p = "%s%s." % (prefix, key)
                    outStr = "%s| %s%s |\n%s" % (outStr, prefix, key, self.print_record(value, "", p, False))
                else:
                    p = "%s%s" % (prefix, key)
                    outStr = "%s| %s%s |%s |\n" % (outStr, prefix, key, value)

        elif type(myObj) is list:
            for value in myObj:
                outStr = "%s| | %s\n" % (outStr, value)
        else:
            outStr = "%s%s" % (outStr, myObj)
        # End if
        return outStr

    def throw_error(self, response):
        print "Error from ServiceNow, HTTP Return: %s\n" % (response.getStatus())
        sys.exit(1)

    def EmptyToNone(self,value):
        if value is None:
           return None
        elif value.strip() == '':
             return None
        else:
            return value

    def create_oauth_token(self, httpConnection):
        servicenow_oauth_url     = "/oauth_token.do"
        content                  = {}
        content['grant_type']    = 'password'
        content['client_id']     = httpConnection['clientId']
        content['client_secret'] = httpConnection['clientSecret']
        content['username']      = httpConnection['oauthUsername']
        content['password']      = httpConnection['oauthPassword']
        httpRequest              = HttpRequest(httpConnection, None, None)
        response                 = httpRequest.post(servicenow_oauth_url, body=urllib.urlencode(content), contentType='application/x-www-form-urlencoded')
        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            return data
        else:
            self.throw_error(response)

    def refresh_token(self, httpConnection, refreshToken):
        servicenowUrl = "/oauth_token.do"
        content                  = {}
        content['grant_type']    = 'refresh_token'
        content['client_id']     = httpConnection['clientId']
        content['client_secret'] = httpConnection['clientSecret']
        content['refresh_token'] = refreshToken
        httpRequest = HttpRequest(httpConnection, None, None)
        response = httpRequest.post(servicenowUrl, body=urllib.urlencode(content), contentType='application/x-www-form-urlencoded')
        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            self.accessToken = data['access_token']
        else:
            print "Unale to refresh token using %s" % refreshToken
            self.throw_error(response)        

    def set_token_header(authToken):
        self.headers['Authorization'] = "Bearer %s" % (authToken)

    def close_client(self):
        if self.httpConnection['useOAuth'] == True :
           httpRequest = HttpRequest(self.httpConnection, None, None)
           servicenowApiUrl = "/oauth_revoke_token.do?token=%s" % self.accessToken
           response = httpRequest.get(servicenowApiUrl)
           servicenowApiUrl = "/oauth_revoke_token.do?token=%s" % self.refreshToken
           response = httpRequest.get(servicenowApiUrl)
