Feature: Test a login form

Scenario: Test Login
  Given I go to "http://crossbrowsertesting.github.io/login-form.html"
    The title of the page should become "Login Form - CrossBrowserTesting.com"
    And when I fill in "username" with "tester@crossbrowsertesting.com"
    And when I fill in "password" with "test123"
    When I press "Login" 
    I should see "You are now logged in!" within 10 seconds
    Then the browser should close
