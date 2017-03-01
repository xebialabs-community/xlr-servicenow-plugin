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

if sysId is None:
    print "No sysId provided."
    sys.exit(1)

if content is None:
    print "No content provided."
    sys.exit(1)

snClient = ServiceNowClient.create_client(servicenowServer, username, password, authToken)


print "Sending content %s" % content

try:
    data = snClient.update_record( tableName, sysId, content )
    print "\n"
    print snClient.print_record( data )
except Exception, e:
    exc_info = sys.exc_info()
    traceback.print_exception( *exc_info )
    print e
    print snClient.print_error( e )
    print "Failed to create record in Service Now"
    sys.exit(1)


