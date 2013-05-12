''' Clipboard implementation for X11 using xlib. '''
import os
from ctypes import *
from pyglet import window
from pyglet.window.xlib import xlib

class XlibClipboard(object):
    def get_text(self, name='CLIPBOARD'):
        option = '-b'
        if name == 'PRIMARY':
            option = '-p'
        elif name == 'SECONDARY':
            option = '-s'
        try:
            return os.popen('xsel %s' % option).read()
        except:
            return None

    def set_text(self, text, name='CLIPBOARD'):
        option = '-b'
        if name == 'PRIMARY':
            option = '-p'
        elif name == 'SECONDARY':
            option = '-s'
        try: 
            os.popen('xsel %s' % option, 'wb').write(text) 
        except:
            pass


if __name__ == '__main__':
    cb = XlibClipboard()
    print 'GOT', `cb.get_text()`            # display last text clipped
    s = "[Clipboard text replaced]"
    cb.set_text(s)
    assert s ==  cb.get_text()              # replace it


