README

  Readme for the PasswordResetTool product for CMF,
  by "J. Cameron Cooper":mailto:prt@jcameroncooper.com for
  "The Connexions Project":http://cnx.rice.edu

  The Password Reset Tool hooks into the standard mechanisms for
  password mailing provided by the CMF in the Registration Tool and
  certain skins and replaces this with a facility for resetting
  passwords with email authentication.

  This is useful not only to keep passwords out of cleartext email and
  is absolutely necessary if you choose to encrypt your passwords (and
  you should.)

  See the INSTALL.txt file for details on installation, and the
  LICENSE.txt file for the license this Product is under.

  The Password Reset Sequence from the User's Point of View

    The user will observe the following steps.

      - User forgets a password and

      - clicks "Forgot your password?", which

      - goes to a form that asks for a username. User fills this in and
        clicks a button to proceed, which

      - goes to a form explaining that an email has been sent.

      - User receieves an email with a URL containing a random,
        unguessable key and opens it in a web browser.

      - This is a form that asks for username and password, which goes to

      - a form reporting success (or failure, if expired or illegitimate.)

  Management Notes

    Reset requests are stored in a persistent dictionary in the
    tool. Removing the tool or reinstalling the product will destroy
    all reset requests.

    A facility for clearing expired requests is provided. This should
    be used occasionally to clear out the storage. A cron script using
    'wget' or 'curl' (or the Windows equivalent) is suggested.

  Notes

    * You can turn username entry off, if you so desire, as this will
      streamline the process. You SHOULD NOT DO THIS if you are
      concerned about account security. Not requiring re-entry of the
      user name allows trivial email-sniffing attacks and makes
      brute-forcing of the reset request keys possible (if unlikely).

    * The very first visit after installation or a restart to a
      'passwordreset' URL will result in a '404 Not Found' error. This
      is a known issue. That script uses the traverse_subpath
      variable, which is (presumably) not obvious to the skinning
      machinery until it is used once. After an initial visit, this is
      remembered. If this is not acceptable behaviour, simply modify
      the 'passwordreset' script to contain the following::

        ##parameters=randomstring
        return context.pwreset_form(randomstring=randomstring)

      Also change 'pwreset_constructURL' to use::

        return "%s/passwordreset?randomstring=%s" % (host, randomstring)

      Hopefully this will be addressed in the future.

    * This tool replaces the built-in password mailing feature. This
      means that the first half of a "forgotten password transaction"
      depends on skin names set in CMF code.

      However, it can be made independent, if you so desire. Simply
      provide an equivalent to

        * 'mail_password_form':
	  Asks for your username, and provides instructions as to what's to come.

        * 'mail_password':
	  Receives the request from mail_password_form, calls 'requestReset' on
	  the tool, and sends a message with the return URL however you care to
	  construct it (usually in 'pwreset_constructURL', which depends on what
	  the equivalent to 'passwordreset' is named.) Returns the equivalent of
	  'mail_password_response'.

	* 'mail_password_template':
	  Provides the text of the email.

	* 'mail_password_response':
	  Informs that the mail has been sent.

      Naturally, the methods and templates on the other side will need
      to be migrated over or have equivalents made as well. If outside
      the CMF, certain source changes will also be needed, such as
      overriding 'getValidUser'.

    * This tool has been made with customization in mind. There are
      several customization points in the code that should allow you
      to change certain policies simply by subclassing the tool and
      overriding one or two methods.
