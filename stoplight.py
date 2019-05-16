from time import sleep
from gpiozero import LED


class Stoplight:
    def __init__(self, states, gpio, fakeGpio=False):
        self.states = states
        self.gpio = gpio
        self.controller = {}
        self.fakeGpio = fakeGpio
        self.ON = True
        self.OFF = False
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

    def controll_pin(self, pin, instruction):
        if instruction:
            if not self.fakeGpio:
                self.controller[pin].on()
            else:
                print("just turned on GPIO " + str(self.controller[pin]))
        else:
            if not self.fakeGpio:
                self.controller[pin].off()
            else:
                print("just turned off GPIO " + str(self.controller[pin]))

    def blink(self, pin, interval, duration):
        oscilations = duration/(interval * 2)
        for i in range(int(oscilations)):
            print("pin ON")
            self.controll_pin(pin, self.ON)
            sleep(interval)
            print("pin OFF")
            self.controll_pin(pin, self.OFF)
            sleep(interval)
        self.controll_pin(pin, self.ON)

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
