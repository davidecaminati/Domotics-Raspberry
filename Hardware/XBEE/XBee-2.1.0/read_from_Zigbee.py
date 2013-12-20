##Configure XBEE on Raspberry#
##http://cae2100.wordpress.com/2012/12/23/raspberry-pi-and-the-serial-port/#
#    sudo nano /etc/inittab
#        #remark this line putting a # in front of the line#
#        #T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100 
#    sudo nano  /boot/cmdline.txt
#        #The contents of the file look like this#
#        dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait
#        #Remove all references to ttyAMA0 (which is the name of the serial port). The file will now look like this#
#        dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait
#        sudo reboot
#    #test serial port#
#        sudo apt-get install minicom
#        #Now run up minicom on the Raspberry Pi using#
#        minicom -b 9600 -o -D /dev/ttyAMA0 
#    #for usage python#
#    #https://pypi.python.org/pypi/XBee#
#        cd ~/Domotics-Raspberry/Hardware/XBEE/XBee-2.1.0
#        sudo python setup.py install
#        sudo pip install pyserial
#    #http://jeffskinnerbox.wordpress.com/2013/01/30/configuration-utilities-for-xbee-radios/#
#    #http://blog.james147.net/xbee-configuration/#
#    #http://tutorial.cytron.com.my/2012/03/08/xbee-series-2-point-to-point-communication/#
    
    
import serial
from xbee import ZigBee
serial_port = serial.Serial('/dev/ttyAMA0', 9600)
xbee = ZigBee(serial_port)
x = 0
while True:
    try:
        dati = xbee.wait_read_frame()
        rf_data = dati['rf_data']
        int_rf_data = ord(rf_data[5:6])
        print int_rf_data
        x = x+1
        print x
    except KeyboardInterrupt:
        break
serial_port.close()