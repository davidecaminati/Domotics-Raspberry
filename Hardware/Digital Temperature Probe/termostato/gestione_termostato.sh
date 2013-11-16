#!/bin/bash
ora=`date "+%H"`
camera=`redis-cli lrange camera -1 -1` 
cucina=`redis-cli lrange cucina -1 -1` 
rele=`redis-cli lrange rele -1 -1`
t_min_notte=`redis-cli get t_min_notte`
t_max_notte=`redis-cli get t_max_notte`
t_min_giorno=`redis-cli get t_min_giorno`
t_max_giorno=`redis-cli get t_max_giorno`
data_ora=`date "+%H:%M:%S"`
giorni[1]="lun"
giorni[2]="mar"
giorni[3]="mer"
giorni[4]="gio"
giorni[5]="ven"
giorni[6]="sab"
giorni[7]="dom"
gg_sett=`date "+%u"`
n_giorno=${giorni[$gg_sett]}
#ricavo la temperatura per l'ora corrente
temp_att=`redis-cli lindex ${n_giorno} ${ora}` 
#case "$temp_att" in
#N) echo "Programma attuale: notte"
#controllo="${data_ora} Temp camera= ${camera}     - Invariato - notte  - min ${t_min_notte}/max ${t_max_notte} - Temperature: ${camera}/${cucina}"
case "$temp_att" in
N) echo "Programma attuale: notte"
min=${t_min_notte}
max=${t_max_notte}
if (( `echo "$camera<${t_min_notte}" | bc -l` )) 
then
rele=1
controllo="${data_ora} Temp camera= ${camera} < ${t_min_notte} - notte - min ${t_min_notte}/max ${t_max_notte} - Temperature: ${camera}/${cucina}"
fi
if (( `echo "$camera>${t_max_notte}" | bc -l` )) 
then
rele=0
controllo="${data_ora} Temp camera= ${camera} > ${t_max_notte} - notte - min ${t_min_notte}/max ${t_max_notte} - Temperature: ${camera}/${cucina}"
fi
 ;;
G) echo "Programma attuale: giorno"
min=${t_min_giorno}
max=${t_max_giorno}
if (( `echo "$cucina<${t_min_giorno}" | bc -l` )) 
then
rele=1
controllo="${data_ora} Temp cucina= ${cucina} < ${t_min_giorno} - giorno - min ${t_min_giorno}/max ${t_max_giorno} - Temperature: ${camera}/${cucina}"
fi
if (( `echo "$cucina>${t_max_giorno}" | bc -l` )) 
then
rele=0
controllo="${data_ora} Temp cucina= ${cucina} > ${t_max_giorno} - giorno - min ${t_min_giorno}/max ${t_max_giorno} - Temperature: ${camera}/${cucina}"
fi
  ;;
S) echo "Programma attuale: spento"
min=0
max=0
controllo="${data_ora} Temp camera= ${camera},Temp cucina= ${cucina} - termo spento"
rele=0
  ;;
esac
/usr/bin/redis-cli rpush rele $rele > /dev/null
#echo "d4=$rele" | /usr/bin/telnet localhost 2000
if [ ! -d /sys/class/gpio/gpio25 ] 
then
  echo "25" > /sys/class/gpio/export
  echo "out" > /sys/class/gpio/gpio25/direction
fi
if [ $rele -eq 1 ] 
then 
echo "0" > /sys/class/gpio/gpio25/value
else
echo "1" > /sys/class/gpio/gpio25/value
fi
/usr/bin/redis-cli rpush controllo "$controllo"  > /dev/null
/usr/bin/redis-cli rpush min "$min" > /dev/null
/usr/bin/redis-cli rpush max "$max" > /dev/null
#echo "camera=${camera} cucina=${cucina}"
echo "Rele: $rele"
echo "Controllo: $controllo" 
