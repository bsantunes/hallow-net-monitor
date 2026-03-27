# Network Fleet Monitor 📡

A lightweight monitoring system for intermittent wireless connections.

## Architecture
1. **Local (Device):** A Bash script reads `dnsmasq.leases`, pings the target, and logs locally.
2. **Sync:** A cron job on the Remote Host pulls logs via `rsync`.
3. **Remote (Dashboard):** A Streamlit app visualizes connectivity and latency for all devices.

## Installation

### 1. Local Device Setup
- Copy `local/monitor.sh` to the device.
- Add to crontab (`crontab -e`):
  `* * * * * /home/pi/monitor.sh`

### 2. Remote Host Setup
- **Syncing:** Add this to the remote host crontab to pull data from the local device (10.20.20.2):
  `* * * * * rsync -az pi@10.20.20.2:/home/pi/monitor_hallow_results.log /home/idwave/`

- **Dashboard:**
  ```bash
  cd remote
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
