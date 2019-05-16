from time import sleep
from gpiozero import LED


class Stoplight:
    def __init__(self, states, gpio, fakeGpio=False):
        self.states = states
        self.gpio = gpio
        self.controller = {}
        self.fakeGpio = fakeGpio
        # self.state = "null"
        for pinout in gpio:
            print("assigning " + pinout + " to GPIO pin: " + str(gpio[pinout]))
            # self.controller[pinout] = gpio[pinout]
            if not self.fakeGpio:
                self.controller[pinout] = LED(gpio[pinout])
                self.controller[pinout].off()
                sleep(1)
            else:
                self.controller[pinout] = gpio[pinout]
                print("Imagine I just turned off LED " + str(gpio[pinout]))
        for state in self.states:
            print("testing: " + state)
            self.assert_state(state)
            if not self.fakeGpio:
                sleep(2)
        self.assert_state("null")

    def assert_state(self, state):
        for key in self.states[state]:
            if self.states[state][key]:
                if not self.fakeGpio:
                    self.controller[key].on()
                else:
                    print("just turned on GPIO " + str(self.controller[key]))
            else:
                if not self.fakeGpio:
                    self.controller[key].off()
                else:
                    print("just turned off GPIO " + str(self.controller[key]))
