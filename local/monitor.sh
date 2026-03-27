#!/bin/bash

# --- Configuration ---
DEVICE_ID="rpi-728"
LEASES_FILE="/var/lib/misc/dnsmasq.leases"
LOCAL_LOG="/home/pi/monitor_hallow_results.log"

# 1. Extract the IP address
TARGET_IP=$(awk -v id="$DEVICE_ID" '$0 ~ id {print $3}' "$LEASES_FILE")

# Handle case where IP is not found in leases
if [ -z "$TARGET_IP" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') | ERROR | IP not found for $DEVICE_ID" >> "$LOCAL_LOG"
    exit 1
fi

# 2. Run the ping (5 packets)
# We use -q (quiet) to only output the summary at the end
PING_OUTPUT=$(ping -c 5 -q "$TARGET_IP" 2>&1)
PING_STATUS=$?

# 3. Process and Log Results
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

if [ $PING_STATUS -eq 0 ]; then
    # Extract the line containing 'rtt' and the actual values
    RTT_STATS=$(echo "$PING_OUTPUT" | grep 'rtt' | cut -d' ' -f4)
    echo "$TIMESTAMP | SUCCESS | IP: $TARGET_IP | RTT: $RTT_STATS (min/avg/max/mdev)" >> "$LOCAL_LOG"
else
    echo "$TIMESTAMP | FAILED  | IP: $TARGET_IP | Host Unreachable" >> "$LOCAL_LOG"
fi
