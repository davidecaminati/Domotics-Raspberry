#!/bin/bash
esterna=`/usr/bin/elinks -dump "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IFCCESEN1&format=1"|awk -F "," '{print $2}'| grep '[0-9]\.[0-9]'| tail -1`
/usr/bin/redis-cli -h 192.168.0.208 rpush temp_ext $esterna
/usr/bin/redis-cli -h 192.168.0.208 rpush temp_ext_ts "`date "+%s"`"
/usr/bin/redis-cli -h 192.168.0.208 rpush timestamp "`date "+%s"`"