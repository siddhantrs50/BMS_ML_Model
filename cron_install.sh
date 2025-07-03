#!/bin/bash

# Absolute path to Python and project directory
PYTHON_PATH=$(which python3)
PROJECT_DIR=$(cd "$(dirname "$0")"; pwd)
SCRIPT="$PROJECT_DIR/daily_predict.py"
LOGFILE="$PROJECT_DIR/cron.log"

# Ensure cron job is not already set
(crontab -l 2>/dev/null | grep -v daily_predict.py; echo "0 23 * * * $PYTHON_PATH $SCRIPT >> $LOGFILE 2>&1") | crontab -

echo "✅ Cron job installed: daily at 11:00 PM"
echo "Log file: $LOGFILE"
