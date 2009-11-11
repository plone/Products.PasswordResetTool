from Products.MailHost.MailHost import MailHost as MailBase
from Products.MailHost.MailHost import _mungeHeaders
from persistent.list import PersistentList


# copied from Products.CMFPlone.tests.utils

class MockMailHost(MailBase):
    """A MailHost that collects messages instead of sending them.
    """

    def __init__(self, id):
        self.reset()

    def reset(self):
        self.messages = PersistentList()

    def send(self, messageText, mto=None, mfrom=None, subject=None,
             encode=None, immediate=False, charset=None, msg_type=None):
        messageText, mto, mfrom = _mungeHeaders(messageText,
                                                mto, mfrom, subject,
                                                charset=charset,
                                                msg_type=msg_type)
        self.messages.append(messageText)

