import requests
import json
from msg_util import *

class APIHelper:
    
    def __init__(self, server_name, api_key):
        self.api_key = api_key
        self.server_name = server_name
    
    def does_dataverse_exist(self, dv_alias):
        """
        GET http://{{SERVER}}/api/dvs/{{id}}
        """
        url_str = self.server_name + '/api/dvs/%s?key=%s' % (dv_alias, self.api_key)
        #url_str = self.server_name + '/api/dvs/%s' % (dv_alias)
        r = requests.get(url_str)
        
        msg('Encoding: %s' % r.encoding)
        msg('Text: %s' % r.text)
        msg('Status Code: %s' % r.status_code)
        
    def create_dataverse(self, dv_params, parent_dv_alias_or_id=None ):
        """Create a dataverse
        POST http://{{SERVER}}/api/dvs/{{ parent_dv_name }}?key={{username}}

        :param parent_dv_alias_or_id: str or integer, the alias or id of an existing datavese 
        :param dv_params: dict containing the parameters for the new dataverse

        Sample: Create Dataverse

        from dataverse_api import DataverseAPILink
        server_with_api = 'dvn-build.hmdc.harvard.edu'
        dat = DataverseAPILink(server_with_api, use_https=False, apikey='pete')
        dv_params = {
                    "alias":"hm_dv",
                    "name":"Home, Home on the Dataverse",
                    "affiliation":"Affiliation value",
                    "contactEmail":"pete@mailinator.com",
                    "permissionRoot":False,
                    "description":"API testing"
                    }
        parent_dv_alias_or_id = 'root'
        print dat.create_dataverse(parent_dv_alias_or_id, dv_params)
        """
        msgt('create_dataverse')
        if not type(dv_params) is dict:
            msgx('dv_params is None')

        if parent_dv_alias_or_id is None:
            parent_dv_alias_or_id = 'root'

        url_str = self.server_name + '/api/dvs/%s?key=%s' % (parent_dv_alias_or_id, self.api_key)
            
        headers = {'content-type': 'application/json'}    
        print 'url_str', url_str
        #return self.make_api_call(url_str, self.HTTP_POST, params=dv_params, headers=headers)
        
        r = requests.post(url_str, data=json.dumps(dv_params), headers=headers)#, auth=auth)
    
        msg('Encoding: %s' % r.encoding)
        msg('Text: %s' % r.text)
        msg('Status Code: %s' % r.status_code)

if __name__=='__main__':
    dv_params = {
    "alias":"peteTop",
    "name":"Top dataverse of Pete",
    "affiliation":"Affiliation value",
    "contactEmail":"pete@mailinator.com",
    "permissionRoot":False,
    "description":"Pete's top level dataverse"
    }
    api_helper = APIHelper('http://localhost:8080', api_key='c9263d1d-12a6-49ab-ad95-d98acfd870e5')
    #api_helper.create_dataverse(dv_params, 'root')
    api_helper.does_dataverse_exist('peteTop')
    