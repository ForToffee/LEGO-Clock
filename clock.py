#!/usr/bin/env python

import time
import urllib3
import json
from neopixel import * 
import scrollphathd
from scrollphathd.fonts import font5x5
from gpiozero import Button, PWMOutputDevice 
import threading
from random import randint

BRIGHTNESS = 0.3
# LED strip configuration:
LED_COUNT      = 2      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 32     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

btnhead = Button(25)

lastID = 0      #most recent entry_id
urlRoot = "http://api.thingspeak.com/channels/1417/"

namesToRGB = {'red': [0xFF, 0, 0],
                'green': [0, 0x80, 0],
                'blue': [0, 0, 0xFF],
                'cyan': [0, 0xFF, 0xFF],
                'white': [0xFF, 0xFF, 0xFF],
                'warmwhite': [0xFD, 0xF5, 0xE6],
                'purple': [0x80, 0, 0x80],
                'magenta': [0xFF, 0, 0xFF],
                'yellow': [0xFF, 0xFF, 0],
                'orange': [0xFF, 0xA5, 0],
                'pink': [0xFF, 0xC0, 0xCB],
                'oldlace': [0xFD, 0xF5, 0xE6]}



#retrieve and load the JSON data into a JSON object
def getJSON(url):
    http = urllib3.PoolManager()
    jsonFeed = http.request('GET', urlRoot + url)
    feedData = jsonFeed.data.decode('utf-8')
    #print feedData
    jsonFeed.close()

    data = json.loads(feedData)
    return data

#use the JSON object to identify the colour in use,
#update the last entry_id processed
def parseColour(feedItem):
    global lastID
    
    for name in namesToRGB.keys():
        if feedItem["field1"] == name:
            ret = namesToRGB[name]    #add the colour to the head

    lastID = getEntryID(feedItem)
    return ret 
    
#read the last entry_id
def getEntryID(feedItem):
    return int(feedItem["entry_id"])

#show all pixels one colour
def showColour(c):
    for x in range(LED_COUNT):
        strip.setPixelColor(x, Color(c[1], c[0], c[2]))
    strip.show()

last_time = 0
def cycle():
    random_id = -1
    for x in range(0,2):
        for i,(k,v) in enumerate(namesToRGB.items()):
            showColour(v)
            time.sleep(0.5)
            if i == random_id:
                break
        random_id = randint(1,len(namesToRGB))
btnhead.when_pressed = cycle
    
while True:
    scrollphathd.clear()

    float_sec = (time.time() % 60) / 59.0
    seconds_progress = float_sec * 15
    scrollphathd.set_pixel(int(seconds_progress), 6, BRIGHTNESS)

    # Display the time (HH:MM) in a 5x5 pixel font
    scrollphathd.write_string(
        time.strftime("%H:%M"),
        x=0, # Align to the left of the buffer
        y=0, # Align to the top of the buffer
        font=font5x5, # Use the font5x5 font we imported above
        brightness=BRIGHTNESS # Use our global brightness value
    )

    if int(time.time()) % 2 == 0:
        scrollphathd.clear_rect(8, 0, 1, 5)
    scrollphathd.show()
    

    if time.time() - last_time > 15:
        data = getJSON("field/1/last.json")
        if getEntryID(data) > lastID:   #Has this entry_id been processed before?
            parseColour(data)
            showColour(parseColour(data))
        last_time = time.time()
    time.sleep(0.1)
