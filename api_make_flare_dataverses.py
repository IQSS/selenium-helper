import json
import os
import time
from msg_util import *
from api_dv_make_dataverse import APIHelper


class FlareMaker:
    
    def __init__(self, server_name, api_key):
        flare_info = open(os.path.join('input','flare.json'), 'r').read()
        flare_dict = json.loads(flare_info)
        self.flare_cnt = 0
        self.api_helper = APIHelper(server_name, api_key)
        
        self.make_dataverse_from_dict(flare_dict, depth=0)
    
    

    def make_dv_dict(self, dv_name):
        return dict( name=dv_name,\
                    alias=dv_name.replace(' ', '-').lower(),\
                    description='Store the datasets for %s' % dv_name,\
                    category='RESEARCH_PROJECTS',\
                    contactEmail='%s@harvard.edu' % (dv_name.replace(' ', '-').lower()),\
                    affiliation='hu test',\
                    permissionRoot=False,\
                    )

    def make_dataverse_from_dict(self, flare_dict, depth, parent_dataverse_alias=None):

        if flare_dict is None:
            return

        if self.flare_cnt == 5:
            msgx('stopping')

        dataverse_name = flare_dict.get('name', None)
        msgt('(%s) Make dataverse: %s' % (dataverse_name, self.flare_cnt))
        if dataverse_name is None:
            return

        dv_dict = self.make_dv_dict(dataverse_name)
        self.flare_cnt+=1

        current_dataverse_alias = dv_dict.get('alias')
        #self.dataverse_parent_lookup[current_dataverse_alias] = parent_dataverse_alias
        
        self.api_helper.create_dataverse(dv_dict, parent_dataverse_alias)
        time.sleep(2)
        
        for child_flare_dict in flare_dict.get('children', []):
            self.make_dataverse_from_dict(child_flare_dict\
                                        , depth=depth+1\
                                        , parent_dataverse_alias=current_dataverse_alias\
                                        )
 
if __name__=='__main__':
        
    fm = FlareMaker(server_name='http://localhost:8080', api_key='c9263d1d-12a6-49ab-ad95-d98acfd870e5')
   