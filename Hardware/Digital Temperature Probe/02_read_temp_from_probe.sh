#!/bin/bash
#sensori[0]='28-0000047b16f9'
#sensori[1]='28-0000047b16f9'
#controllo che lo script venga lanciato con 1 parametro
if [ $# != 1 ]
 then
 echo -n "Lancia lo script: $0 [all"
 for i in "${sensori[@]}"
 do
   echo -n "|$i"
 done
 echo ']'
else 
 if [ $1 == "all" ] # Se lanciato con il parametro all visualizza la lettura di tutti i sensori
 then
  for i in "${sensori[@]}"
  do
    $0 $i 
  done
 else
 sensore=$1

 for x in 1 2 3 4
 do
  lettura=`paste -s /sys/bus/w1/devices/${sensore}/w1_slave | grep YES` # esegue la lettura verificando il CRC
  #echo $?
  #echo $lettura
  if [ $? == 0 ]
   then temp=$lettura; break
   else temp='ERR' ; break
  fi
 done

 temperatura=`echo $temp | paste -s | awk -F "=" '{print $3/1000}'`

 echo $temperatura
 fi
fi
