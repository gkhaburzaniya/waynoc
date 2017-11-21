from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver


class SeleniumTestCase(StaticLiveServerTestCase):

    browser = WebDriver()

    def setUp(self):
        User.objects.create_user(username='bar', password='foo')
        self.browser.get(self.live_server_url + '/accounts/login/')
        self.browser.find_element_by_name('username').send_keys('bar')
        self.browser.find_element_by_name('password').send_keys('foo')
        self.browser.find_element_by_css_selector('*[type=submit]').click()
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Log Out', text)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(StaticLiveServerTestCase, cls).tearDownClass()
