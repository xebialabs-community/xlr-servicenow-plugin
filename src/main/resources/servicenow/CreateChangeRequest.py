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

if shortDescription is None:
    print "No shortDescription provided."
    sys.exit(1)

if comments is None:
    print "No comments provided."
    sys.exit(1)

snClient = ServiceNowClient.create_client(servicenowServer, username, password)

content = """
{
  "short_description"   : "%s"
, "comments"            : "%s"
, "cmdb_ci"             : "%s"
, "assignment_group"    : "%s"
, "assigned_to"         : "%s"
, "implementation_plan" : "%s"
, "backout_plan"        : "%s"
, "start_date"          : "%s"
, "end_date"            : "%s"
}
""" % ( 
  shortDescription
, comments
, configurationItem
, assignmentGroup
, assignTo
, '' if implementationPlan is None else implementationPlan.replace('\n','\\n').replace('\r','\\r')
, '' if backoutPlan        is None else backoutPlan.replace('\n','\\n').replace('\r','\\r')
, plannedStartDateTime
, plannedEndDateTime 
)

print "Sending content %s" % content

try:
    data = snClient.create_record( tableName, content )
    sysId = data["sys_id"]
    Ticket = data["number"]
    print "Created %s in Service Now." % (sysId)
    print "Created %s in Service Now." % (Ticket)
    print "\n"
    print snClient.print_record( data )
except Exception, e:
    exc_info = sys.exc_info()
    traceback.print_exception( *exc_info )
    print e
    print snClient.print_error( e )
    print "Failed to create record in Service Now"
    sys.exit(1)


