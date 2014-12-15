from selenium_helper import SeleniumHelper
from msg_util import *
from random import randint
from collections import OrderedDict
import json

from selenium_dv_actions import pause_script, login_user, logout_user,\
                        has_expected_name, goto_dataverse_user_page,\
                        goto_home, make_dataverse, goto_dataverse_by_alias,\
                        publish_dataverse


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



    def make_some_dataverses(self):

        # Already logged in...

        # Make dataverse 1
        #
        dv_info = dict( name='Elevation',\
                        alias='elevation',\
                        description='Elevation Tour Live Slane Castle,Ireland.. September 1 2001',\
                        category='RESEARCH_PROJECTS',\
                        contact_email='harvie@mudd.edu',\
                )
        make_dataverse(self.sdriver, dv_info)

        # Go to the Dataverse alias page
        #
        goto_dataverse_by_alias(self.sdriver, 'elevation')
        pause_script()

        # Publish the dataverse
        #
        publish_dataverse(self.sdriver)
        pause_script()
        self.check_name()

        # Make dataverse 2
        #
        dv_info = dict( name='Joshua Tree',\
                alias='desert',\
                description=' which took place during 1987, in support of their album',\
                category='RESEARCH_PROJECTS',\
                )
        make_dataverse(self.sdriver, dv_info)





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
    tester.make_some_dataverses()

def run_user_admin(dataverse_url):
    auth = ('admin', 'admin')
    run_as_user(dataverse_url, auth, 'Admin Dataverse')


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
    #dataverse_url = 'https://dvn-build.hmdc.harvard.edu/'
    #dataverse_url = 'https://shibtest.dataverse.org'
    dataverse_url = 'http://localhost:8080'


    user_choices = OrderedDict( [\
                      ('0', run_user_admin)\
                    , ('1' , run_user_pete)\
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


