#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time, traceback
import com.xhaus.jyson.JysonCodec as json
from servicenow.ServiceNowClient import ServiceNowClient

def getVariableByName(variables, variableName):
   for variable in variables:
       if variable.key == variableName  :
           return variable
   return None
# End def 


def cancelChangeRequest(servicenowServer, sysId, cancelStatusId):
    snClient = ServiceNowClient.create_client(servicenowServer, None, None, None)
    tableName = servicenowServer.changeRecordTableName
    content = '{"state": "%s" }' % (cancelStatusId)

    logger.info ("Sending content %s" % content)

    try:
        data = snClient.update_record( tableName, sysId, content )
        logger.info("Cancelled Change request for release %s" % release.id)
    except Exception, e:
        exc_info = sys.exc_info()
        traceback.print_exception( *exc_info )
        logger.error( e)
        logger.error(snClient.print_error( e ))
        logger.error("Failed to update record in Service Now")
        sys.exit(1)
    # end try
# end def

if exportHook.servicenowServer is None:
    logger.error("No server provided.")
    sys.exit(1)
else :
    servicenowServer = {
                        'url':exportHook.servicenowServer.url, 'username':exportHook.servicenowServer.username, 
                       'password':exportHook.servicenowServer.password,'useOAuth':exportHook.servicenowServer.useOAuth 
                       ,'clientId':exportHook.servicenowServer.clientId, 'clientSecret':exportHook.servicenowServer.clientSecret
                       ,'proxyHost': exportHook.servicenowServer.proxyHost, 'proxyPort':exportHook.servicenowServer.proxyPort
                       , 'changeRecordTableName': exportHook.servicenowServer.changeRecordTableName, 'changeTaskTableName': exportHook.servicenowServer.changeTaskTableName 
                       }
if release.status != 'ABORTED' :
   print "Release status is %s, ignoring Abort Hook" % (release.status)
else:
    sysIdVar = getVariableByName(release.variables, exportHook.sysId )
    if sysIdVar is None:
       logger.error( "Variable %s not found in release" % exportHook.sysId)
       sys.exit(1)
    else:
        sysId = sysIdVar.value
        cancelChangeRequest(servicenowServer, sysId, exportHook.cancelStatusId)
