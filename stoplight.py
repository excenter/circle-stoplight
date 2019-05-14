from time import sleep
from gpiozero import LED


class Stoplight:
    def __init__(self, states, gpio):
        self.states = states
        self.gpio = gpio
        self.controller = {}
        for pinout in gpio:
            print("assigning " + pinout + " to GPIO pin: " + str(gpio[pinout]))
            # self.controller[pinout] = gpio[pinout]
            self.controller[pinout] = LED(gpio[pinout])
            self.controller[pinout].off()
            sleep(1)
        for state in self.states:
            print("testing: " + state)
            self.assert_state(state)
            sleep(2)
        self.assert_state("null")

    def assert_state(self, state):
        for key in self.states[state]:
            if self.states[state][key]:
                self.controller[key].on()
                # print("just turned on GPIO " + str(self.controller[key]))
            else:
                self.controller[key].off()
                # print("just turned off GPIO " + str(self.controller[key]))
