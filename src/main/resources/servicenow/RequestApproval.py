#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
import com.xhaus.jyson.JysonCodec as json
from servicenow.ServiceNowClient import ServiceNowClient

if servicenowServer is None:
    print "No server provided."
    sys.exit(1)

if tableName is None:
    print "No tableName provided."
    sys.exit(1)

if content is None:
    print "No content provided."
    sys.exit(1)

if shortDescription is None:
    print "No shortDescription provided."
    sys.exit(1)

if description is None:
    print "No description provided."
    sys.exit(1)

snClient = ServiceNowClient.create_client(servicenowServer, username, password, authToken)
contentJSON = content % (shortDescription, description)
sysId = None

content = content % (shortDescription, description)

print "Sending content %s" % content

try:
    data = snClient.create_record( tableName, content )
    print "Returned DATA = %s" % (data)
    print json.dumps(data, indent=4, sort_keys=True)
    sysId = data["sys_id"]
    Ticket = data["number"]
    print "Created %s in Service Now." % (sysId)
    print "Created %s in Service Now." % (Ticket)
except Exception, e:
    exc_info = sys.exc_info()
    traceback.print_exception( *exc_info )
    print e
    print snClient.print_error( e )
    print "Failed to create record in Service Now"
    sys.exit(1)

isClear = False
while ( not isClear ):

  try:
    data = snClient.get_change_request(tableName, sysId)

    status = data["approval"]
    print "Found %s in Service Now as %s" % (data['number'], status)
    if "approved" == status:
        approval = False
        isClear = True
        print "ServiceNow approval received."
        ticket = data["number"]
    elif "rejected" == status:
        print "Failed to get approval from ServiceNow"
        sys.exit(1)
    else:
        time.sleep(5) 

  except:
        print json.dumps(data, indent=4, sort_keys=True)
        print "Error finding status for %s" % statusField
  # End try

# End While
