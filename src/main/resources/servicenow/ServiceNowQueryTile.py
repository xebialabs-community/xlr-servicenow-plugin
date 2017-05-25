#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import urllib
import com.xhaus.jyson.JysonCodec as json
from servicenow.ServiceNowClient import ServiceNowClient

if not servicenowServer:
    raise Exception("ServiceNow server ID must be provided")

snClient = ServiceNowClient.create_client(servicenowServer, username, password)
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


results = snClient.find_record(tableName, "sysparm_display_value=true&sysparm_limit=1000&sysparm_query=%s"% (urllib.quote_plus('' if query == None else query)) )

rows= {}
for item in results:
    row = item['number']
    rows[row] = get_row_data(item)
data = rows

