import os
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
        self.flare_cnt = 0

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


    def make_dv_dict(self, dv_name):
        return dict( name=dv_name,\
                    alias=dv_name.replace(' ', '-').lower(),\
                    description='Store the datasets for %s' % dv_name,\
                    category='RESEARCH_PROJECTS',\
                    contact_email='%s@harvard.edu' % (dv_name.replace(' ', '-').lower()),\
                    )


    def make_dataverse_from_dict(self, flare_dict, depth):

        if flare_dict is None:
            return

        #if self.flare_cnt == 15:
        #    msgx('stopping')

        dataverse_name = flare_dict.get('name', None)
        if dataverse_name is None:
            return

        dv_dict = self.make_dv_dict(dataverse_name)
        self.flare_cnt+=1
        msg('(%s)%s(%s) make dataverse: [%s]' %  ( self.flare_cnt, '---|'*depth, depth, dataverse_name))
        make_dataverse(self.sdriver, dv_dict)
        pause_script()
        publish_dataverse(self.sdriver)
        pause_script()

        for child_flare_dict in flare_dict.get('children', []):
            self.make_dataverse_from_dict(child_flare_dict, depth=depth+1)

    def start_flare_process(self):

        flare_info = open(os.path.join('input','flare.json'), 'r').read()
        flare_dict = json.loads(flare_info)

        self.make_dataverse_from_dict(flare_dict, depth=0)



    def login(self):
        login_user(self.sdriver, self.dv_url, self.auth[0], self.auth[1])

        self.check_name()


def run_as_user(dataverse_url, auth, expected_name):

    tester = CreateDatasetTester(dataverse_url, auth, expected_name=expected_name)
    #tester.login()
    tester.start_flare_process()

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
    dataverse_url = 'https://dvn-build.hmdc.harvard.edu/'
    #dataverse_url = 'https://shibtest.dataverse.org'
    #dataverse_url = 'http://localhost:8080'


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


