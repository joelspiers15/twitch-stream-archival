#!/usr/bin/env bash

mkdir -p logs

log_file=logs/`date +%m-%d-%Y_%H:%M`.log
flock -n /tmp/twitch-stream-archival.lockfile sudo python3 twitch-stream-archival.py >${log_file} 2>&1 &

echo "======== Starting Server ========"
echo "To stop server:"
echo -e "\tsudo ./stop_server"
if [[ "$1" = "-w" ]]
then
    echo -e "\tThe output below is just live output of the log file."
    echo -e "\tCTRL+C WILL NOT STOP THE SERVER"
    tail -f ${log_file}
else
    echo "To watch logs live run start_server.sh with the -a flag or:"
    echo -e "\ttail -f $log_file"
fi