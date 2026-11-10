#!/bin/bash
# Title:        cron_hoa_insights_surpriseaz.sh
# Description:  runs application with no args
# Author:       TASCS LLC
# Date:         2026-11-02
# Version:      1.0
# Usage:        ./cron_hoa_insights_surpriseaz.sh 
# Helper:       https://linux.die.net/man/1/keychain


# Load keychain variables
[ -z "$HOSTNAME" ] && HOSTNAME=`uname -n`
. $HOME/.keychain/$HOSTNAME-sh 2>/dev/null

cd /home/todd/python_projects/hoa_insights_surpriseaz/src/hoa_insights_surpriseaz

/home/todd/.local/bin/uv run main.py