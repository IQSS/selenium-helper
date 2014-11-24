from selenium_helper import SeleniumHelper
from msg_util import *
from random import randint
from collections import OrderedDict
import requests
from selenium_dataverse_specs import DataverseInfoChecker
from datetime import datetime
import time
import os



def pause_script(num_seconds=3):
    """
    Pause for 'num_seconds' seconds
    """
    msg('\n...Pausing for for %s second(s)...' % num_seconds)
    time.sleep(num_seconds)

def login_user(selenium_helper, dataverse_url, user_name, user_credentials):
    msgt('login')
    assert isinstance(selenium_helper, SeleniumHelper), "selenium_helper must be a SeleniumHelper object"
    assert dataverse_url is not None, "dataverse_url cannot be None"
    assert user_name is not None, "user_name cannot be None"
    assert user_credentials is not None, "user_name cannot be None"

    selenium_helper.get(dataverse_url)

    msg('click login')
    selenium_helper.find_link_by_text_click('Log In')

    msg('fill in user_name/user_credentials click login')
    # login
    selenium_helper.find_by_id_send_keys('loginForm:credentialsContainer2:0:credValue', user_name)
    selenium_helper.find_by_id_send_keys('loginForm:credentialsContainer2:1:sCredValue', user_credentials)
    selenium_helper.find_by_id_click('loginForm:login')
    pause_script()


def logout_user(selenium_helper):
    msgt('Log out')
    assert isinstance(selenium_helper, SeleniumHelper), "selenium_helper must be a SeleniumHelper object"

    # click account dropdown menu
    #
    if selenium_helper.find_by_css_selector_and_click("a[id$='lnk_header_account_dropdown']"):
        #
        # click logout
        #
        selenium_helper.find_by_css_selector_and_click("a[id$='lnk_header_logout']")


def goto_home(selenium_helper):
    """
    Go to the home page
    """
    assert isinstance(selenium_helper, SeleniumHelper), "selenium_helper must be a SeleniumHelper object"
    selenium_helper.goto_link('/')


def goto_dataverse_user_page(selenium_helper):
    """
    Go to the page dataverseuser.xhtml
    """
    assert isinstance(selenium_helper, SeleniumHelper), "selenium_helper must be a SeleniumHelper object"
    selenium_helper.goto_link('/dataverseuser.xhtml')


def has_expected_name(selenium_helper, expected_name):
    """
    Look for the logged in name in the upper right corner of the screen
    """
    assert  isinstance(selenium_helper, SeleniumHelper), "selenium_helper must be a SeleniumHelper object"

    page_source = selenium_helper.get_page_source()
    search_str = '">%s' %  (expected_name)
    msgt('check for: [%s]' % search_str)
    if page_source.find(search_str) == -1:
        msg('!' * 200)
        msg('Not logged in as: %s' % expected_name)
        msg('May also be a 500 error')

        thetime = time.time()
        fname = 'not_logged_in-%s.html' % datetime.fromtimestamp(\
                                                    thetime\
                                            ).strftime("%Y-%m-%d_%H%M-%S")
        fname = os.path.join('bad_html_pages', fname)
        open(fname, 'w').write(page_source.encode('utf-8'))
        msgt('Bad html file written: %s' % fname)
        msgt('pause for 5 minutes!')
        pause_script(60*5)
    else:
        msg('Still logged in as: %s' % expected_name)
    return True

def make_dataverse(selenium_helper, dv_info):
    """
    dv_info example
    dv_info = dict( name='Elevation',\
                    alias='elevation',\
                    description='Elevation Tour Live Slane Castle,Ireland.. September 1 2001',\
                    category='RESEARCH_PROJECTS',\
                    contact_email='harvie@mudd.edu',\
                    )

    """
    assert  isinstance(selenium_helper, SeleniumHelper), "selenium_helper must be a SeleniumHelper object"

    DataverseInfoChecker.is_valid_dataverse_info(dv_info)

    sh = selenium_helper
    sh.find_link_in_soup_and_click('New Dataverse')
    pause_script()

    # name
    sh.find_by_id_send_keys('dataverseForm:name', dv_info['name'])

    # alias
    sh.find_by_id_send_keys('dataverseForm:alias', dv_info['alias'])

    # contact email
    if dv_info.has_key('contact_email'):
        sh.find_by_id_send_keys('dataverseForm:contactEmail', dv_info['contact_email'])


    # description
    sh.find_by_id_send_keys('dataverseForm:description', dv_info['description'])

    # category
    sh.find_by_id_send_keys('dataverseForm:dataverseCategory', dv_info['category'], clear_existing_val=False)

    # save
    sh.find_by_id_click('dataverseForm:save')

    # pause
    pause_script()









