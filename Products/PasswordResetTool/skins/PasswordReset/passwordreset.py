## Script (Python) "passwordreset.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Receive password reset requests
##parameters=key=None
if key:
    randomstring = key
else:
    randomstring = traverse_subpath[0]
return context.pwreset_form(randomstring=randomstring)
