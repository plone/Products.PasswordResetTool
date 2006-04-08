"""Support for using zope.testbrowser from Zope2.

Mostly just copy and paste from zope.testbrowser.testing.

BBB: Five 1.4 includes this module (``Five/testbrowser.py``).
"""

import urllib2

import mechanize
import ClientCookie

from zope.testbrowser import testing
from zope.testbrowser import browser
import zope.publisher.http


class PublisherConnection(testing.PublisherConnection):

    def __init__(self, host):
        from Testing.ZopeTestCase.zopedoctest.functional import http
        self.caller = http
        self.host = host

    def getresponse(self):
        """Return a ``urllib2`` compatible response.

        The goal of ths method is to convert the Zope Publisher's reseponse to
        a ``urllib2`` compatible response, which is also understood by
        mechanize.
        """
        real_response = self.response._response
        status = real_response.getStatus()
        reason = zope.publisher.http.status_reasons[real_response.status]

        headers = real_response.headers.items()
        headers.sort()
        headers.insert(0, ('Status', "%s %s" % (status, reason)))
        headers = '\r\n'.join('%s: %s' % h for h in headers)
        content = real_response.body
        return testing.PublisherResponse(content, headers, status, reason)


class PublisherHTTPHandler(urllib2.HTTPHandler):
    """Special HTTP handler to use the Zope Publisher."""

    http_request = urllib2.AbstractHTTPHandler.do_request_

    def http_open(self, req):
        """Open an HTTP connection having a ``urllib2`` request."""
        # Here we connect to the publisher.
        return self.do_open(PublisherConnection, req)


class PublisherMechanizeBrowser(mechanize.Browser):
    """Special ``mechanize`` browser using the Zope Publisher HTTP handler."""

    handler_classes = {
        # scheme handlers
        "http": PublisherHTTPHandler,

        "_http_error": ClientCookie.HTTPErrorProcessor,
        "_http_request_upgrade": ClientCookie.HTTPRequestUpgradeProcessor,
        "_http_default_error": urllib2.HTTPDefaultErrorHandler,

        # feature handlers
        "_authen": urllib2.HTTPBasicAuthHandler,
        "_redirect": ClientCookie.HTTPRedirectHandler,
        "_cookies": ClientCookie.HTTPCookieProcessor,
        "_refresh": ClientCookie.HTTPRefreshProcessor,
        "_referer": mechanize.Browser.handler_classes['_referer'],
        "_equiv": ClientCookie.HTTPEquivProcessor,
        "_seek": ClientCookie.SeekableProcessor,
        }

    default_schemes = ["http"]
    default_others = ["_http_error", "_http_request_upgrade",
                      "_http_default_error"]
    default_features = ["_authen", "_redirect", "_cookies", "_seek"]


class Browser(browser.Browser):
    """A Zope ``testbrowser` Browser that uses the Zope Publisher."""

    def __init__(self, url=None):
        mech_browser = PublisherMechanizeBrowser()
        # override the http handler class
        mech_browser.handler_classes["http"] = PublisherHTTPHandler
        super(Browser, self).__init__(url=url, mech_browser=mech_browser)
