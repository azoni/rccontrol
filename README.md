rccontrol
============
rccontrol is Python library for controlling RC Car. rccontrol allows you to control your RC Car through Intel edison.

### how to install

- git clone https://github.com/konchan/rccontrol.git 
- Move to src folder and run the following command.

```
python setup.py install
```

### how to use

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
  
```

### Contributing
1. Fork it
2. Create your feature branch (```git checkout -b my-new-feature```)
3. Commit your changes (```git commit -am 'Add some feature'```)
4. Push to the branch (```git push origin my-new-feature```)
5. Create new Pull Request
