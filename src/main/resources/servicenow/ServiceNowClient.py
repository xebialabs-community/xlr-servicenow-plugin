#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest

SN_RESULT_STATUS = 200
RECORD_CREATED_STATUS = 201

class ServiceNowClient(object):

    def __init__(self, httpConnection, username=None, password=None):
        self.httpConnection = httpConnection
        self.httpRequest = HttpRequest(httpConnection, username, password)

    @staticmethod
    def create_client(httpConnection, username=None, password=None):
        return ServiceNowClient(httpConnection, username, password)


    def get_change_request_states(self):
        servicenow_api_url = '/api/now/v1/table/%s?element=state&name=task&sysparm_fields=%s' % ('sys_choice','value,label')
        response = self.httpRequest.get(servicenow_api_url, contentType = 'application/json')
        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        self.throw_error(response)

    def get_change_request(self, table_name,number,fields):
        servicenow_api_url = '/api/now/v1/table/%s?number=%s&sysparm_fields=%s' % (table_name,number,",".join(fields))
        response = self.httpRequest.get(servicenow_api_url, contentType = 'application/json')
        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            if len(data['result']) == 1:
                return data['result'][0]
        self.throw_error(response)

    def get_change_request(self, table_name,sysId):
        servicenow_api_url = '/api/now/v1/table/%s/%s' % (table_name, sysId)
        response = self.httpRequest.get(servicenow_api_url, contentType = 'application/json')
        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        self.throw_error(response)
        
    def create_record(self, table_name, content):
        servicenow_api_url = '/api/now/v1/table/%s' % (table_name)
        response = self.httpRequest.post(servicenow_api_url, body = content, contentType = 'application/json')

        if response.getStatus() == RECORD_CREATED_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        else:
            self.throw_error(response)
        # End if
    #End create_record

    def update_record(self, table_name, sysId, content):
        servicenow_api_url = '/api/now/v1/table/%s/%s' % (table_name, sysId)
        response = self.httpRequest.put(servicenow_api_url, body = content, contentType = 'application/json')

        if response.getStatus() == SN_RESULT_STATUS:
            data = json.loads(response.getResponse())
            return data['result']
        else:
            self.throw_error(response)
        # End if
    #End create_record

    def print_table(self, headers, rows):
        print "\n|", "|".join(headers), "|"
        print "|", " ------ |" * len(headers)
        for r in rows:
            print "| ", "  |".join(r), " |"
        print "\n"

    def print_record( self, myObj, outStr = "", prefix="", header=True ):
       if header:
          outStr = "%s| Key | Value |\n" % (outStr)
          outStr = "%s| --- | --- |\n" % (outStr)
       if type(myObj) is dict:
          for key in myObj.iterkeys():
              value = myObj[key]
              if type(value) is dict or type(value) is list:
                 p = "%s%s." % (prefix, key)
                 outStr =  "%s| %s%s |\n%s" % (outStr, prefix, key, self.print_record( value, "", p, False ) )
              else:
                 p = "%s%s" % (prefix, key)
                 outStr =  "%s| %s%s |%s |\n" % (outStr, prefix, key, value )
                 
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



