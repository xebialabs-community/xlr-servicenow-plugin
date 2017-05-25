#
# Copyright 2017 XEBIALABS
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

snClient = ServiceNowClient.create_client(servicenowServer, username, password)

content = """
{"used_for":"%s","name":"%s","company":"%s","u_config_admin_group":"%s","version":"%s","u_vm":"%s","u_tomcat":"%s","u_mysql":"%s","u_space":"%s"}
""" % (environment, applicationName, company, configAdminGroup, version, virtualMachine, tomcat, mysql, cfSpace)
print "Sending content %s" % content

try:
    data = snClient.create_record( 'cmdb_ci_appl', content )
    #data = snClient.update_record( 'cmdb_ci_appl', content )
    sysId = data["sys_id"]
    print "#Created %s in Service Now.#\n" % (sysId)
    print snClient.print_record( data )
except Exception, e:
    print e
    print "Failed to create record in Service Now"
    sys.exit(1)
