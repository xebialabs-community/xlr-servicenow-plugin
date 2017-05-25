#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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


