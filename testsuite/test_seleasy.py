import os
import sys
import unittest

from selenium.webdriver import Firefox
from expecter import expect
from mock import Mock


path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path, '..'))

from seleasy import Seleasy, SmartElementSet


WEBSERVER_ADDRESS = 'http://127.0.0.1:5000/'


class SeleasyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Firefox()
        cls.seleasy = Seleasy(cls.browser)
        super(SeleasyTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SeleasyTest, cls).tearDownClass()

    def test_assert_title_selenium(self):
        self.get('/')

        expect(self.browser.title) == 'Seleasy Test Site'

    def test_click_in_link_selenium(self):
        self.get('/')

        self.browser.find_element_by_css_selector('a').click()

        expect(self.browser.page_source).contains('Menu Link Clicked')

    def test_click_in_link(self):
        self.get('/')

        self.seleasy('a').click()

    def test_click_in_link_using_index(self):
        self.get('/')

        self.seleasy('a')[0].click()

    def test_element_not_found_not_throw_error(self):
        expect(len(self.seleasy('a.notfound'))) == 0

    @unittest.skip('implement later')
    def test_call_action_in_an_empty_set(self):
        with expect.raises(StandardError):
            self.seleasy('a.notfound').click()

    def test_click_link_with_content(self):
        self.get('/')

        self.seleasy(content='Menu Link 1').click()

    def test_click_button_with_content(self):
        self.get('/')

        self.seleasy(content='Click me!').click()

        button = self.browser.find_element_by_id('click-me-button')

        expect(button.text) == 'Clicked!'

    @unittest.skip('need to match content with attribute value')
    def test_click_input_type_button_with_content(self):
        self.get('/')

        self.seleasy(content='Click me too!').click()

        button = self.browser.find_element_by_id('click-me-input')

        expect(button.text) == 'Clicked too!'

    def get(self, uri):
        self.browser.get('%s%s' % (WEBSERVER_ADDRESS, uri))


class SmartElementSetTest(unittest.TestCase):

    def setUp(self):
        self.element1 = Mock()
        self.element2 = Mock()
        self.element3 = Mock()

        self.elements = [self.element1, self.element2, self.element3]

        self.smartset = SmartElementSet(self.elements)

    def test_always_delegate_calls_to_first_element(self):
        self.smartset.click()

        self.element1.click.assert_called_with()

    def test_length(self):
        expect(len(self.smartset)) == 3

    def test_indexing(self):
        expect(self.smartset[0]) == self.element1
        expect(self.smartset[1]) == self.element2
        expect(self.smartset[2]) == self.element3


if __name__ == '__main__':
    unittest.main()
