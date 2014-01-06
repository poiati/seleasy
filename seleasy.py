class NoElementsError(Exception):

    def __init__(self, selector):
        msg = "Can not find any element for selector '%s'" % selector
        super(NoElementsError, self).__init__(msg)


class Seleasy(object):

    def __init__(self, driver):
        self._driver = driver

    def __call__(self, selector='a, button', content=None):
        elements = self._driver.find_elements_by_css_selector(selector)
        if content is not None:
            elements = filter(self._content_filter(content), elements)
        return SmartElementSet(selector, elements)

    def _content_filter(self, content):
        return lambda element: element.text.strip() == content


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
