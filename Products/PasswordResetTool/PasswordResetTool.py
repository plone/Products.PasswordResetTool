"""PasswordResetTool.py

Mailback password reset product for CMF.
Author: J Cameron Cooper, Sept 2003
"""

from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
from OFS.SimpleItem import SimpleItem
from Globals import InitializeClass, DTMLFile
from AccessControl import ClassSecurityInfo
from Products.CMFCore.CMFCorePermissions import View, ManagePortal
#from Products.CMFCore.ActionProviderBase import ActionProviderBase

from interfaces.portal_password_reset import portal_password_reset as IPWResetTool

import time, random, md5, socket
from DateTime import DateTime
try:
    import datetime
except ImportError:
    pass # no Python 2.3. Pity.

class PasswordResetTool (UniqueObject, SimpleItem):
    """Provides a default implementation for a password reset scheme.

    From a 'forgotten password' template, you submit your username to
    a handler script that does a 'requestReset', and sends an email
    with an unguessable unique hash in a url as built by 'constructURL'
    to the user.

    The user visits that URL (the 'reset form') and enters their username,
    """
    
    ## other things needed for this to work
    # skins:
    #  - handler script for forgotten password form (probably over-riding existing Plone one
    #  - email template
    #  - password reset form
    #  - password reset form handler script

    ## Tool/CMF/Zope machinery

    # The latter will work only with Plone 1.1 => hence, the if
    #if hasattr(ActionProviderBase, '__implements__'):
    #    __implements__ = (IPWResetTool, ActionProviderBase.__implements__)
    __implements__ = (IPWResetTool)

    id = 'portal_password_reset'
    meta_type = 'Password Reset Tool'
    #_actions = ()

    security = ClassSecurityInfo()

    manage_options=(( { 'label' : 'Overview'
                        , 'action' : 'manage_overview'
                        },
                      ) + SimpleItem.manage_options
                    )

    ##   ZMI methods
    security.declareProtected(ManagePortal, 'manage_overview')
    manage_overview = DTMLFile('dtml/explainPWResetTool', globals() )

    security.declareProtected(ManagePortal, 'manage_setTimeout')
    def manage_setTimeout(self, hours=24, REQUEST=None):
    	"""ZMI method for setting the expiration timeout in hours."""
	self.setExpirationTimeout(hours)
        return self.manage_overview(manage_tabs_message="Timeout set to %s hours" % hours)   

    security.declareProtected(ManagePortal, 'manage_toggleUserCheck')
    def manage_toggleUserCheck(self, REQUEST=None):
    	"""ZMI method for toggling the flag for checking user names on return."""
	self.toggleUserCheck()
        m = self.checkUser() and 'on' or 'off'
        return self.manage_overview(manage_tabs_message="Returning username check turned" % m)

    ## Internal attributes
    _user_check = 1
    _requests = {}
    _timedelta = 24

    ## Interface fulfillment ##
    security.declarePublic('requestReset')
    def requestReset(self, userid):
        """Ask the system to start the password reset procedure for
        user 'userid'.

        Returns a dictionary with the random string that must be
        used to reset the password in 'randomstring', the expiration date
        as a DateTime in 'expires', and the userid (for convenience) in
        'userid'. Returns None if no such user."""
        if not self.getValidUser(userid):
            return None
        randomstring = self.uniqueString(userid)
        expiry = self.expirationDate()
        self._requests[randomstring] = (userid, expiry)
        self._p_changed = 1
        
        retval = {}
        retval['randomstring'] = randomstring
        retval['expires'] = expiry
        retval['userid'] = userid
        return retval

    security.declarePublic('resetPassword')
    def resetPassword(self, userid, randomstring, password):
        """Set the password (in 'password') for the user who maps to
        the string in 'randomstring' iff the entered 'userid' is equal
        to the mapped userid. (This can be turned off with the
        'toggleUserCheck' method.)

        Note that this method will *not* check password validity: this
        must be done by the caller.

        Throws an 'ExpiredRequestError' if request is expired.
        Throws an 'InvalidRequestError' if no such record exists,
        or 'userid' is not in the record.
        """
        try:
            stored_user, expiry = self._requests[randomstring]
        except KeyError:
            raise 'InvalidRequestError'
        
        if self.checkUser() and (userid != stored_user):
            raise 'InvalidRequestError'
        if self.expired(expiry):
            del self._requests[randomstring]
            raise 'ExpiredRequestError'

        member = self.getValidUser(userid)
        if not member:
            raise 'InvalidRequestError'

        # actually change password
        user = member.getUser()
        try:
            # this is a GRUF special case, but I don't feel bad, because
            # the regular Zope user object should be so lucky as to have this call
            user.changePassword(password)
        except AttributeError:
            # this sets __ directly (via MemberDataTool) which is the usual
            # (and stupid!) way to change a password in Zope
            member.setSecurityProfile(password=password)

        # clean out the request
        del self._requests[randomstring]
        

    ## Implementation ##

    # external

    security.declareProtected(ManagePortal, 'setExpirationTimeout')
    def setExpirationTimeout(self, timedelta):
        """Set the length of time a reset request will be valid.

        Takes a 'datetime.timedelta' object (if available, since it's
        new in Python 2.3) or a number of hours, possibly
        fractional. Since a negative delta makes no sense, the
        timedelta's absolute value will be used."""
        self._timedelta = abs(timedelta)

    security.declarePublic('getExpirationTimeout')
    def getExpirationTimeout(self):
        """Get the length of time a reset request will be valid.

        In hours, possibly fractional. Ignores seconds and shorter."""
        try:
            if isinstance(self._timedelta,datetime.timedelta):
                return self._timedelta.days / 24
        except NameError:
            pass  # that's okay, it must be a number of hours...
        return self._timedelta

    security.declareProtected(ManagePortal, 'clearExpired')
    def clearExpired(self):
        """Destroys all expired reset request records."""
        pass

    security.declareProtected(ManagePortal, 'toggleUserCheck')
    def toggleUserCheck(self):
        """Changes whether or not the tool requires someone to give the uerid
        they're trying to change on a 'password reset' page. Highly recommended
        to LEAVE THIS ON."""
        if not hasattr(self, '_user_check'):
            self._user_check = 1

        self._user_check = not self._user_check
        
    security.declarePublic('checkUser')
    def checkUser(self):
        """Returns a boolean representing the state of 'user check' as described
        in 'toggleUserCheck'. True means on, and is the default."""
        if not hasattr(self, '_user_check'):
            self._user_check = 1

        return self._user_check

    # customization points

    security.declarePrivate('uniqueString')
    def uniqueString(self, userid):
        """Returns a string that is random and unguessable, or at
        least as close as possible.

        This is used by 'requestReset' to generate the auth
        string. Override if you wish different format.

        This implementation ignores userid and simply generates a
        UUID. That parameter is for convenience of extenders, and
        will be passed properly in the default implementation."""
        # this is the informal UUID algorithm of
        # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/213761
        # by Carl Free Jr
        t = long( time.time() * 1000 )
        r = long( random.random()*100000000000000000L )
        try:
            a = socket.gethostbyname( socket.gethostname() )
        except:
            # if we can't get a network address, just imagine one
            a = random.random()*100000000000000000L
        data = str(t)+' '+str(r)+' '+str(a)#+' '+str(args)
        data = md5.md5(data).hexdigest()
        return str(data)

    security.declarePrivate('expirationDate')
    def expirationDate(self):
        """Returns a DateTime for exipiry of a request from the
        current time.

        This is used by housekeeping methods (like clearEpired)
        and stored in reset request records."""
        if not hasattr(self, '_timedelta'):
            self._timedelta = 24
        try:
            if isinstance(self._timedelta,datetime.timedelta):
                expire = datetime.datetime.utcnow() + self._timedelta
                return DateTime(expire.year,
                                expire.month,
                                expire.day,
                                expire.hour,
                                expire.minute,
                                expire.second,
                                'UTC')
        except NameError:
            pass  # that's okay, it must be a number of hours...
        expire = time.time() + self._timedelta*3600  # 60 min/hr * 60 sec/min
        return DateTime(expire)

    security.declarePrivate('getValidUser')
    def getValidUser(self, userid):
        """Returns the member with 'userid' if available and None otherwise."""
        membertool = getToolByName(self, 'portal_membership')
        return membertool.getMemberById(userid)
    
    # internal

    security.declarePrivate('expired')
    def expired(self, datetime, now=None):
        """Tells whether a DateTime or timestamp 'datetime' is expired
        with regards to either 'now', if provided, or the current
        time."""
        if not now:
            now = DateTime()
        return now.greaterThanEqualTo(datetime)

# these are possible customization points I'm not really sure we need.
#
#    def getRequestRecord(self, randomstring):
#        """Returns a tuple (userid,expiration) that maps to a specific
#        reset request, as keyed by the 'randomstring'.
#
#        Expiration is a DateTime."""
#
#    def setRequestRecord(self, randomstring, userid, expiry):
#        """Create a reset request record keyed by 'randomstring'
#        containing 'userid' and 'expiry' (which should be a DateTime)."""
#
#    def removeRequestRecord(self, randomstring):
#        """Destroy the request reset record keyed by 'randomstring'."""
#
#    def getAllRequests(self):
#        """Returns a list of all reset requests in a tuple
#        '(randomstring, userid, expiry)'.
#
#        Used primarily for housekeeping. Expiry is a DateTime."""

    # def # bobo_traverse_override to get URL as above

InitializeClass(PasswordResetTool)
