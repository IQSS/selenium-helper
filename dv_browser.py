from selenium_helper import SeleniumHelper
from msg_util import *
from random import randint
from collections import OrderedDict
import requests

class CreateDatasetTester:
    
    def __init__(self, dv_url, auth, expected_name='Pete Privileged'):
        self.dv_url = dv_url
        self.auth = auth
        self.expected_name = expected_name
        self.sdriver = SeleniumHelper()
    
    def has_expected_name(self):
        """
        Look for the logged in name in the upper right corner of the screen
        """
        assert self.sdriver is not None, "self.sdriver cannot be None"
        
        page_source = self.sdriver.get_page_source()
        search_str = '">%s' %  (self.expected_name)
        msgt('check for: [%s]' % search_str)
        if page_source.find(search_str) == -1:
            msg('!' * 200)
            msg('Not logged in as: %s' % self.expected_name)
            msgt('pause for 10 minutes!')
            self.sleep(60*10)
        else:
            msg('Still logged in as: %s' % self.expected_name)
        return True
        
    def logout(self):
        msg('Log out')        
        assert self.sdriver is not None, "self.sdriver cannot be None"
        
        e = self.sdriver.driver.find_element_by_partial_link_text('Log')
        #e = self.driver.find_element_by_link_text(link_text)
        if e: e.click()
        #self.sdriver.find_link_by_text_click('Log Out')
        
    def sleep(self, num_seconds=3):
        assert self.sdriver is not None, "self.sdriver cannot be None"
        msg('Sleeping for %s seconds' % num_seconds)
        self.sdriver.sleep(num_seconds)
    
    def goto_dataverse_user_page(self):
        assert self.sdriver is not None, "self.sdriver cannot be None"
        self.sdriver.goto_link('https://dvn-build.hmdc.harvard.edu/dataverseuser.xhtml')
    
    def goto_random_dvobject(self):
        msgt('Navigate to Random DvObject')
        assert self.sdriver is not None, "self.sdriver cannot be None"
        
        d = self.sdriver
        available_links = d.get_dvobject_links()
        if len(available_links) > 0:
            random_idx = randint(0, len(available_links)-1)
            msgt('go to random page: %s' % available_links[random_idx])
            d.goto_link(available_links[random_idx])
            self.sleep()
            self.has_expected_name()
            
            msg('go back home')
            d.goto_link("/")
            self.sleep()
            self.has_expected_name()
        else:
            msg('no available links...')
            
    def browse_around(self, loops=100):
        # assume already logged in
        #self.logout()
        #return
        for cnt in range(1, loops+1):
            msgt('Loop #%d' % cnt )
            d = self.sdriver
        
            # Go to home page, sleep, check name
            msg('go home')
            d.goto_link("/")
            self.sleep()
            self.has_expected_name()

            # go to random available page
            self.goto_random_dvobject()
                
            # Go to dataverse user page, sleep, check name
            self.goto_dataverse_user_page()
            self.sleep()
            self.has_expected_name()
    
            msg('go home')
            d.goto_link("/")
            self.sleep()
            self.has_expected_name()
            
            # Go to new dataset page, sleep, add data, cancel, check name
            self.start_adding_new_data_and_cancel()
            self.has_expected_name()
    
    def start_adding_new_data_and_cancel(self):
        msg('Add new dataset')
        assert self.sdriver is not None, "self.sdriver cannot be None"

        d = self.sdriver
        d.find_link_in_soup_and_click('New Dataset')
        
        self.sleep()
        # try to add title
        # find <a rel="title" class="pre-input-tag"></a>
        prefix = 'pre-input-'
        d.find_input_box_and_fill('%stitle' % prefix, 'A Hard Rain is Gonna Fall')
        d.find_input_box_and_fill('%sauthor' % prefix, 'Bob Dylan')
        d.find_input_box_and_fill('%sdatasetContact' % prefix, 'bd@harvard.edu')
        d.find_input_box_and_fill('%sdsDescription' % prefix, 'A long and winding description', input_type='textarea')
        
        d.find_by_id_click('datasetForm:cancelCreate')
        self.sleep()

    def login(self):
        d = self.sdriver
        
        msgt('login')
        d.get(self.dv_url)

        msg('click login')        
        d.find_link_by_text_click('Log In')

        msg('fill in username/pw click login')
        # login
        d.find_by_id_send_keys('loginForm:credentialsContainer2:0:credValue', self.auth[0])  
        d.find_by_id_send_keys('loginForm:credentialsContainer2:1:sCredValue', self.auth[1])      
        d.find_by_id_click('loginForm:login')
        self.sleep()
                
        msg('Check if Pete is logged in')
        self.has_expected_name()
        #assert has_expected_val > -1, "has_expected_val must be greater than 1"
        
        return
        #http://localhost:8080/dataset.xhtml?id=61&versionId=4
        #d.goto_link("/dataset.xhtml?id=61&versionId=4")
        #return
        self.sleep(2)
        
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

def run_as_user(dataverse_url, auth, expected_name):

    tester = CreateDatasetTester(dataverse_url, auth, expected_name=expected_name)
    tester.login()
    tester.browse_around(loops=100)

def run_user_pete(dataverse_url):
    auth = ('pete', 'pete')
    run_as_user(dataverse_url, auth, 'Pete Privileged')

def run_user_uma(dataverse_url):
    auth = ('uma', 'uma')
    run_as_user(dataverse_url, auth, 'Uma Underprivileged')

def run_user_nick(dataverse_url):
    auth = ('nick', 'nick')
    run_as_user(dataverse_url, auth, 'Nick NSA')

def run_user_cathy(dataverse_url):
    auth = ('cathy', 'cathy')
    run_as_user(dataverse_url, auth, 'Cathy Collaborator')

def run_user_gabbi(dataverse_url):
    auth = ('gabbi', 'gabbi')
    run_as_user(dataverse_url, auth, 'Gabbi Guest')



if __name__=='__main__':
    dataverse_url = 'https://dvn-build.hmdc.harvard.edu/'
    
    
    user_choices = OrderedDict( [ ('1' , run_user_pete)\
                    , ('2' , run_user_uma)\
                    , ('3' , run_user_nick)\
                    , ('4' , run_user_cathy)\
                    , ('5' , run_user_gabbi)\
                    ] )
    
    if len(sys.argv) == 2 and sys.argv[1] in user_choices.keys():
        print 'do something'
        user_choices[sys.argv[1]](dataverse_url)
    else:
        info_lines = []
        for k, v in user_choices.items():
            info_lines.append(' %s - %s' % (k, v.__name__))
            
        print """
Please run with one of the choices below:

%s 

example:
$ python dv_browser.py 1        
        """ % ('\n'.join(info_lines))
        

