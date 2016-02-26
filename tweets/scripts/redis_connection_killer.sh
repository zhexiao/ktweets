#!/bin/bash
# This bash is aim to remove dead redis connection


# clear

SERVER_ADDRESS="127.0.0.1"


# loop
while true
do

c1=$(redis-cli client list | grep cmd=subscribe | grep  $SERVER_ADDRESS | cut -d ' ' -f 1 | cut -d '=' -f 2 | awk '{print "CLIENT KILL ID " $0}' | wc -l)
# if connection more than 100
if [ "$c1" -gt "100" ]
    then
        redis-cli client list | grep cmd=subscribe | grep  $SERVER_ADDRESS | cut -d ' ' -f 1 | cut -d '=' -f 2 | awk '{print "CLIENT KILL ID " $0}' | redis-cli -x
fi


echo $c1

# exec this script each 600 seconds
sleep 600
done
