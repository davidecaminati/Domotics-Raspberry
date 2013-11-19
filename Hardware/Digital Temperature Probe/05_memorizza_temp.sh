#!/bin/bash
sensore[0]='28-0000047b16f9'
#sensore[1]='28-0000047b16f9'
#sensore[2]='28-0000047b16f9'
#esterna=`/usr/bin/elinks -dump "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IFCCESEN1&format=1"|awk -F "," '{print $2}'| grep '[0-9]\.[0-9]'| tail -1`
#esterna=`/usr/bin/elinks -dump "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IITALIAB2&format=1"|awk -F "," '{print $2}'| grep '[0-9]\.[0-9]'| tail -1`

#IFCCESEN1
d_sensore[0]='cucina'
#d_sensore[1]='camera'
#d_sensore[2]='camerina'
y=0
for i in "${sensore[@]}"
do
 temp=`/root/termostato/04_leggi_temperatura.sh $i`
 if [ "$temp" != "-0.062" ]
  then
  if [ "$temp" != "85" ]
   then
    /usr/bin/redis-cli rpush ${d_sensore[${y}]} $temp
#     /usr/bin/redis-cli rpush ${d_sensore[${y}]} 27
  fi
 fi
y=`expr $y + 1` 
done
#/usr/bin/redis-cli rpush temp_esterna $esterna
/usr/bin/redis-cli rpush lettura "`date "+%Y-%m-%d %H:%M:%S"`"
/usr/bin/redis-cli rpush timestamp "`date "+%s"`"
