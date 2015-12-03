#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import com.xhaus.jyson.JysonCodec as json

from httputil.HttpRequest import HttpRequest

SN_RESULT_STATUS = 200

class ServiceNowClient(object):
    def __init__(self, httpConnection, username=None, password=None):
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

    def print_table(self, headers, rows):
        print "\n|", "|".join(headers), "|"
        print "|", " ------ |" * len(headers)
        for r in rows:
            print "| ", "  |".join(r), " |"
        print "\n"

    def throw_error(self, response):
        print "Error from ServiceNow, HTTP Return: %s\n" % (response.getStatus())
        sys.exit(1)



