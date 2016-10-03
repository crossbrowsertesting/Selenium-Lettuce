from lettuce import *
from lettuce_webdriver.util import assert_true
from lettuce_webdriver.util import AssertContextManager
from lettuce import step

@step(u'The title of the page should become "([^"]*)"')
def the_title_of_the_page_should_become(step, result):
    title = world.browser.title
    try: 
        assert_true(step, title == result)
    except AssertionError as e:
        world.browser.quit()

@step(u'when I fill in "([^"]*)" with "([^"]*)"')
def when_i_fill_in(step, locator, username):
    try: 
        world.browser.find_element_by_name(locator).sendkeys(username)
    except AssertionError as e:
        world.browser.quit()

@step(u'When I click "([^"]*)"')
def when_i_press(step, locator):
    try: 
        world.browser.find_element_by_link_text(locator).click()
    except AssertionError as e:
        world.browser.quit()

@step(u'the browser should close')
def browser_should_close(step):
    world.browser.quit()
