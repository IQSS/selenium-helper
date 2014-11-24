from selenium_helper import SeleniumHelper
from msg_util import *
from random import randint
from collections import OrderedDict
import requests
from datetime import datetime
import time
import os

from selenium_dv_actions import pause_script, login_user, logout_user,\
                        has_expected_name, goto_dataverse_user_page\
                        , goto_home, make_dataverse


class CreateDatasetTester:

    def __init__(self, dv_url, auth, expected_name='Pete Privileged'):
        self.dv_url = dv_url
        self.auth = auth
        self.expected_name = expected_name
        self.sdriver = SeleniumHelper()


    def check_name(self):
        """
        Look for the logged in name in the upper right corner of the screen
        """
        has_expected_name(self.sdriver, self.expected_name)
        return True


    def goto_random_dvobject(self):
        msgt('Navigate to Random DvObject')
        assert self.sdriver is not None, "self.sdriver cannot be None"

        d = self.sdriver
        available_links = d.get_dvobject_links()
        if len(available_links) > 0:
            random_idx = randint(0, len(available_links)-1)
            msgt('go to random page: %s' % available_links[random_idx])
            d.goto_link(available_links[random_idx])
            pause_script()
            self.check_name()

            msg('go back home')
            d.goto_link("/")
            pause_script()
            self.check_name()
        else:
            msg('no available links...')

    def browse_around(self, loops=1):
        # assume already logged in

        for cnt in range(1, loops+1):

            # Every Nth loop, logout and login
            #
            loop_to_logout = 2  # e.g. '3' means every 3rd loop, '10' means every 10th loop, etc.
            if cnt > 0 and (cnt % loop_to_logout) == 0:
                msgt('Log out and then Log in again')
                #msg('cnt/mod: %s|%s' % (cnt, (cnt%loop_to_logout)))
                logout_user(self.sdriver)
                pause_script()

                self.login()
                pause_script()
                self.check_name()

            dv_info = dict( name='Elevation',\
                    alias='elevation',\
                    description='Elevation Tour Live Slane Castle,Ireland.. September 1 2001',\
                    category='RESEARCH_PROJECTS',\
                    contact_email='harvie@mudd.edu',\
                    )
            make_dataverse(self.sdriver, dv_info)
            return


            msgt('Loop #%d' % cnt )
            d = self.sdriver

            # Go to home page, sleep, check name
            goto_home(self.sdriver)
            pause_script()
            self.check_name()

            # go to random available page
            self.goto_random_dvobject()

            # Go to dataverse user page, sleep, check name
            goto_dataverse_user_page(self.sdriver)
            pause_script()
            self.check_name()


            goto_home(self.sdriver)
            pause_script()
            self.check_name()

            msg('go to advanced search')
            d.goto_link('/search/advanced.xhtml')
            pause_script()
            d.find_by_id_send_keys('advancedSearchForm:dvFieldName', 'dataverse')
            self.check_name()

            # Go to new dataset page, sleep, add data, cancel, check name
            #self.start_adding_new_data_and_cancel()
            #self.check_name()

    def start_adding_new_data_and_cancel(self):
        msg('Add new dataset')
        assert self.sdriver is not None, "self.sdriver cannot be None"

        d = self.sdriver
        d.find_link_in_soup_and_click('New Dataset')

        pause_script()
        # try to add title
        # find <a rel="title" class="pre-input-tag"></a>
        prefix = 'pre-input-'
        d.find_input_box_and_fill('%stitle' % prefix, 'A Hard Rain is Gonna Fall')
        d.find_input_box_and_fill('%sauthor' % prefix, 'Bob Dylan')
        d.find_input_box_and_fill('%sdatasetContact' % prefix, 'bd@harvard.edu')
        d.find_input_box_and_fill('%sdsDescription' % prefix, 'A long and winding description', input_type='textarea')

        d.find_by_id_click('datasetForm:cancelCreate')
        pause_script()

    def login(self):
        login_user(self.sdriver, self.dv_url, self.auth[0], self.auth[1])

        msg('Check if Pete is logged in')
        self.check_name()


def run_as_user(dataverse_url, auth, expected_name):

    tester = CreateDatasetTester(dataverse_url, auth, expected_name=expected_name)
    tester.login()
    tester.browse_around(loops=1000)

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
    #dataverse_url = 'https://shibtest.dataverse.org'
    #dataverse_url = 'http://localhost:8080'


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


