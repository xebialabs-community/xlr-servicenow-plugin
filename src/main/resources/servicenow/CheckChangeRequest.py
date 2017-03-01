#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
from servicenow.ServiceNowClient import ServiceNowClient

if servicenowServer is None:
    print "No server provided."
    sys.exit(1)

if number is None:
    print "No number provided.\n"
    sys.exit(1)

snClient = ServiceNowClient.create_client(servicenowServer, username, password, authToken)
change_request = snClient.get_change_request_with_fields(tableName, number, ['state'])
status = change_request["approval"]
print "Found %s in Service Now as %s" % (change_request['number'], status)
if "approved" == status:
    approval = False
    isClear = True
    print "ServiceNow approval received."
elif "rejected" == status:
    print "Failed to get approval from ServiceNow"
    sys.exit(1)

if change_request['state'] not in state_number:
    print "Change Request %s is in required state\n" % (number)
else:
    print "Change Request %s is NOT in required state\n" % (number)
    sys.exit(1)

print "\n"
print snClient.print_record(change_request)
