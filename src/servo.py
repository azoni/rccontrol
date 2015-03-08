#/usr/bin/env python
# -*- coding: utf-8 -*-
# Servo.py
# Author: KONNO Katsuyuki <konno.katsuyuki@nifty.com>
# Copyright (c) 2015 KONNO Katsuyuki
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import mraa
import time
import logging
import datetime
from threading import Thread, Event

class Servo(Thread):
    def __init__(self, pin):
        super(Servo, self).__init__()
        self.NEUTRAL = 0.06
        self.x = mraa.Pwm(pin)
        self.x.period_ms(20)
        self.x.enable(True)
        self.MAX_ANGLE = 30
        self.offset = 0
        self.x.write(self.NEUTRAL)
        self.thread_wait = 0.1
        self.stop_event = Event()

        # logger
        self.log = logging.getLogger('Servo')
        self.log.setLevel(logging.INFO)
        logHandler = logging.FileHandler(datetime.datetime.now().strftime('Servo_%Y%m%d_%H%M%S.log'))
        logHandler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        self.log.addHandler(logHandler)
        self.logpath = ""
        self.log.info('Starting Servo...')

    def set_max_angle(self, angle):
        self.log.info('set MAX ANGLE to %i' % (direction, offset))
        self.MAX_ANGLE = angle

    def set_offset(self, direction, offset):
        self.log.info('set %s offset to %i' % (direction, offset))
        if direction == 'left':
            self.NEUTRAL += offset/self.MAX_ANGLE
        else:
            self.NEUTRAL -= offset/self.MAX_ANGLE
        self.MAX_ANGLE -= offset

    def turn_left(self, angle):
        self.log.info('turn left, angle: %i' % angle)
        self.turn(angle)

    def turn_right(self, angle):
        self.log.info('turn right, angle: %i' % angle)
        self.turn(-1*angle)

    def turn(self, angle):
        if (abs(angle) <= self.MAX_ANGLE):
            try:
                angle += self.MAX_ANGLE
                val = float(angle)/(self.MAX_ANGLE*2) * self.NEUTRAL + 0.03
                self.log.debug('write pulse width of %f us' % val)
                self.x.write(round(val,2))
            except Exception as e:
                self.log.error(e)
        else:
            self.log.warn('angle[%i] exceeds the max angle[%i]' % (angle, self.MAX_ANGLE))

    def stop(self):
        self.stop_event.set()

    def run(self):
        while True:
            if self.stop_event.is_set():
                self.turn(0)
                self.log.info('terminating Servo...')
                break
            self.stop_event.wait(self.thread_wait)
