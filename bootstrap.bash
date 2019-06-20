#!/bin/bash
sleep 10s
git pull
echo "booted at $(date)"
python circle_ci_monitor.py