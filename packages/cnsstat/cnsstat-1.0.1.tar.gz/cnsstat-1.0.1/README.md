# cnsstat

Cheap-n-nasty text system status via psutil:

	$ cnsstat
	Load: 4 %, 0.1, 0.1, 0.0
	Temp: 41.0 °C
	Mem: 46 %, 1.3/4 GB
	sda: [/] 38 %, 45.1/119 GB
	wlp1s0: 4 | 3 kbit/s

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

