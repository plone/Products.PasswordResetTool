## Script (Python) "pwreset_action.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Reset a user's password
##parameters=
req = context.REQUEST
fparams = {'randomstring':'', 'userid':'',
           'password':'', 'password2':'',}
for fp in fparams:
    fparams[fp] = req.get(fp, '')
    if not fparams[fp]:
        req.RESPONSE.redirect(context.portal_url())

failMessage=context.portal_registration.testPasswordValidity(fparams['password'],
                                                             fparams['password2'])
if failMessage:
    return context.pwreset_form(portal_status_message=failMessage)

try:
    pw_tool = context.portal_password_reset
    pw_tool.resetPassword(fparams['userid'], fparams['randomstring'],
                          fparams['password'])
    status = "done"
except 'ExpiredRequestError':
    status = "expired"
except 'InvalidRequestError':
    status = "invalid"

return context.pwreset_finish(status=status)

