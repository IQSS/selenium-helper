import requests

from os.path import abspath, dirname, isfile, join, isdir

import unittest
import json

from msg_util import *

WORLDMAP_TOKEN_NAME = 'GEOCONNECT_TOKEN'
WORLDMAP_TOKEN_VALUE = '6f5912a778d6e3f1969ee10f8452ba3ca61f117556c7a29e36de45c3916d9b2c'
DATAVERSE_SERVER = 'http://localhost:8080'

class WorldMapBaseTest(unittest.TestCase):

    def setUp(self):
        global WORLDMAP_TOKEN_NAME, WORLDMAP_TOKEN_VALUE, DATAVERSE_SERVER
        self.wm_token_name = WORLDMAP_TOKEN_NAME
        self.wm_token_value = WORLDMAP_TOKEN_VALUE
        self.dataverse_server = DATAVERSE_SERVER
    
    def getWorldMapTokenDict(self):
        return { self.wm_token_name : self.wm_token_value }
        
    def runTest(self):
        msg('runTest')
        
    def tearDown(self):
        self.wmToken = None

class RetrieveFileMetadataTestCase(WorldMapBaseTest):

    def run_test01_metadata(self):
        
        api_url = '%s/api/worldmap/datafile/' % (self.dataverse_server)
        params = self.getWorldMapTokenDict()
        
        msg('api_url: %s' % api_url)     
        msg('params: %s' % params)     
        try:
            r = requests.post(api_url, data=json.dumps(params))
        except requests.exceptions.ConnectionError as e:
            msgx('Connection error: %s' % e.message)
        except:
            msgx("Unexpected error: %s" % sys.exc_info()[0])

        self.assertEqual(r.status_code, 200, "API call successful, with a 200 response?")
        msg(r.text)
        
        json_resp = r.json()
        self.assertEqual(json_resp.get('status'), 'OK', "status is 'OK'")

        metadata_json = json_resp.get('data', None)
        self.assertTrue(type(metadata_json) is not None, "Check that metadata_json is a dict")

        self.assertTrue(metadata_json.has_key('datafile_download_url') is True, "Check that metadata_json has 'datafile_download_url'")

        self.datafile_download_url = metadata_json['datafile_download_url']
        
    def run_test02_download_file(self):
        self.assertTrue(self.datafile_download_url is not None\
                        "Check that metadata_json has 'datafile_download_url'")
        
        
        
    



def get_suite():
    suite = unittest.TestSuite()
    suite.addTest(RetrieveFileMetadataTestCase())
    #suite.addTest(WidgetTestCase('test_resize'))
    return suite


if __name__=='__main__':
    test_suite = unittest.TestSuite(get_suite())
    text_runner = unittest.TextTestRunner().run(test_suite)