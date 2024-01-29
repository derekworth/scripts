
#Enable Jumbo frames -- be careful if you are turning off the ethernet attached to VNC -- copy paste all the commands at once
#sudo ip link set eth0 down
#sudo ip link set eth0 mtu 9000
#sudo ip link set eth0 up

#Maximize ethernet receive buffers to avoid partial / incomplete vimba images
#sudo sysctl -w net.core.rmem_max=33554432
#sudo sysctl -w net.core.wmem_max=33554432
#sudo sysctl -w net.core.rmem_default=33554432
#sudo sysctl -w net.core.wmem_default=33554432

#Set path for this terminal to launch Camera Acquisition
cd /repos/VimbaX_2023-patched/cti/
. SetGenTLPath.sh
source SetGenTLPath.sh 

#Now launch the viewer. Click on the camera and then click the Play button in the new window that appears. This can be used to set exposure time and other camera settings
#/repos/VimbaX_2023-patched/bin/VimbaXViewer

#Launch Camera Acquisition
cd /repos/aburn/usr/hub/camera_acquisition/br
./camera_acquisition

