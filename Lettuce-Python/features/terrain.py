
from lettuce import *
from selenium import webdriver
import lettuce_webdriver.webdriver


username = 'you@yourdomain.com'
authkey = '12345'


@before.all
def setUp():
    caps = {}
    caps['name'] = 'First Lettuce Test'
    caps['build'] = '1.0'
    caps['browser_api_name'] = 'IE10'
    caps['os_api_name'] = 'Win7x64-C2'
    caps['screen_resolution'] = '1024x768'
    caps['record_video'] = 'true'
    caps['record_network'] = 'true'

    world.browser = webdriver.Remote(
        desired_capabilities = caps,
        command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub"%(username, authkey)
    )

def tearDown():
    world.browser.quit()
