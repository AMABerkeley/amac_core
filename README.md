# amac_core
Core AMAC ROS Metapackage

## Usage

Install [Docker Container Environment](https://docs.docker.com/install/) if you haven't already.

Build and tag the container with `docker build -t amac/ros <<PATH>>`, replacing `PATH` with the directory containing the Dockerfile.

To shell into the container, run `docker run -it amac/ros`.


To run without docker, simply install dnsmasq and perhaps some other dependencies. `sudo apt-get install dnsmasq`

edit this file `sudo vim /etc/dnsmasq.conf`

uncomment this line: `dhcp-range=192.168.1.50,192.168.1.150,12h`

uncomment this line: `interface=enp0s31f6`

save changes then sethernet connection to manual iPv4 `194.168.1.1`

run dnsmasq: `sudo systemctl start dnsmasq`

Use `journalctl -fu dnsmasq` to see dnsmasq’s status. You should see an IP address be allocated to the sensor after 10-15 seconds.

Then startup all sensors by: `roslaunch amac_bringup drive.launch os1_hostname:=<os1_hostname> os1_udp_dest:=<udp_data_dest>` os1_hostname deafult: 192.168.1.94 udp_dest default: 192.168.1.1