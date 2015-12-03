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

if fieldNames is None:
    print "No field names provided.\n"
    sys.exit(1)

servicenow_client = ServiceNowClientUtil.createServiceNowClient(servicenowServer, username, password)
change_request = servicenow_client.get_change_request(tableName, number, fieldNames)

rows = []
row = []
for field in fieldNames:
    row.append(change_request[field])
rows.append(row)
servicenow_client.print_table(fieldNames,rows)

