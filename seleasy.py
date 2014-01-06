class Seleasy(object):

    def __init__(self, driver):
        self._driver = driver

    def __call__(self, selector='a, button', content=None):
        elements = self._driver.find_elements_by_css_selector(selector)
        if content is not None:
            elements = filter(self._content_filter(content), elements)
        return SmartElementSet(elements)

    def _content_filter(self, content):
        def filter(element):
            return element.text.strip() == content
        return filter


class SmartElementSet(object):

    def __init__(self, elements):
        self._elements = elements

    def __getattr__(self, name):
        return getattr(self._elements[0], name)

    def __len__(self):
        return len(self._elements)

    def __getitem__(self, index):
        return self._elements[index]
