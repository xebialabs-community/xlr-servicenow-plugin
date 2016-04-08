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

if tableName is None:
    print "No tableName provided."
    sys.exit(1)

if ticket is None:
    print "No Ticket provided."
    sys.exit(1)

snClient = ServiceNowClient.create_client(servicenowServer, username, password)

query = "number=%s" % ( ticket )

try:
    data = snClient.find_record( tableName, query )
    numRecords = len(data)
    print "Found %s records for %s" % (numRecords, ticket)
    data = data[0]
    sysId = data["sys_id"]
    print "Found %s in Service Now with sysId = %s." % (ticket, sysId)
    print "\n"
    print snClient.print_record( data )
except Exception, e:
    exc_info = sys.exc_info()
    traceback.print_exception( *exc_info )
    print e
    print "Failed to find record in Service Now"
    sys.exit(1)


