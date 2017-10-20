from contextlib import contextmanager

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver


class SeleniumTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(StaticLiveServerTestCase, cls).setUpClass()
        cls.browser = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(StaticLiveServerTestCase, cls).tearDownClass()

    @contextmanager
    def wait_for_page_load(self, timeout=10):
        old_page = self.browser.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.browser, timeout).until(staleness_of(old_page))


class LoginTest(SeleniumTestCase):

    def test_successful_login(self):
        password = 'foo'
        user = User.objects.create_user(username='bar', password=password)
        self.browser.get(self.live_server_url + "/accounts/login/")
        self.browser.find_element_by_name('username').send_keys(user.username)
        self.browser.find_element_by_name('password').send_keys(password)
        with self.wait_for_page_load():
            self.browser.find_element_by_css_selector('*[type=submit]').click()
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Log Out', text)
