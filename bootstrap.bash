#!/bin/bash
git -C /home/pi/circle-stoplight pull
echo "booted at $(date)"
/home/pi/.pyenv/shims/python circle_ci_monitor.py