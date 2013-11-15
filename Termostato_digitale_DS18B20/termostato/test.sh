#!/bin/bash
echo "Visualizzazione elementi lista in redis"
redis-cli keys "*"
echo "Display valori lista primo sensore: cucina"
redis-cli lrange cucina -10 -1
echo "Display valori lista primo sensore: camera"
redis-cli lrange camera -10 -1
echo "Display valori lista temperatura esterna"
redis-cli lrange temp_esterna -10 -1
