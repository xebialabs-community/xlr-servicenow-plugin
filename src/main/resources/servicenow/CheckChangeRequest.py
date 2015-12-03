#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
from servicenow.ServiceNowClientUtil import ServiceNowClientUtil

if servicenowServer is None:
    print "No server provided.\n"
    sys.exit(1)

if number is None:
    print "No number provided.\n"
    sys.exit(1)


# Fetch allowed state numbers
state_number = []
servicenow_client = ServiceNowClientUtil.createServiceNowClient(servicenowServer, username, password)
available_states = servicenow_client.get_change_request_states()
status_allowed = expectedStatus.split(',')
for state in available_states:
    if state['label'] in status_allowed:
        state_number.append(state['value'])

change_request = servicenow_client.get_change_request(tableName, number, 'state')
if change_request['state'] not in state_number:
    print "Change Request %s is in required state\n" % (number)
else:
    print "Change Request %s is NOT in required state\n" % (number)
    sys.exit(1)

