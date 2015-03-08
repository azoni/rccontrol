#/usr/bin/env python
# -*- coding: utf-8 -*-
# ESC.py
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

class Esc(Thread):
    def __init__(self, pin):
        super(Esc, self).__init__()
        self.NEUTRAL = 1300
        self.FORWARD_MAX = 2000
        self.BACKWARD_MAX = 500
        self.LIMIT_SPEED = 100
        self.f_step = int((self.FORWARD_MAX-self.NEUTRAL)/100)
        self.b_step = int((self.NEUTRAL-self.BACKWARD_MAX)/100)
        self.x = mraa.Pwm(pin)
        self.x.period_ms(20)
        self.x.enable(True)
        self.current_pulsewidth = self.NEUTRAL
        self.step = 100
        self.wait_time = 0.2
        self.thread_wait = 0.1
        self.stop_event = Event()

        # logger
        self.log = logging.getLogger('Esc')
        self.log.setLevel(logging.INFO)
        logHandler = logging.FileHandler(datetime.datetime.now().strftime('Esc_%Y%m%d_%H%M%S.log'))
        logHandler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        self.log.addHandler(logHandler)
        self.logpath = ""
        self.log.info('Starting Esc...')

    def calibrate_forward(self):
        self.log.info('calibrating forward, %i' % self.FORWARD_MAX)
        self.x.pulsewidth_us(self.FORWARD_MAX)

    def calibrate_backward(self):
        self.log.info('calibrating backward, %i' % self.BACKWARD_MAX)
        self.x.pulsewidth_us(self.BACKWARD_MAX)

    def calibrate_neutral(self):
        self.log.info('calibrating neutral, %i' % self.NEUTRAL)
        self.x.pulsewidth_us(self.NEUTRAL)

    def set_limit(self, speed):
        self.LIMIT_SPEED = speed

    def up_range(self, start, stop):
        r = start
        while r < stop:
            yield r
            r += self.step

    def down_range(self, start, stop):
        r = start
        while r > stop:
            yield r
            r -= self.step

    def forward(self, speed):
        if speed > self.LIMIT_SPEED: speed = self.LIMIT_SPEED
        val = speed * self.f_step + self.NEUTRAL
        if val > self.current_pulsewidth:
            range_ = self.up_range(self.current_pulsewidth, val)
        else:
            range_ = self.down_range(self.current_pulsewidth, val)
        for v in range_:
            self.x.pulsewidth_us(v)
            time.sleep(self.wait_time)
        self.current_pulsewidth = val
        self.log.info('set forward speed to %i' % speed)

    def backward(self, speed):
        if speed > self.LIMIT_SPEED: speed = self.LIMIT_SPEED
        val = self.NEUTRAL - speed * self.b_step
        if val > self.current_pulsewidth:
            range_ = self.up_range(self.current_pulsewidth, val)
        else:
            range_ = self.down_range(self.current_pulsewidth, val)
        for v in range_:
            self.x.pulsewidth_us(v)
            time.sleep(self.wait_time)
        self.current_pulsewidth = val
        self.log.info('set backward speed to %i' % speed)

    def stop(self):
        self.stop_event.set()

    def run(self):
        while True:
            if self.stop_event.is_set():
                self.forward(0)
                self.log.info('terminating Esc...')
                break
            self.stop_event.wait(self.thread_wait)
