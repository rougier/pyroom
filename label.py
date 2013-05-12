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

from pyglet.text import Label

class FadingLabel(Label):
    def __init__(self, *args, **kwargs):        
        super(FadingLabel,self).__init__(*args, **kwargs)
        self.visible = False
        self.fadeout = 0.25
        self._time = 0

    def _fadeout_start(self, dt=0, start=False):
        if start:
            self._time = 0
            pyglet.clock.schedule_interval(self.fadeout, 1/60.)
        else:
            self._time += dt
            a = 1.0 - self._time/self.fadeout_time
            if self._time > self.fadeout_time:
                self.visible = False
                pyglet.clock.unschedule(self.update)
            else:
                self.color = (255,255,255,int(a*255))

    def _fadeout_do(self, dt=0, start=False):
        if start:
            self._time = 0
            pyglet.clock.schedule_interval(self.fadeout, 1/60.)
        else:
            self._time += dt
            a = 1.0 - self._time/self.fadeout_time
            if self._time > self.fadeout_time:
                self.visible = False
                pyglet.clock.unschedule(self.update)
            else:
                self.color = (255,255,255,int(a*255))

    def show(self, time=3.0, fadeout_time=0.25):
        self.visible = True
        self.fadeout_time = fadeout_time
        pyglet.clock.schedule_once(self.fadeout, time, start=True)

    def draw(self):
        if self.visible:
            super(Label,self).draw()


if __name__ == '__main__':
    import pyglet
    import pyglet.window

    window = pyglet.window.Window()
    label = FadingLabel(text='Hello world !',
                        font_name = 'Bitstream Vera Sans',
                        font_size=16,
                        anchor_x='center', anchor_y='center',
                        x=window.width//2, y=window.height//2)
    label.show()

    @window.event
    def on_draw():
        window.clear()
        label.draw()

    pyglet.app.run()
