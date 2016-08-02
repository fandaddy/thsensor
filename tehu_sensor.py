#!usr/bin/python
#  -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time
import urllib
import urllib2
import json

# 基本设置
channel = 18

#POST函数，提交数据
def http_post(temprature, humidity):
    url = 'http://api.heclouds.com/devices/{device_id}/datapoints'
    values = {"datastreams":[{"id":"temperature","datapoints":[{"value":temperature}]}, {"id":"humidity","datapoints":[{"value":humidity}]}]}
    jdata = json.dumps(values)
    req = urllib2.Request(url, jdata)
    req.add_header("api-key","Ur api key")
    response = urllib2.urlopen(req)
    return response.read()

check = 0
tmp = 1

data = []
j = 0

GPIO.setmode(GPIO.BCM)
time.sleep(1)
GPIO.setup(channel, GPIO.OUT)
GPIO.output(channel, GPIO.LOW)
time.sleep(0.02)
GPIO.output(channel, GPIO.HIGH)
for i in range(3):
    m = 1
GPIO.setup(channel, GPIO.IN)
while GPIO.input(channel) == GPIO.HIGH:
    continue
while GPIO.input(channel) == GPIO.LOW:
    continue
while GPIO.input(channel) == GPIO.HIGH:
    continue

while j < 40:
    k = 0
    while GPIO.input(channel) == GPIO.LOW:
        continue
    while GPIO.input(channel) == GPIO.HIGH:
        k += 1
        if k > 100:
            break
    if k < 8:
        data.append(0)
    else:
        data.append(1)
        j += 1

humidity_bit = data[0:8]
humidity_point_bit = data[8:16]
temperature_bit = data[16:24]
temperature_point_bit = data[24:32]
check_bit = data[32:40]

humidity = 0
humidity_point = 0
temperature = 0
temperature_point = 0

for i in range(8):
    humidity += humidity_bit[i] * 2 ** (7-i)
    humidity_point += humidity_point_bit[i] * 2 ** (7-i)
    temperature += temperature_bit[i] * 2 ** (7-i)
    temperature_point += temperature_point_bit[i] * 2 ** (7-i)
    check += check_bit[i] * 2 ** (7-i)

tmp = humidity + humidity_point + temperature + temperature_point
if check == tmp:
    resp = http_post(temperature, humidity)
    print resp
else:
    print "wrong"

GPIO.cleanup()


