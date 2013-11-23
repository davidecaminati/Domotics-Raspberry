#!/bin/bash
sensore[0]='28-0000047b16f9'
d_sensore[0]='my_room_1'
ts_sensore[0]='my_room_1_ts'


y=0
for i in "${sensore[@]}"
do
 set_execute=`chmod +x  /home/pi/Domotics-Raspberry/Hardware/Digital\ Temperature\ Probe/02_read_temp_from_probe.sh`
 temp=`/home/pi/Domotics-Raspberry/Hardware/Digital\ Temperature\ Probe/02_read_temp_from_probe.sh $i`

 /usr/bin/redis-cli -h 192.168.0.208 rpush ${d_sensore[${y}]} $temp
 /usr/bin/redis-cli -h 192.168.0.208 rpush ${ts_sensore[${y}]} "`date "+%Y-%m-%d %H:%M:%S"`"
 y=`expr $y + 1` 
done

