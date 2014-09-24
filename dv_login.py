from selenium_helper import SeleniumHelper
from msg_util import *
import requests

class CreateDatasetTester:
    
    def __init__(self, dv_url, auth, fname):
        self.dv_url = dv_url
        self.auth = auth
        self.sdriver = SeleniumHelper()
        self.upload_fname = fname
        
    def login(self):
        d = self.sdriver
        
        msgt('login')
        d.get(self.dv_url)

        msg('click login')        
        d.find_link_by_text_click('Log In')

        msg('fill in username/pw click login')
        # login
        d.find_by_id_send_keys('loginForm:credentialsContainer2:0:credValue', auth[0])  # pete
        d.find_by_id_send_keys('loginForm:credentialsContainer2:1:sCredValue', auth[1]) # pete     
        d.find_by_id_click('loginForm:login')
        d.sleep(2)
        
        page_source = d.get_page_source()
        msg('Check if source exists')
        assert(page_source is not None, True)
        
        msg('Check if Pete is logged in')
        expected_val = '<a value="#" class="dropdown-toggle" data-toggle="dropdown">Pete Privileged'
        has_expected_val = page_source.find(expected_val)
        assert(has_expected_val > -1, True)
        
        return
        #http://localhost:8080/dataset.xhtml?id=61&versionId=4
        #d.goto_link("/dataset.xhtml?id=61&versionId=4")
        #return
        d.sleep(2)
        
        msg('Add new dataset')
        d.find_link_in_soup_and_click('New Dataset')
        # try to add title
        # find <a rel="title" class="pre-input-tag"></a>
        prefix = 'pre-input-'
        d.find_input_box_and_fill('%stitle' % prefix, 'A Hard Rain is Gonna Fall')
        d.find_input_box_and_fill('%sauthor' % prefix, 'Bob Dylan')
        d.find_input_box_and_fill('%sdatasetContact' % prefix, 'bd@harvard.edu')
        d.find_input_box_and_fill('%sdsDescription' % prefix, 'A long and winding description', input_type='textarea')
        #label-for-subject
        #d.find_input_box_and_fill('pre-input-title', 'Tangled Up In Blue')
        #d.find_link_in_soup_and_click('worldmap/map-it')
        
        """
        d.find_by_id_send_keys('dataverseForm:name', dv.name)
        d.find_by_id_send_keys('dataverseForm:alias', dv.alias)
        d.find_by_id_send_keys('dataverseForm:affiliation', dv.affiliation)
        d.find_by_id_send_keys('dataverseForm:contactEmail', dv.contactEmail)
        d.find_by_id_send_keys('dataverseForm:description', dv.description)
        d.find_by_id_click('dataverseForm:save')
        """

if __name__=='__main__':
    #dataverse_url = "http://localhost:8080"
    dataverse_url = 'http://dvn-build.hmdc.harvard.edu/'
    #dataverse_url = 'http://dvn-alpha.hmdc.harvard.edu/'
    auth = ('pete', 'petez')
    tester = CreateDatasetTester(dataverse_url, auth, None)
    tester.login()