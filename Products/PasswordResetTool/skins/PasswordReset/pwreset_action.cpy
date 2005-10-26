## Script (Python) "pwreset_action.cpy"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Reset a user's password
##parameters=randomstring, userid=None, password=None, password2=None
from Products.CMFCore.utils import getToolByName

status = "success"
pw_tool = getToolByName(context, 'portal_password_reset')
try:
    pw_tool.resetPassword(userid, randomstring, password)
except 'ExpiredRequestError':
    status = "expired"
except 'InvalidRequestError':
    status = "invalid"

membership_tool = getToolByName(context, 'portal_membership')
member = membership_tool.getMemberById(userid)
login_time = member.getProperty('login_time', '2000/01/01')
if  str(login_time) == '2000/01/01':
  try:
    membership_tool.setLoginTimes()
    membership_tool.createMemberArea()
  except AttributeError:
    pass       # plone 2.0.5 doesn't have this

return state.set(status=status)

