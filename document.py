#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  ______         ______                       
# |   __ \.--.--.|   __ \.-----.-----.--------.
# |    __/|  |  ||      <|  _  |  _  |        |
# |___|   |___  ||___|__||_____|_____|__|__|__|
#         |_____| Copyright 2009 © Nicolas Rougier
#                         
#  This program is free software: you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free Software
#  Foundation, either  version 3 of the  License, or (at your  option) any later
#  version.
# 
#  This program is  distributed in the hope that it will  be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR  A  PARTICULAR PURPOSE.  See  the GNU  General  Public  License for  more
#  details.
# 
#  You should have received a copy  of the GNU General Public License along with
#  this program. If not, see <http://www.gnu.org/licenses/>.
''' '''
import pyglet
from pyglet.text.document import UnformattedDocument
import clipboard


class Action(object):
    def __init__(self, start, text):
        self.start = start
        self.end = start+len(text)
        self.text = text
        self.mergeable = len(text) == 1 or text not in '\n\r'

class Insert(Action):
    def merge(self, action):
        if not isinstance(action,Insert):
            return False
        if not self.mergeable or not action.mergeable:
            return False
        elif action.start != self.end:
            return False
        elif self.text[-1] in ' \t' and action.text not in ' \t':
            return False
        self.text += action.text
        self.end = self.start+len(self.text)
        return True

    def __repr__(self):
        return str(('i', self.start, self.text))

class Delete(Action):
    def merge(self, action):
        if not isinstance(action,Delete):
            return False
        if not self.mergeable or not action.mergeable:
            return False
        elif action.end != self.start and action.start != self.start:
            return False
        elif self.text[0] in ' \t' and action.text not in ' \t':
            return False
        if action.start == self.start: # Forward delete
            self.text += action.text
        else:                          # Backward delete
            self.start = action.start
            self.text = action.text + self.text
        self.end = self.start+len(self.text)
        return True

    def __repr__(self):
        return str(('d', self.start, self.text))


class Document(UnformattedDocument):
    '''A document having uniform style over all text with an undo/redo manager.

    Changes to the style of text within the document affects the entire
    document.  For convenience, the ``position`` parameters of the style
    methods may therefore be omitted.
    '''

    def __init__(self, text=''):
        UnformattedDocument.__init__(self, text)
        self._clipboard = None
        self._killbuffer = None
        self.end_not_undoable_action()

    def _get_clipboard(self):
        self._clipboard = clipboard.get_text() or self._clipboard
        return self._clipboard
    def _set_clipboard(self, text):
        self._clipboard = text
        clipboard.set_text(text)
    clipboard = property(_get_clipboard, _set_clipboard)

    def _get_killbuffer(self):
        self._killbuffer = clipboard.get_text('PRIMARY') or self._killbuffer
        return self._killbuffer
    def _set_killbuffer(self, text):
        self._killbuffer = text
        clipboard.set_text(text, 'PRIMARY')
    killbuffer = property(_get_killbuffer, _set_killbuffer)

    def copy(self, start, end, name = 'CLIPBOARD'):
        ''' '''
        if name == 'PRIMARY':
            self.killbuffer = self.text[start:end]
        else:
            self.clipboard = self.text[start:end]

    def cut(self, start, end, name = 'CLIPBOARD'):
        ''' '''
        if name == 'PRIMARY':
            self.killbuffer = self.text[start:end]
        else:
            self.clipboard = self.text[start:end]
        self.delete_text(start,end)

    def paste(self, start, name = 'CLIPBOARD'):
        ''' '''
        if name == 'PRIMARY':
            clipboard = self.killbuffer
        else:
            clipboard= self.clipboard
        if clipboard:
            self.insert_text(start, clipboard)

    def can_undo(self):
        ''' Determines whether a document can undo the last action.
        '''
        return len(self._undos) > 0

    def can_redo(self):
        ''' Determines whether a document can redo the last action (i.e. if the
        last operation was an undo).
        '''
        return len(self._redos) > 0

    def begin_not_undoable_action(self):
        ''' Marks the beginning of a not undoable action on the document,
        disabling the undo manager. Typically you would call this function
        before initially setting the contents of the document (e.g. when loading
        a file in a text editor).
        '''
        self._undoable_action = False

    def end_not_undoable_action(self):
        ''' Marks the end of a not undoable action on the document. When the
        last not undoable block is closed through the call to this function, the
        list of undo actions is cleared and the undo manager is re-enabled.
        '''
        self._undoable_action = True
        self._undos = []
        self._redos = []

    def insert_text(self, start, text, attributes=None):
        '''Insert text into the document.

        :Parameters:
            `start` : int
                Character insertion point within document.
            `text` : str
                Text to insert.
            `attributes` : dict
                Optional dictionary giving named style attributes of the
                inserted text.

        '''
        if self._undoable_action:
            action = Insert(start,text) 
            if self._undos:
                last = self._undos[-1]
                if not last.merge(action):
                    self._undos.append(action)
            else:
                self._undos.append(action)
            #print self._undos
        UnformattedDocument.insert_text(self, start, text, attributes)

    def delete_text(self, start, end):
        '''Delete text from the document.

        :Parameters:
            `start` : int
                Starting character position to delete from.
            `end` : int
                Ending character position to delete to (exclusive).

        '''
        if self._undoable_action:
            action = Delete(start, self.text[start:end]) 
            if self._undos:
                last = self._undos[-1]
                if not last.merge(action):
                    self._undos.append(action)
            else:
                self._undos.append(action)
            #print self._undos
        UnformattedDocument.delete_text(self, start, end)

    def undo(self):
        ''' Undoes the last user action which modified the document. Use
        can_undo to check whether a call to this function will have any effect.
        '''

        if not self._undos: return None
        action = self._undos.pop()
        if isinstance(action, Insert):
            self._redos.append(action)
            UnformattedDocument.delete_text(self, action.start, action.end)
            return action.start
        elif isinstance(action, Delete):
            self._redos.append(action)
            UnformattedDocument.insert_text(self, action.start, action.text)
            return action.end
        return None

    def redo(self):
        ''' Redoes the last undo operation. Use can_redo to check whether a call
        to this function will have any effect.
        '''

        if not self._redos: return None
        action = self._redos.pop()
        if isinstance(action, Insert):
            self._undos.append(action)
            UnformattedDocument.insert_text(self, action.start, action.text)
            return action.end
        elif isinstance(action, Delete):
            self._undos.append(action)
            UnformattedDocument.delete_text(self, action.start, action.end)
            return action.start
        return None

