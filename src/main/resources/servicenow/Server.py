#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from servicenow.ServiceNowClient import ServiceNowClient

params = {
    'url': configuration.url, 'username': configuration.username
    , 'password': configuration.password, 'useOAuth': configuration.useOAuth
    , 'oauthUsername': configuration.oauthUsername, 'oauthPassword': configuration.oauthPassword
    , 'clientId': configuration.clientId, 'clientSecret': configuration.clientSecret
    , 'proxyHost': configuration.proxyHost, 'proxyPort': configuration.proxyPort
    , 'changeRecordTableName': configuration.changeRecordTableName
    , 'changeTaskTableName': configuration.changeTaskTableName
    , 'sysparmDisplayValue': configuration.sysparmDisplayValue
    , 'sysparmInputDisplayValue': configuration.sysparmInputDisplayValue
}

sn_client = ServiceNowClient.create_client(params)
content = None

print "Sending content %s" % content

data = sn_client.get_change_request_states()
