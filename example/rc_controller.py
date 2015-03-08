#/usr/bin/env python
# -*- coding: utf-8 -*-
# rc_controller.py
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
 
from rccontrol import Servo, Esc
import time

if __name__ == "__main__":
    servo = Servo(3)
    servo.start()
    esc = Esc(5)
    print 'start calibrating:'
    esc.calibrate_forward()
    raw_input('press enter key')
    esc.calibrate_backward()
    raw_input('press enter key')
    esc.calibrate_neutral()
    raw_input('press enter key')
    print 'done.'
    esc.start()

    while True:
        val = raw_input('input value: ')
        print val
        if (val == 'q'):
            servo.stop()
            esc.stop()
            exit()
        try:
            type_, v_ = val.split(',')
            if type_ == 'f':
                print 'forward, speed', v_
                esc.forward(int(v_))
            elif type_ == 'b':
                print 'backward, speed', v_
                esc.backward(int(v_))
            elif type_ == 'l':
                print 'turn left, angle', v_
                servo.turn_left(int(v_))
            elif type_ == 'r':
                print 'turn right, angle', v_
                servo.turn_right(int(v_))
        except:
            continue
        time.sleep(0.1)
