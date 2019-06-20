#!/bin/bash
sleep 10s
git pull
echo "booted at $(date)" >> logs.log
python circle_ci_monitor.py >> logs.log