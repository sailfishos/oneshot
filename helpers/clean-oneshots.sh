#!/bin/sh
# Copyright (c) 2020 Open Mobile Platform LLC.
#
# Cleans up oneshot jobs after removing user

USERID="$1"

if [ -n "$USERID" ]; then
    DIRECTORY="/etc/oneshot.d/$USERID/"
    [ ! -d "$DIRECTORY" ] && exit 0
    rm -r "$DIRECTORY"
else
    echo "No uid given!"
    exit 1
fi
