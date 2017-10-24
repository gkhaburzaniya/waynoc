from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver


class SeleniumTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(StaticLiveServerTestCase, cls).setUpClass()
        User.objects.create_user(username='bar', password='foo')
        cls.browser = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(StaticLiveServerTestCase, cls).tearDownClass()
