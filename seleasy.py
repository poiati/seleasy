class NoElementsError(Exception):

    def __init__(self, selector):
        msg = "Can not find any element for selector '%s'" % selector
        super(NoElementsError, self).__init__(msg)


class Seleasy(object):

    def __init__(self, driver):
        self._driver = driver

    def fill(self, name, value):
        self._driver.find_element_by_name(name).send_keys(value)

    def click(self, text):
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
