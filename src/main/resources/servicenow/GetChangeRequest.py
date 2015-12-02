#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
import com.xhaus.jyson.JysonCodec as json

def print_table(headers, rows):
    print "\n|", "|".join(headers), "|"
    print "|", " ------ |" * len(headers)
    for r in rows:
        print "| ", "  |".join(r), " |"
    print "\n"

SN_RESULT_STATUS = 200

if servicenowServer is None:
    print "No server provided.\n"
    sys.exit(1)

if number is None:
    print "No number provided.\n"
    sys.exit(1)

if fieldNames is None:
    print "No field names provided.\n"
    sys.exit(1)


request = HttpRequest(servicenowServer, username, password)

servicenow_api_url = '/api/now/v1/table/%s?number=%s&sysparm_fields=%s' % (tableName,number,fieldNames)

response = request.get(servicenow_api_url, contentType = 'application/json')


# if response received from SN
if response.getStatus() == SN_RESULT_STATUS:
    # retrieve issue
    data = json.loads(response.getResponse())
    rows = []
    for issue in data['result']:
        row = []
        for field in fieldNames.split(','):
            row.append(issue[field])
        rows.append(row)
    print_table(fieldNames.split(","),rows)
else:
    print "Error from ServiceNow, HTTP Return: %s\n" % (response.getStatus())
    response.errorDump()
    sys.exit(1)

