from .base import SeleniumTestCase
# from movienite.models import Person


class MovieniteTest(SeleniumTestCase):

    def test_movienite(self):
        self.browser.get(self.live_server_url + '/accounts/login/')
        self.browser.find_element_by_name('username').send_keys('bar')
        self.browser.find_element_by_name('password').send_keys('foo')
        self.browser.find_element_by_css_selector('*[type=submit]').click()
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Log Out', text)
        # self.browser.get(self.live_server_url + '/movie_add/')
        # self.browser.find_element_by_name('title').send_keys('Hackers')
        # self.browser.find_element_by_class_name('select2-selection__arrow').click()
        # Person(name="George").save()
        # Person(name="Trey").save()
