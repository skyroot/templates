#!/bin/sh

mysqld &> /dev/null &

echo 

cd /app

echo 
echo "Running Server..."

php7 -S 0.0.0.0:80 &> /dev/null