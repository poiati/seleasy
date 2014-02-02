"""
Seleasy is an alternative to the classic python Selenium API. The main advantage
of it is a clear and less verbose inteface.
"""


__version__ = '0.1.0'
__author__ = 'Paulo Poiati'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Paulo Poiati'


class NoElementsError(Exception):

    def __init__(self, selector):
        msg = "Can not find any element for selector '%s'" % selector
        super(NoElementsError, self).__init__(msg)


class Seleasy(object):
    """
    Main interface of seleasy. 

    :param driver: A selenium WebDriver instance, for example: 
    selenium.webdriver.Firefox

    Instances of this class are callable and
    can be used to query for elements in the document using css selectors.

    >>> table = seleasy('.clients-tables')
    >>> assert 'Peter Parker' in table.text

    You can call selenium methods at the matching elements.

    >>> seleasy('button#send-form').click()

    If the css selector match more than one element the underlying action will 
    go to the first element of the matches.

    >>> seleasy('form input[type=text]').send_keys('Fill the first input element of the form')

    """

    def __init__(self, driver):
        self._driver = driver

    def fill(self, name, value):
        """
        Fill a form input.

        :param name: The input name
        :param value: The input new value

        >>> seleasy.fill('name', 'Peter Parker')
        >>> seleasy.fill('password', 'spiderweb')
        """
        self._driver.find_element_by_name(name).send_keys(value)

    def click(self, text):
        """
        Click in a button that contains text.

        :param text: The button text

        >>> seleasy.click('Submit')
        """
        self(text=text).click()

    def __call__(self, selector='a, button, input', text=None):
        elements = self._driver.find_elements_by_css_selector(selector)
        if text is not None:
            elements = filter(self._text_filter(text), elements)
        return SmartElementSet(selector, elements)

    def _text_filter(self, text):
        def fn(element):
            element_text = element.get_attribute('value') or element.text
            return element_text.strip() == text
        return fn


class SmartElementSet(object):

    def __init__(self, selector, elements):
        self._selector = selector
        self._elements = elements

    def __getattr__(self, name):
        try:
            return getattr(self._elements[0], name)
        except IndexError:
            raise NoElementsError(self._selector)

    def __len__(self):
        return len(self._elements)

    def __getitem__(self, index):
        return self._elements[index]
