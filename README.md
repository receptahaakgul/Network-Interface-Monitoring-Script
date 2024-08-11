# Network Monitor

A Python script for monitoring network interfaces and saving data to a SQLite database.

## Features

- **Monitor Network Interfaces:** Tracks key network statistics such as IP address, netmask, broadcast address, and more.
- **Data Storage:** Saves the monitored data into a SQLite database for easy retrieval and analysis.
- **Customizable:** Choose which network parameters to monitor using command-line arguments.
- **Clear Database:** Easily clear the database with a simple command.

## Installation and Usage on WSL (Ubuntu)

### Prerequisites

- Ensure that WSL is installed on your Windows machine.
- Install Ubuntu from the Microsoft Store if you haven't already.
- Make sure Python 3.x and SQLite3 are installed in your WSL Ubuntu environment.

### Step-by-Step Guide

1. **Open WSL Ubuntu:**
   - Press `Win + R`, type `wsl` and hit enter.

2. **Clone the Repository:**
   - Run the following command in your WSL terminal:
     ```bash
     git clone https://github.com/kullaniciadi/network-monitor.git
     ```
   - Navigate into the project directory:
     ```bash
     cd network-monitor
     ```

3. **Install Required Packages:**
   - Ensure Python and SQLite3 are installed. You can install them using:
     ```bash
     sudo apt update
     sudo apt install python3 sqlite3
     ```

4. **Run the Script:**
   - You can run the script using various command-line arguments. For example:
     ```bash
     python3 network_monitor.py --interval 30 --all
     ```
   - This command will monitor all available network statistics every 30 seconds and store them in the database.

### Command-Line Arguments

- `--clear` : Clear the database.
- `--all` : Save all available network information.
- `--inet` : Save IP address information.
- `--netmask` : Save netmask value.
- `--broadcast` : Save broadcast address.
- `--inet6` : Save IPv6 address.
- `--ether` : Save Ethernet address.
- `--rx_pocket` : Save RX packet count.
- `--rx_error` : Save RX error count.
- `--tx_pocket` : Save TX packet count.
- `--tx_error` : Save TX error count.
- `--interval <seconds>` : Set the monitoring interval in seconds.
- `--yardim` : Show help message.

### Example

To monitor the `inet` and `netmask` values every 20 seconds, run:
```bash
python3 network_monitor.py --interval 20 --inet --netmask
