flock -n /tmp/twitch-stream-archival.lockfile sudo python3 twitch-stream-archival.py >logs/`date +%m-%d-%Y_%H:%M`.log 2>&1 &
