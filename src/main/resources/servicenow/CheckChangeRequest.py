#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
from servicenow.ServiceNowClient import ServiceNowClient

if servicenowServer is None:
    print "No server provided."
    sys.exit(1)

if number is None:
    print "No number provided.\n"
    sys.exit(1)

snClient = ServiceNowClient.create_client(servicenowServer, username, password)
data = ""

try:
    available_states = snClient.get_change_request_states()
    status_allowed = expectedStatus.split(',')
    for state in available_states:
        if state['label'] in status_allowed:
            state_number.append(state['value'])

    change_request = snClient.get_change_request(tableName, number, ['state'])
    if change_request['state'] not in state_number:
        print "Change Request %s is in required state\n" % (number)
    else:
        print "Change Request %s is NOT in required state\n" % (number)
        sys.exit(1)

    print "\n"
    print snClient.print_record( change_request )
except Exception, e:
    exc_info = sys.exc_info()
    traceback.print_exception( *exc_info )
    print e
    print "Error finding status for %s" % statusField
# End try


