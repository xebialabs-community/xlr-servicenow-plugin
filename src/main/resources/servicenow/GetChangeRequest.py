#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys

from servicenow.ServiceNowClientUtil import ServiceNowClientUtil

if servicenowServer is None:
    print "No server provided.\n"
    sys.exit(1)

if number is None:
    print "No number provided.\n"
    sys.exit(1)

if fieldNames is None:
    print "No field names provided.\n"
    sys.exit(1)

servicenow_client = ServiceNowClientUtil.createServiceNowClient(servicenowServer, username, password)
change_request = servicenow_client.get_change_request_with_fields(tableName, number, fieldNames)

rows = []
row = []
for field in fieldNames:
    row.append(change_request[field])
rows.append(row)
servicenow_client.print_table(fieldNames, rows)

