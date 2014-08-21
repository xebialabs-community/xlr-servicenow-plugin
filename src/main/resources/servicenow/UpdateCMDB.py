#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
import com.xhaus.jyson.JysonCodec as json

RECORD_CREATED_STATUS = 201

if servicenowServer is None:
    print "No server provided."
    sys.exit(1)

servicenowUrl = servicenowServer['url']

credentials = CredentialsFallback(servicenowServer, username, password).getCredentials()
content = """
{"used_for":"%s","name":"%s","company":"%s","u_config_admin_group":"%s","version":"%s","u_vm":"%s","u_tomcat":"%s","u_mysql":"%s","u_space":"%s"}
""" % (environment, applicationName, company, configAdminGroup, version, virtualMachine, tomcat, mysql, cfSpace)

print "Sending content %s" % content

servicenowAPIUrl = servicenowUrl + '/api/now/table/cmdb_ci_appl'

servicenowResponse = XLRequest(servicenowAPIUrl, 'POST', content, credentials['username'], credentials['password'], 'application/json').send()

if servicenowResponse.status == RECORD_CREATED_STATUS:
    data = json.loads(servicenowResponse.read())
    sysId = data["result"]["sys_id"]
    print "Created %s in Service Now." % (sysId)
else:
    print "Failed to create approval record in Service Now"
    servicenowResponse.errorDump()
    sys.exit(1)

