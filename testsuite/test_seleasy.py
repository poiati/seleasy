from unittest import TestCase

from selenium.webdriver import Firefox


class SeleasyTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Firefox()
        super(SeleasyTest, self).setUp()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SeleasyTest, self).tearDown()

    def test_find_click_in_a_link(self):
        self.browser.get('http://www.google.com')
