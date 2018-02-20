#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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

snClient = ServiceNowClient.create_client(servicenowServer, username, password)
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
    if "Approved" == status:
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
