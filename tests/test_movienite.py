from datetime import date

from selenium.webdriver.common.keys import Keys

from movienite.models import Person, Movie
from .base import SeleniumTestCase


class MovieniteTest(SeleniumTestCase):

    def test_add_person(self):
        Person(name='Trey').save()
        self.browser.get(self.live_server_url + '/movie_add/')
        self.browser.find_element_by_name('title').send_keys('Hackers')
        self.browser.find_element_by_css_selector('*[id=id_attendees] + span').click()
        self.browser.switch_to.active_element.send_keys(Keys.ENTER + 'George' + Keys.ENTER)
        self.browser.find_element_by_css_selector('*[type=submit]').click()
        self.assertTrue(Person.objects.get(name='George'))

    def test_remove_attendee(self):
        trey = Person.objects.create(name='Trey')
        george = Person.objects.create(name='George')
        m1 = Movie.objects.create(id=1, title='Hackers', picker=trey, date=date.today())
        m1.attendees.set([trey, george])
        m2 = Movie.objects.create(id=2, title='Tremors', picker=george, date=date.today())
        m2.attendees.set([trey, george])
        self.browser.get(self.live_server_url + '/movie_edit/1/')
        self.browser.find_element_by_css_selector('*[title=George]>span').click()
        self.browser.find_element_by_name('title').click()
        self.browser.find_element_by_css_selector('*[type=submit]').click()
        self.assertTrue(
            Person.objects.get(name='Trey').score > Person.objects.get(name='George').score
        )
