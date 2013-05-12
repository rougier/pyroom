'''Interaction with the Operating System text clipboard
'''

import sys

def get_text(name = 'CLIPBOARD'):
    '''Get a string from the clipboard.
    '''
    return _clipboard.get_text(name)

def set_text(text, name = 'CLIPBOARD'):
    '''Put the string onto the clipboard.
    '''
    return _clipboard.set_text(text, name)

# Try to determine which platform to use.
if sys.platform == 'darwin':
    #from carbon import CarbonPasteboard
    #_clipboard = CarbonPasteboard()
    _clipboard = None
elif sys.platform in ('win32', 'cygwin'):
    from win32 import Win32Clipboard
    _clipboard = Win32Clipboard()
else:
    from xlib import XlibClipboard
    _clipboard = XlibClipboard()

