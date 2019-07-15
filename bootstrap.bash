#!/bin/bash
git pull
echo "booted at $(date)"
/home/pi/.pyenv/shims/python circle_ci_monitor.py 