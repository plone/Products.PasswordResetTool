## Script (Python) "pwreset_action.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Reset a user's password
##parameters=randomstring, userid, password, password2

failMessage=context.portal_registration.testPasswordValidity(password, password2)
if failMessage:
    return context.pwreset_form(portal_status_message=failMessage)

try:
    pw_tool = context.portal_password_reset
    pw_tool.resetPassword(userid, randomstring, password)
    status = "done"
except 'ExpiredRequestError':
    status = "expired"
except 'InvalidRequestError':
    status = "invalid"

return context.pwreset_finish(status=status)

