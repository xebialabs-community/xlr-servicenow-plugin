#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import urllib
import com.xhaus.jyson.JysonCodec as json
from servicenow.ServiceNowClient import ServiceNowClient

if not servicenowServer:
    raise Exception("ServiceNow server ID must be provided")

snClient = ServiceNowClient.create_client(servicenowServer, username, password, authToken)
servicenowUrl = servicenowServer['url'].rstrip("/")

content = None
print "Sending content %s" % content

def get_row_data(item):
    row_map = {}
    for column in detailsViewColumns:
        if detailsViewColumns[column] and "." in detailsViewColumns[column]:
            json_col = detailsViewColumns[column].split('.')
            if item[json_col[0]]:
                row_map[column] = item[json_col[0]][json_col[1]]
        else:
            row_map[column] = item[column]
    row_map['link'] = servicenowUrl + "/nav_to.do?uri=%s.do?sys_id=%s" % (tableName, item['sys_id'])
    return row_map

results = snClient.find_record(tableName, "sysparm_display_value=true&sysparm_limit=1000&sysparam_query=%s"% (urllib.quote_plus(query)) )
rows= {}
for item in results:
    row = item['number']
    rows[row] = get_row_data(item)
data = rows

