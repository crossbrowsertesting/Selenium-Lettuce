# Selenium Testing with Lettuce and Python

**[Lettuce](http://lettuce.it/)** is a [Behavior Driver Development](https://en.wikipedia.org/wiki/Behavior-driven_development) framework that allows you to execute automated Python tests from plain-text descriptions. This allows you to write tests that even your company's business people can understand.

You can even use **Lettuce** to run your tests with CrossBrowserTesting’s cloud testing platform. Let’s see how!

If you already have `lettuce-webdriver` scripts setup to work locally, changing them to work with our system is easy. You just have to change the `WebDriver` object to a `RemoteWebDriver` object, and supply it with capabilities that match up with the CrossBrowserTesting API. For example, you might create a Firefox WebDriver like this:

```
world.browser = webdriver.firefox()
```

And to run your test on crossbrowsertesting, you just have to change that line to this:

```
world.browser = webdriver.Remote(
        desired_capabilities = caps,
        command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub"%(username, authkey)
    )
```

Your `username` here will be the email address associated with your CBT account and your `authkey` can be found on the [Manage Account](https://crossbrowsertesting.com/account) section of CrossBrowserTesting.

-----

If you haven’t used Lettuce before, it's easy to get started. First let’s get the framework installed. You can do so quickly with PIP.

```
pip install lettuce
```

We’ll also need `lettuce-webdriver`

```
pip install lettuce-webdriver
```

-----

Alright, now we can get started. To run a test with Lettuce, you need at least three basic files:
* a `*.feature` file describing your tests using [Gherkin's](https://github.com/cucumber/cucumber/wiki/Gherkin) *Given-When-Then* syntax
* a `terrain.py` file containing your email, authkey, capabilities, and any other setup/teardown steps for your tests
* at least one `steps.py` file where test functions from your `*.feature` files are defined

Don't worry if any of that sounds confusing, We go over each step below. If you want to follow along with this example, you can find all the files we use on [our repository](https://github.com/crossbrowsertesting/Framework-Integrations/tree/master/Lettuce-Python/features)

----

Lettuce, like Ruby's *Cucumber* framework, uses Gherkin to translate plain English descriptions of how an application should behave into automated functional tests. You should have a different `*.feature` file for each different feature your are testing. The filename doesn't matter (since Lettuce loads all `*.feature` files it finds), but you should make it descriptive. In this example we'll be testing a login form, so let's call the file `login.feature`.

Example `login.feature`

```
Feature: Test the features of our Login Form

Scenario: Test Login Form
  Given I go to "http://crossbrowsertesting.github.io/login-form.html"
    The title of the page should become "Login Form - CrossBrowserTesting.com"
    And when I fill in "username" with "tester@crossbrowsertesting.com"
    And when I fill in "password" with "test123"
    When I press "Login"
    I should see "You are now logged in!" within 10 seconds
    Then the browser should close
```

As you’ll see, Lettuce reads quoted input from these instructions to use with correlating Python methods. These Python methods will be setup in a file called steps.py.

Example `steps.py`

```python
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
```

As you now see, our Python methods pull input from the Gherkin story by using the @step decorator. In this example, we confirm the title of the page, enter a username/password, then hit submit. Finally we ensure that the text “You are now logged in” can be located within the page to verify that our login was successful.

Lastly, we need to ensure that our tests are pointed to CBT! Lettuce uses python to instantiate a RemoteWebDriver, we just need to make sure its pointed at our hub and uses our API names to pick out a OS/Browser configuration.

Example terrain.py

```python
from lettuce import *
from selenium import webdriver
import lettuce_webdriver.webdriver

username = ‘you@yourdomain.com'  # make sure to change this to your username
authkey = ‘12345'                                # make sure to change this to your authkey

@before.all
def setUp():
    caps = {}
    caps['name'] = 'First Lettuce Test'
    caps['build'] = '1.0'
    caps['browser_api_name'] = 'ff-latest'          # request the latest version of firefox
    caps['os_api_name'] = 'Win7x64'
    caps['screen_resolution'] = '1024x768'
    caps['record_video'] = 'true'
    caps['record_network'] = 'true'

    world.browser = webdriver.Remote(
        desired_capabilities = caps,
        command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub"%(username, authkey)
    )

def tearDown():
    world.browser.quit()

```

Now we lettuce. Within your terminal navigate to the parent of your features directory and run the `lettuce` command. Go to the [Selenium dashboard](https://app.crossbrowsertesting.com/selenium/run) on our site, and watch your test in action. From the terminal you can watch your test run, and eventually pass:

```
user$ lettuce

Feature: Test the features of our Login Form

  Scenario: Test Login Form                 
    Given I go to "http://crossbrowsertesting.github.io/login-form.html"
    The title of the page should become "Login Form - CrossBrowserTesting.com"
    And when I fill in "username" with "tester@crossbrowsertesting.com"       
    And when I fill in "password" with "test123"                              
    When I press "Login"                                                      
    I should see "You are now logged in!" within 10 seconds                   
    Then the browser should close

1 feature (1 passed)
1 scenario (1 passed)
7 steps (7 passed)


Give it a shot with your webpage! See just how powerful Selenium is, and how easy it is to write by using the Lettuce framework. If you have any questions or trouble getting your tests working with us, don’t hesitate to get in touch.
