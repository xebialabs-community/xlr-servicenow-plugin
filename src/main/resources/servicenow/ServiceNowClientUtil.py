#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from servicenow.ServiceNowClient import ServiceNowClient


class ServiceNowClientUtil(object):

    @staticmethod
    def createServiceNowClient(container, username, password):
        client = ServiceNowClient.create_client(container, username, password)
        return client