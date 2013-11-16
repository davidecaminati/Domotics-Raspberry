#!/bin/bash
temp=`/usr/bin/elinks -dump "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IITALIAB2&format=1"|awk -F "," '{print $2}'| grep '[0-9]\.[0-9]'| tail -1`
/usr/bin/redis-cli rpush temp_esterna $temp
