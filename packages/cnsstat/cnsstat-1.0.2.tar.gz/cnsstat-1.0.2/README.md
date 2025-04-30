# cnsstat

Cheap-n-nasty text system status via psutil:

	$ cnsstat
	Load: 1 %, 0.0, 0.0, 0.0
	Temp: 51 °C
	Mem: 12 %, 0.1/1 GB
	overlay: [/] 39 %, 80.6/211 MB
	eth0: 17 | 223 kbit/s

Displays estimate of current overall CPU usage in percent, load average
divided by number of cores, CPU package temperature(s), memory usage,
mounted filesystem space and network traffic per interface TX | RX.

Text is formatted for sending by DM or SMS.

## Usage

	cnsstat [NETDEV] ...

Optionally specify a list of network devices to display
on the command line, any that are up will be included in
the output.

## Requirements

   - psutil

## Installation

	$ python3 -m venv --system-site-packages venv
	$ ./venv/bin/pip install cnsstat

