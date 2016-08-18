Changelog
=========

2.2.3 (2016-08-18)
------------------

Bug fixes:

- Use zope.interface decorator.
  [gforcada]


2.2.2 (2016-06-27)
------------------

Bug fixes:

- Remove unused attribute access of ``fullname`` (whereas it should have been access via ``getProperty``) on a PlonePAS MemberData object in ``mail_password_template.pt``, which lead to attribute access errors.
  [thet]


2.2.1 (2015-09-12)
------------------

- Pull email_from_name from configuration registry.
  [esteele]


2.2.0 (2015-07-18)
------------------

- Fix getting email from address.
  [vangheem]


2.1.2 (2015-03-26)
------------------

- Set mail Content-Type within registration and password reset email
  templates (rather than HTTP response headers which are ignored).
  [davidjb]

- Read ``use_email_as_login`` setting from the registry instead of portal
  properties (see https://github.com/plone/Products.CMFPlone/issues/216).
  [jcerjak]

- Amend browser.txt test to the new p.a.registry-based control panels
  (Plone 5 only).
  [timo]

- Move tests to plone.app.testing.
  [tomgross]

- Added userid information in reset mail (useful when the administrator
  resets a user password)
  [sgeulette]


2.1.1 (2014-10-22)
------------------

- Fix i18n of 'This field is required' for the login field in pwreset form.
  [vincentfretin]

- Ported tests to plone.app.testing
  [tomgross]


2.1.0 (2014-02-26)
------------------

- Barceloneta Plone 5 theme test fix.
  [davisagli]


2.0.16 (2014-01-27)
-------------------

- Password reset emails will now be sent from the navigation root instead
  the portal, enabling support for multilingual sites and other subsites
  to keep the correct language, title, menus and designs.
  [regebro]


2.0.15 (2013-08-13)
-------------------

- Nothing changed yet.


2.0.14 (2013-05-23)
-------------------

- Always try to look up what the user entered as a login name before
  treating it as a user id.
  [davisagli]

- Make sure password reset form action url is based on the reset tool and not
  the "passwordreset" python script. Fixes issue where the "passwordreset"
  was executed before the pwreset_form action handler was traversed to and
  caused an error before the reset request could even be attempted.
  [vangheem]


2.0.13 (2013-03-17)
-------------------

- Fix exception when use_email_as_login is on and the user enters
  an invalid login on pwreset_form.
  [davisagli]


2.0.12 (2013-03-05)
-------------------

- Fixed typo in registered_notify_template.pt: capitalization of sentence start.


2.0.11 (2013-01-13)
-------------------

- Fixed undefined django_crypto.
  [maurits]


2.0.10 (2012-12-09)
-------------------

- Use system random when available. This is part of the fix for
  https://plone.org/products/plone/security/advisories/20121106/24
  [davisagli]

- registered_notify_template.pt: show login name instead of user id.
  Normally this is the same, but this is not necessarily true when
  using the email address as login name.
  [maurits]


2.0.9 (2012-08-30)
------------------

- Changed deprecated getSiteEncoding to hardcoded `utf-8`
  [tom_gross]


2.0.8 (2012-05-25)
------------------

- Be less sensitive for white space differences in tests.
  [maurits]


2.0.7 (2011-11-24)
------------------

- getExpirationTimeout() now returns the correct number of hours, and not a value 24*24 times too low.
  (The code was never used though, since _timedelta does currently not store a timedelta but an int.)
  [kleist]


2.0.6 - 2011-06-02
------------------

- Apply patch to prevent exploitation of CVE-2011-1948 (Hotfix 20110531.)
  [elro]

- Fix edge case where member.fullname returns None instead of a string (ZMI
  or emergency user resets)
  [eleddy]

2.0.5 - 2011-01-03
------------------

- Depend on ``Products.CMFPlone`` instead of ``Plone``.
  [elro]

- URL for login form is now '/login' instead of 'login_form', adjust tests
  accordingly.
  [esteele]

2.0.4 - 2010-11-23
------------------

- Fallback import to work with Plone 3.
  [elro]

2.0.3 - 2010-09-20
------------------

- Fix the fix to http://dev.plone.org/plone/ticket/11136.
  [davisagli]

- Fix string exceptions in pwreset_action.cpy
  [davisagli]

2.0.2 - 2010-09-17
------------------

- Fix userid/login mixup which made it impossible to reset the password
  in environments where userid and login name are not equal. This fixes
  `Plone ticket 1136 <http://dev.plone.org/plone/ticket/11136>`_.
  [wichert]

2.0.1 - 2010-07-31
------------------

- Added line feed after the reset_url in mail_password_template.
  It was impossible to reset the password by clicking the url because
  there was "(This" at the end.
  [vincentfretin]

2.0 - 2010-07-18
----------------

- Updated markup of password reset form. This closes
  http://dev.plone.org/plone/ticket/10768.
  [hannosch]

2.0b7 - 2010-03-03
------------------

- Avoid test failures caused by access to hardcoded temp directories.
  [hannosch]

2.0b6 - 2010-02-18
------------------

- Allow imports of PasswordResetTool exceptions from restricted Python.
  [esteele]

- Updated templates to recent markup conventions.
  References http://dev.plone.org/old/plone/ticket/9981
  [spliter]

- Convert the string exceptions into class exceptions, since string
  ones don't work in Python 2.6.
  Fixes http://dev.plone.org/plone/ticket/9743
  [dukebody]

- Changed registration email to not rely on the request to hold the full name;
  instead the new member object is queried.
  [mj]

2.0b5 - 2010-01-28
------------------

- Changed mail_password_template.pt to the one proposed by limi:

    The following link will take you to a page where you can reset your
    password for XYZsite:

    http://example.com/resetpassword/c635bf8d892f4f30dd868d16c1
    (This link is valid for X days)

    If you didn't expect to receive this email, please ignore it.
    Your password has not been changed.

  This close ticket
  http://dev.plone.org/plone/ticket/8694
  [amleczko]

- The activation email no longer enumerates the hours before expiry, but gives a
  date/time instead. This fixes http://dev.plone.org/plone/ticket/9116.
  [limi]

2.0b4 - 2009-12-27
------------------

- Fixed package dependencies.
  [hannosch]

2.0b3 - 2009-12-16
------------------

- Fixed failing test after recent plone.app.users change: we never
  send the password in the email, only a link to set the password.
  [maurits]

2.0b2 - 2009-12-03
------------------

- Put a new line before greetings in registered_notify_template.pt
  [vincentfretin]

2.0b1 - 2009-12-02
------------------

- Make adjustments to fit with Plone 4's new @@register and @@new-user.
  [maurits]

- Fix issue where subject headers got double-encoded.
  [davisagli]

2.0a1 - 2009-11-15
------------------

- Properly encode mail headers (From and Subject). Fixes #8070
  [naro]

- When the new (Plone 4) property use_email_as_login is present and is
  True, we try to get the member by login name when userid gives no
  results. Refs http://dev.plone.org/plone/ticket/9214.
  [maurits]

- Avoid acquiring `portal_properties` and call it via a proper API.
  [hannosch]

- Converted installation code to a GenericSetup profile.
  [hannosch]

- Cleaned up package metadata and general codebase.
  [hannosch]

- Declare package dependencies, fixed deprecation warnings for use of
  Globals and fixed deprecation warnings for the md5 module.
  [hannosch]

1.2 - 2009-05-16
----------------

- Cleanup package metadata and add it to the egg description.
  [wichert]

- Internationalized dates in mail_password_template
  [vincentfretin]

- Removed duplicate DOCTYPE definition from mail_password_form.
  [limi]

- Adjusted browser tests to no longer rely on the login portlet.
  [hannosch]

- Catch RunTimeError when changing a password fails. Fixes #5742.
  [maurits]

- Added i18n domain for the userid label in the password reset form.
  [markvl]

- Purged old Zope 2 Interface interfaces for Zope 2.12 compatibility.
  [elro]


1.1 - 2008-03-26
----------------

- Fixed browser tests.
  [hannosch]

- Set correct i18n:domain on subject, fixes #7217.
  [martior]

- Move trunk into the egg.
  [wichert]

- Removed i18n folder. Translations are part of the PloneTranslations
  product for some time now.
  [hannosch]

1.0
---

- Providing 'fullname' now for email notification. This does not really
  close http://dev.plone.org/plone/ticket/6680, but makes it possible to
  use the information the user provided in the mail notification (and its
  translations).
  [gogo]

1.0rc2
------

- Fixed four occurrences of the term login name which wasn't used anywhere so
  far. We only use user id and user name.
  [hannosch]

1.0rc1
------

- Updated tests to work with Zope 2.10 / Plone 3.0.
  [hannosch]

- Converted mail_password_template from a dtml page to a Page Template, as
  dtml pages cannot be translated anymore.
  [hannosch]

- If available use the email_charset property instead of default_charset to
  encode mails.
  [hannosch]

- Added the portal name to the subject in the registered_notify_template.pt,
  so it's easier to distinguish those mails for various websites. This
  closes http://dev.plone.org/plone/ticket/5242.
  [hannosch]

- Replaced some last occurrences of the term member with user.
  [hannosch]

0.4.2
-----

- Fixed some minor whitespace issue in registered_notify_template.pt.
  [hannosch]

- allow password reset token to be passed in, in cases where we might not
  have the permission to request a reset from within the template
  [rafrombrc]

0.4.1
-----

- protect requestRest method of the tool so it can not be called anonymously
  through the web interface

0.4
---

- Removed unused import in install code
- use virtual host forwarded IP if present
- i18n markup (translations in PloneTranslations)
- fixed DTML markup to not fail on missing translations
- fixed root link in pwreset_expired template
- deprectation warnings removed
- tabindex not assumed present to be more CMF-friendly
- add stats to ZMI page
- implement expired record clearing on every request
- work around traversal bug with python: expressions instead of path expressions for attributes

0.3
---

- Updated to use CMFFormController
- Support for using to set initial account passwords
- Verify token before prompting user for new password
- Generated URLs don't use query strings
- Fixes to work with CMFMember
