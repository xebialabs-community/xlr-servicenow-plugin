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

isClear = False
snClient = ServiceNowClient.create_client(servicenowServer, username, password)

while ( not isClear ):

  try:
    data = snClient.get_change_request(tableName, sysId)

    status = data[statusField]
    if status == checkForStatus :
         print "Found %s in Service Now." % (sysId)
         status = data[statusField]
         ticket = data["number"]
         print "Found %s in Service Now." % (sysId)
         print json.dumps(data, indent=4, sort_keys=True)
         isClear = True
    # End if
  except:
        print json.dumps(data, indent=4, sort_keys=True)
        print "Error finding status for %s" % statusField
  # End try

  time.sleep( pollInterval )
# End While
