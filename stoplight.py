# -*- coding: utf-8 -*-
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

    def control_pin(self, pin, instruction):
        if instruction:
            if not self.fakeGpio:
                self.controller[pin].on()
            # else:
            print(
                "GPIO " + str(self.controller[pin]).zfill(2) + " O " + pin)
        else:
            if not self.fakeGpio:
                self.controller[pin].off()
            # else:
            print(
                "GPIO " + str(self.controller[pin]).zfill(2) + " X " + pin)

    def blink(self, pin, interval, duration):
        oscilations = duration/(interval * 2)
        for i in range(int(oscilations)):
            print("pin ON")
            self.control_pin(pin, self.ON)
            sleep(interval)
            print("pin OFF")
            self.control_pin(pin, self.OFF)
            sleep(interval)
        self.control_pin(pin, self.ON)

    def assert_state(self, state):
        print("state assertion has been received")
        for key in self.states[state]:
            if self.states[state][key]:
                self.control_pin(key, self.ON)
            else:
                self.control_pin(key, self.OFF)
        print("state assertion has been completed")
