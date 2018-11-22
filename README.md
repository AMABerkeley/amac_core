# amac_core
Core AMAC ROS Metapackages. Should defintely have sudo access to get everything working.

# Setup
`mkdir -p catkin_ws/src`\
`cd catkin_ws/src`\
`catkin_init_workspace`\
`git clone https://github.com/AMABerkeley/amac_core.git`\
`git clone https://github.com/AMABerkeley/inertial_sense_ros.git`\
`git clone https://github.com/AMABerkeley/usb_cam.git`\
`git clone https://github.com/AMABerkeley/ouster_lidar.git`\
`cd ..`\
`catkin_make`\

## Usage (Docker)

Install [Docker Container Environment](https://docs.docker.com/install/) if you haven't already.

Build and tag the container with `docker build -t amac/ros <<PATH>>`, replacing `PATH` with the directory containing the Dockerfile.

To shell into the container, run `docker run -it amac/ros`.

## Usage (No Docker)

To run without docker, simply install dnsmasq and perhaps some other dependencies. `sudo apt-get install dnsmasq`

edit this file `sudo vim /etc/dnsmasq.conf`

uncomment this line: `dhcp-range=192.168.1.50,192.168.1.150,12h`

uncomment this line: `interface=enp0s31f6`

save changes then sethernet connection to manual iPv4 `194.168.1.1`

run dnsmasq: `sudo systemctl start dnsmasq`

Use `journalctl -fu dnsmasq` to see dnsmasq’s status. You should see an IP address be allocated to the sensor after 10-15 seconds.

Then startup all sensors by: `roslaunch amac_bringup drive.launch os1_hostname:=<os1_hostname> os1_udp_dest:=<udp_data_dest>` os1_hostname deafult: 192.168.1.94 udp_dest default: 192.168.1.1


## Common Problems

Not enough bandwidth for three cameras hooked up on one USB-hub plugged into one USB port. Simply run:
`sudo rmmod uvcvideo`\
`sudo modprobe uvcvideo quirks=128`\

OpenCV 2 is needed for usb-cam launch. This is to set size of capture image to smaller than opencv 3 allows.

Must upload arduino code that is here: `https://github.com/AMABerkeley/amac_arduino` in order for this to run. Future version will embed the compilation of arduino code within this package. 
