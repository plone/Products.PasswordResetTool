# XXX For the time being, we have to do this ugly monkey-patch, or
# else we'll encounter problems with links that have leading
# whitespace, e.g. 'href=" index.html"'.  I expect this to be fixed in
# mechanize soon.

from mechanize import _mechanize    
original_link_class = _mechanize.Link

class StrippingLink(original_link_class):
    def __init__(self, base_url, url, text, tag, attrs):
        url = url.strip()
        original_link_class.__init__(self, base_url, url, text, tag, attrs)

def monkeyMechanize():
    _mechanize.Link = StrippingLink

def unmonkeyMechanize():
    _mechanize.Link = original_link_class

