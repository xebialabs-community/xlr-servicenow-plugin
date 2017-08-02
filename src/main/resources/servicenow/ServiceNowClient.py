#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import sys
import urllib
import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest

SN_RESULT_STATUS       = 200
RECORD_CREATED_STATUS  = 201

class ServiceNowClient(object):
    def __init__(self, httpConnection, username=None, password=None): 
        self.headers        = {}
        self.accessToken    = None
        self.refreshToken   = None
        self.httpConnection = httpConnection
        self.useOAuth = httpConnection['useOAuth']
        if username:
           self.httpConnection['username'] = username
        if password:
           self.httpConnection['password'] = password
        self.httpRequest = HttpRequest(self.httpConnection, username, password)
        self.sysparms = 'sysparm_display_value=%s&sysparm_input_display_value=%s' % (self.httpConnection['sysparmDisplayValue'], self.httpConnection['sysparmInputDisplayValue'])

    @staticmethod
    def create_client(httpConnection, username=None, password=None):
        return ServiceNowClient(httpConnection, username, password)

    def get_change_request_states(self):
        if self.useOAuth : self.issue_token()
        servicenow_api_url = '/api/now/v1/table/%s?element=state&name=task&sysparm_fields=%s&%s' % ('sys_choice', 'value,label', self.sysparms)
        response = self.httpRequest.get(servicenow_api_url, contentType='application/json', headers = self.headers)
        if self.useOAuth :self.revoke_token()
        
        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        self.throw_error(response)
       
    def get_scorecards(self):
        if self.useOAuth :self.issue_token()
        servicenow_api_url = '/api/now/v1/pa/scorecards'
        response = self.httpRequest.get(servicenow_api_url, contentType='application/json', headers = self.headers)
        if self.useOAuth :self.revoke_token()
        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        self.throw_error(response)

    def get_change_request_with_fields(self, table_name, number, fields):
        if self.useOAuth :self.issue_token()
        servicenow_api_url = '/api/now/v1/table/%s?number=%s&sysparm_fields=%s&%s' % (table_name, number, ",".join(fields), self.sysparms)
        response = self.httpRequest.get(servicenow_api_url, contentType='application/json', headers = self.headers)
        if self.useOAuth :self.revoke_token()

        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            if len(data['result']) == 1:
                return data['result'][0]
        self.throw_error(response)

    def get_change_request(self, table_name, sys_id):
        if self.useOAuth :self.issue_token()
        servicenow_api_url = '/api/now/v1/table/%s/%s?%s' % (table_name, sys_id, self.sysparms)
        response = self.httpRequest.get(servicenow_api_url, contentType='application/json', headers = self.headers)
        if self.useOAuth :self.revoke_token()

        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        self.throw_error(response)

    def create_record(self, table_name, content):
        if self.useOAuth :self.issue_token()
        servicenow_api_url = '/api/now/v1/table/%s?%s' % (table_name, self.sysparms)
        response = self.httpRequest.post(servicenow_api_url, body=content, contentType='application/json', headers = self.headers)
        if self.useOAuth :self.revoke_token()

        if response.getStatus() == RECORD_CREATED_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        else:
            self.throw_error(response)
        # End if

    # End create_record

    def update_record(self, table_name, sysId, content):
        if self.useOAuth :self.issue_token()
        servicenow_api_url = '/api/now/v1/table/%s/%s?%s' % (table_name, sysId, self.sysparms)
        response = self.httpRequest.put(servicenow_api_url, body=content, contentType='application/json', headers = self.headers)
        if self.useOAuth :self.revoke_token()

        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        else:
            self.throw_error(response)
        # End if

    # End create_record

    def find_record(self, table_name, query):
        if self.useOAuth :self.issue_token()
        servicenow_api_url = '/api/now/v1/table/%s?%s&%s' % (table_name, query, self.sysparms)
        print "Service Now URL = %s " % (servicenow_api_url)
        response = self.httpRequest.get(servicenow_api_url, contentType='application/json', headers = self.headers)
        if self.useOAuth :self.revoke_token()

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
        print "Detailed error: %s\n" % response.response
        if self.useOAuth :self.revoke_token()
        sys.exit(1)

    def EmptyToNone(self,value):
        if value is None:
           return None
        elif value.strip() == '':
             return None
        else:
            return value

    def issue_token(self):
        print "Issuing a new token"
        tokenData = self.create_token(self.httpConnection)
        self.set_token_header(tokenData)

    def create_token(self, httpConnection):
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
        print 'Could not get access token'
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
            return data
        print "Unable to refresh token using %s" % refreshToken
        self.throw_error(response)        

    def set_token_header(self, tokenData):
        self.accessToken  = tokenData['access_token']
        self.refreshToken = tokenData['refresh_token']
        self.headers['Authorization'] = "Bearer %s" % (self.accessToken)

    def revoke_token(self):
        print "Revoking token"
        httpRequest = HttpRequest(self.httpConnection, None, None)
        servicenowApiUrl = "/oauth_revoke_token.do?token=%s" % self.accessToken
        response = httpRequest.get(servicenowApiUrl)
        servicenowApiUrl = "/oauth_revoke_token.do?token=%s" % self.refreshToken
        response = httpRequest.get(servicenowApiUrl)
