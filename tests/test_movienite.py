from selenium.webdriver.common.keys import Keys

from .base import SeleniumTestCase

from movienite.models import Person


class MovieniteTest(SeleniumTestCase):

    def test_movienite(self):
        Person(name='Trey').save()
        self.browser.get(self.live_server_url + '/movie_add/')
        self.browser.find_element_by_name('title').send_keys('Hackers')
        self.browser.find_element_by_xpath(
            '/html/body/div/form/p[4]/span'
        ).click()
        self.browser.switch_to.active_element.send_keys(Keys.ENTER + 'George' + Keys.ENTER)
        self.browser.find_element_by_css_selector('*[type=submit]').click()
        # self.assertTrue()
