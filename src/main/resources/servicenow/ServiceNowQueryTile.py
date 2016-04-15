#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import com.xhaus.jyson.JysonCodec as json

if not servicenowServer:
    raise Exception("ServiceNow server ID must be provided")
if not username:
    username = servicenowServer["username"]
if not password:
    password = servicenowServer["password"]

servicenowUrl = servicenowServer['url']

credentials = CredentialsFallback(servicenowServer, username, password).getCredentials()
content = None
RESPONSE_OK_STATUS = 200
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
    row_map['link'] = servicenowUrl + "nav_to.do?uri=%s.do?sys_id=%s" % (tableName, item['sys_id'])
    return row_map

servicenowAPIUrl = servicenowUrl + '/api/now/v1/table/%s?sysparm_display_value=true&sysparm_limit=1000&sysparm_query=%s' % (tableName, query)

servicenowResponse = XLRequest(servicenowAPIUrl, 'GET', content, credentials['username'], credentials['password'], 'application/json').send()
if servicenowResponse.status == RESPONSE_OK_STATUS:
    json_data = json.loads(servicenowResponse.read())
    rows = {}
    for item in json_data['result']:
        row = item['number']
        rows[row] = get_row_data(item)
    data = rows
else:
    error = json.loads(servicenowResponse.read())
    if 'Invalid table' in error['error']['message']:
        print "Invalid Table Name"
        data = {"Invalid table name"}
        servicenowResponse.errorDump()
    else:
        print "Failed to run query in Service Now"
        servicenowResponse.errorDump()
        sys.exit(1)