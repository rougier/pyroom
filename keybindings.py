#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Nicolas P. Rougier
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
#
# Adapted from multi_hotkey.py by Josiah carlson (http://come.to/josiah)

"""
This module exposes a class that bind arbitrary key sequences within
a pyglet application. A sequence is described as a comma separated list
string describing the sequence.

Examples:
---------
"Control-X"           -> Type Control + X
"Control-X,Control-C" -> Type Control + X then Control + C

Note:
-----
* If a given complete sequence is also the starting sequence of another
  one, the last sequence won't be registered. For example, you cannot
  register "Control,x" then register "Control,x,y" since there is no
  (context-free) way to decide which sequence to consider when
  control,x is pressed.
* Do not use "Alt" for describing the Alt key but use "Meta" since it
  is the official name.
"""

import pyglet

class KeyBindings:
    """ Arbitrary key sequences bindings to be used in a GTK application """

    def __init__ (self, fallback=None):
        """ Initialization

        Arguments:
        ----------
        fallback -- Function to call if pressed key is not part of a sequence
        """
        self.clear()
        self.__fallback = fallback


    def clear (self):
        """ Clear all keybindings """

        self.bindings = {}
        self.bindings_list = {}
        self.sequence = self.bindings
        

    def set_fallback (self, fallback):
        """ Set fallback function
        
        Arguments:
        ----------
        fallback -- Function to call if pressed key is not part of a sequence
        """

        self.__fallback = fallback


    def register (self, sequence, function, *args, **kwargs):
        """ Register a new key sequence

        Arguments:
        ----------
        sequence -- string describing the sequence
        function -- function to call when the sequence has been typed
        *args    -- arguments to pass to the function
        **kwargs -- keyword arguments to pass to the function
        """

        sequence = sequence.lower()
        bindings = self.bindings
        x = [i.strip() for i in sequence.split(',') if i]
        x = [(i, j==len(x)-1) for j,i in enumerate(x)]
        for name, last in x:
            if last:
                if name in bindings:
                    return False
                bindings[name] = (function, args, kwargs)
                self.bindings_list[sequence] = (function, args, kwargs)
            else:
                if name in bindings:
                    if not isinstance(bindings[name], dict):
                        return False
                else:
                    bindings[name] = {}
                bindings = bindings[name]
                self.bindings_list[sequence] = (function, args, kwargs)


    def unregister (self, sequence):
        """ Unregister a key sequence

        Arguments:
        ----------
        sequence -- string describing the sequence
        """

        # Remove sequence from list
        if self.bindings_list.has_key (sequence):
            self.bindings_list.pop (sequence)
        # Rebuild remaining bindings
        self.bindings = {}
        for key in self.bindings_list:
            function, args, kwargs = self.bindings_list[key]
            try:
                self.register (key, function, *args, **kwargs)
            except:
                pass

    def on_key_press(self, symbol, modifiers):
        """ Key press event callback

        Each time a key is pressed, this callback has to be called. It returns
        True is the pressed key corresponds to some ongoing sequence, else, it
        calls the default handler if any, else it return False.

        Arguments:
        ----------
        """
        key = ''
        prefix = ''
        if modifiers & pyglet.window.key.MOD_CTRL:
            prefix += "control-"
        if modifiers & pyglet.window.key.MOD_SHIFT:
            prefix += "shift-"
        if modifiers & pyglet.window.key.MOD_ALT:
            prefix += "alt-"
        if symbol > 32 and symbol < 127:
            key = prefix + chr(symbol)
        if not key:
            return pyglet.event.EVENT_UNHANDLED
        if key not in self.sequence:
            self.sequence = self.bindings
        if key in self.sequence:
            self.sequence = self.sequence[key]
            if not isinstance(self.sequence, dict):
                args = self.sequence[1]
                kwargs = self.sequence[2]
                self.sequence[0](*args, **kwargs)
                self.sequence = self.bindings
            return True
        elif self.sequence is not self.bindings:
            self.sequence = self.bindings
        elif self.__fallback:
            return self.__fallback (widget, event)
        return False


if __name__ == '__main__':
    def func(a,b):
        print "a: %d, b: %d" %(a,b)
    keybindings = KeyBindings()
    keybindings.register("control-a", func, a=1, b=2)
    keybindings.register("control-shift-a", func, a=1, b=2)
    keybindings.register("control-b", func, 4, 5)
    keybindings.register("control-x, control-c", pyglet.app.exit )
    window = pyglet.window.Window()
    window.push_handlers(keybindings)
    pyglet.app.run()
