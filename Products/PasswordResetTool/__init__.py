"""Initialize PasswordResetTool Product"""

from Products.CMFCore import utils
import PasswordResetTool

product_globals = globals()

tools = ( PasswordResetTool.PasswordResetTool, )

def initialize(context):
    utils.ToolInit('Password Reset Tool',
                    tools = tools,
                    icon='tool.gif' 
                    ).initialize( context )
