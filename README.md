# Network Fleet Monitor 📡

![System Architecture](diagram.png)

A lightweight monitoring system for intermittent wireless connections.

## Architecture
1. **Local (Device):** A Bash script reads `dnsmasq.leases`, pings the target, and logs locally.
2. **Sync:** A cron job on the Remote Host pulls logs via `rsync`.
3. **Remote (Dashboard):** A Streamlit app visualizes connectivity and latency for all devices.

## Installation

### 1. Local Device Setup
- Copy `local/monitor.sh` to the device.
- Make it executable (chmod +x monitor.sh)
- Add to crontab (`crontab -e`):
  `*/5 * * * * /home/pi/monitor.sh`

### 2. Remote Host Setup
- **Syncing:** Add this to the remote host crontab to pull data from the local device (10.20.20.2):
- `* * * * * rsync -avz --append-verify pi@10.20.20.2:/home/pi/monitor_hallow_results.log /home/idwave/monitor_hallow_results.log`

- **Dashboard:**
  ```bash
  cd remote
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

### 3. Run streamlit as systemd service:
 
- Copy streamlit_monitor.service to /etc/systemd/system/, reload daemon, and start the service.
- `sudo systemctl daemon-reload`
- `sudo systemctl enable --now streamlit_monitor.service`
- `sudo systemctl start streamlit_monitor.service`
- `sudo systemctl status streamlit_monitor.service`

