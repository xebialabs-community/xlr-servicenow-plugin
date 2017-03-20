#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time, traceback
import com.xhaus.jyson.JysonCodec as json
from servicenow.ServiceNowClient import ServiceNowClient

if servicenowServer is None:
    print "No server provided."
    sys.exit(1)

if sysId is None:
    print "No sysId provided."
    sys.exit(1)

if tableName is None:
    print "No tableName provided."
    sys.exit(1)

if pollInterval is None:
    print "No pollInterval provided."
    sys.exit(1)


isClear = False
snClient = ServiceNowClient.create_client(servicenowServer, username, password)
data = ""

while ( not isClear ):

  try:
    data = snClient.get_change_request(tableName, sysId)

    status = data[statusField]
    if status == checkForStatus :
         status = data[statusField]
         ticket = data["number"]
         print "Found %s in Service Now." % (sysId)
         isClear = True
    # End if
  except Exception, e:
    exc_info = sys.exc_info()
    traceback.print_exception( *exc_info )
    print e
    print snClient.print_error( e )
    print "Error finding status for %s" % statusField
  # End try

  time.sleep( pollInterval )
# End While

print "\n"
print snClient.print_record( data )


