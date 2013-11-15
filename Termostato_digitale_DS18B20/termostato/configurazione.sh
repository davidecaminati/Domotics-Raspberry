#!/bin/bash
for x in `seq 0 6`
do
 redis-cli rpush lun N
 redis-cli rpush mar N
 redis-cli rpush mer N
 redis-cli rpush gio N
 redis-cli rpush ven N
 redis-cli rpush sab N
 redis-cli rpush dom N
done
for x in `seq 7 23`
do
 redis-cli rpush lun G
 redis-cli rpush mar G
 redis-cli rpush mer G
 redis-cli rpush gio G
 redis-cli rpush ven G
 redis-cli rpush sab G
 redis-cli rpush dom G
done
redis-cli lrange lun 0 23
redis-cli lrange mar 0 23
redis-cli lrange mer 0 23
redis-cli lrange gio 0 23
redis-cli lrange ven 0 23
redis-cli lrange sab 0 23
redis-cli lrange dom 0 23
redis-cli set t_min_giorno 21
redis-cli set t_max_giorno 21.5
redis-cli set t_min_notte 21
redis-cli set t_max_notte 21.5
redis-cli get t_min_giorno 
redis-cli get t_max_giorno 
redis-cli get t_min_notte
redis-cli get t_max_notte 
redis-cli lpush rele 0 
redis-cli lrange rele 0 -1 
redis-cli lpush timestamp 0 
redis-cli lrange timestamp 0 -1 
redis-cli rpush min 0
redis-cli rpush max 0
redis-cli lrange min 0 -1 
redis-cli lrange max 0 -1
