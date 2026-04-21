import ipaddress
import os
import ssl
import wifi
import socketpool
import adafruit_requests
import time
import gc
import sys
import random
import math
import time
import board
import busio
import digitalio
from adafruit_ra8875 import ra8875
from adafruit_ra8875.ra8875 import color565
import supervisor
import json 

COLORS = {
    "BLACK": color565(10, 0, 0),
    "RED": color565(255, 0, 0),
    "BLUE": color565(0, 0, 255),
    "GREEN": color565(0, 255, 0),
    "YELLOW": color565(255, 255, 0),
    "CYAN": color565(0, 255, 255),
    "MAGENTA": color565(255, 0, 255),
    "WHITE": color565(255, 255, 255),
}

LINE_HEIGHT = 15
QUOTE_MARGIN = 30
AUTHOR_MARGIN = 15
AVERAGE_CHAR_WIDTH = 8
HIGHLIGHT_SPACING = 0
MAX_X = 470
MAX_Y = 270
MAX_LINE_CHAR_COUNT = math.floor((MAX_X - (QUOTE_MARGIN * 2)) / AVERAGE_CHAR_WIDTH) #51

BACKGROUND_COLOR = COLORS[os.getenv("BACKGROUND_COLOR")]
TEXT_COLOR = COLORS[os.getenv("TEXT_COLOR")]
HIGHLIGHT_COLOR = COLORS[os.getenv("HIGHLIGHT_COLOR")]
MISSING_QUOTES = ["11:46", "12:31", "13:36", "18:44"]

DISPLAY_MERIDIEM = os.getenv("DISPLAY_MERIDIEM").lower() == "true"
USE_MILITARY_TIME = os.getenv("USE_MILITARY_TIME").lower() == "true"

def timeToDecimal(time):
    return float(time[0]) + (float(time[1]) / 60)
    
SCREEN_OFF_TIME = timeToDecimal([int(x) for x in os.getenv("SCREEN_OFF_TIME").split(":")])
SCREEN_ON_TIME = timeToDecimal([int(x) for x in os.getenv("SCREEN_ON_TIME").split(":")])

# Configuration for CS and RST pins:
cs_pin = digitalio.DigitalInOut(board.GP21)
rst_pin = digitalio.DigitalInOut(board.GP22)
int_pin = digitalio.DigitalInOut(board.GP1)

# Config for display baudrate (default max is 6mhz):
BAUDRATE = 6000000

# Setup SPI bus using hardware SPI:
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)

# Create and setup the RA8875 display:
display = ra8875.RA8875(spi, cs=cs_pin, rst=rst_pin, baudrate=BAUDRATE)
display.init()

# lowering the brightness causes buzzing noises.
#display.brightness(200)


# Get our username, key and desired timezone
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
aio_username = os.getenv("ADAFRUIT_AIO_USERNAME")
aio_key = os.getenv("ADAFRUIT_AIO_KEY")
timezone = os.getenv("TIMEZONE")
TIME_URL = f"https://io.adafruit.com/api/v2/{aio_username}/integrations/time/strftime?x-aio-key={aio_key}&tz={timezone}"
TIME_URL += "&fmt=%25Y-%25m-%25d+%25H%3A%25M%3A%25S.%25L+%25j+%25u+%25z+%25Z"


wifi.radio.stop_scanning_networks()
wifi.radio.connect(ssid, password)
print(f"Connected to {ssid}!")

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())


def incTime(lastTime) -> int:
    minutes = int(lastTime[1]) + 1
    if minutes == 60:
        minutes = 0
        lastTime[0] = str(int(lastTime[0]) + 1)
    lastTime[1] = str(minutes) if minutes > 9 else "0" + str(minutes)
    if lastTime[0] == 24:
        lastTime[0] = 0
    return lastTime

def getRemoteTime() -> list[str]:
    gc.collect()
    try:
        if not wifi.radio.ipv4_address:
            wifi.radio.stop_scanning_networks()
            wifi.radio.connect(ssid, password)
        response = requests.get(TIME_URL)
        splitDate = response.text.split(" ")
        splitTime = splitDate[1].split(":")
        return splitTime
    except:
        return ["", ""]

def getTime(timesRan, lastTime) -> tuple[list[str], float, int]:
    # get time every half hour to make sure we haven't crept
    sleepTime = 60
    timesRan = timesRan + 1
    if timesRan >= 15:
        print("Queried internet for time")
        queriedTime = getRemoteTime()
        if queriedTime[0] == "":
            print("failed getting remote time")
            if lastTime[0] == "":
                #display.fill(BACKGROUND_COLOR)
                #display.txt_set_cursor(100, math.floor(MAX_Y / 2))
                #display.txt_write("No internet connection")
                print("No internet connection")
                while queriedTime[0] == "":
                    queriedTime = getRemoteTime()
                    time.sleep(60)

            lastTime = incTime(lastTime)
        else:
            lastTime = queriedTime
            timesRan = 0
            sleepTime = 60 - float(lastTime[2])

    else:
        lastTime = incTime(lastTime)

    return lastTime, sleepTime, timesRan

def displayTime(lastTime) -> None:
    display.txt_trans(TEXT_COLOR)
    display.txt_size(0)
    time = ""

    hours = lastTime[0]
    if USE_MILITARY_TIME: 
        time = hours + ":" + lastTime[1]
    else: 
        meridiem = "a.m."
        if int(hours) == 0:
            hours = "12"
        elif int(hours) > 12:
            hours = str(int(hours) % 12)
            meridiem = "p.m."
            
        time = hours + ":" + lastTime[1] + (" " + meridiem if DISPLAY_MERIDIEM else "")

        if time[0] == "0":
            time = time[1:]
        
    display.txt_set_cursor(math.floor((MAX_X / 2) - ((AVERAGE_CHAR_WIDTH * len(time)) / 2)), 10)
    display.txt_write(time)

def checkIfReloadNeeded(time): 
    if time not in MISSING_QUOTES:
        # This is a goofy solution, but after running for a long time 
        # circuitpython seems to lose the ability to find files. 
        # It will not throw an error, it just can't find them anymore. 
        # if that happens, force a reload. 
        print("Reloading")
        supervisor.reload() 
    else: 
        print("Quote is known as missing") 
    
def getQuote(lastTime) -> None:
    quote = {
        "fullQuote": "No quote found for this time :( I'm sorry",
        "highlight": "I'm sorry",
        "book": "No book found",
        "author": ""
    }
 
    quotePath = "lib/quotes/" + lastTime[0] + "_" + lastTime[1] + ".json"
    try:
        # this will throw an OSError if path doesn't exist
        os.stat(quotePath)
            
        with open(quotePath, "r") as file:
            data = json.load(file)                    
            randQuoteInd = random.randint(0, len(data) - 1)
            quote = data[randQuoteInd]

    except OSError:
        # os.stat is kind of a dumb way to do this in circuitpython because 
        # it just throws an error if the file isn't found. 
        checkIfReloadNeeded(lastTime[0] + ":" + lastTime[1])
    except Exception as e:
        print(lastTime)
        print(e)
        quote["book"] = str(e)

    return quote

def splitQuote(quote) -> tuple[list[str], int, int]:
    REPLACE_STR = "%&%"
    quote["fullQuote"] = quote["fullQuote"].replace(quote["highlight"], REPLACE_STR)
    forcedLines = []

    highlightIndex = []
    highlightSubIndex = []
    tempChars = ""
    skipCount = 0
    addHighlight = False
    for i in range(len(quote["fullQuote"])):
        added = False

        if skipCount > 0:
            skipCount = skipCount - 1
        elif i < len(quote["fullQuote"]) - 3 and quote["fullQuote"][i : i + 4].lower() == "<br>":
            skipCount = 3
            added = True
        elif i < len(quote["fullQuote"]) - (len(REPLACE_STR) - 1) and quote["fullQuote"][i : i + len(REPLACE_STR)] == REPLACE_STR:
            skipCount = len(REPLACE_STR) - 1
            addHighlight = True
        elif quote["fullQuote"][i] == " ":
            nextSpace = -1
            for j in range(i + 1, len(quote["fullQuote"])):
                found = False 
                if quote["fullQuote"][j] == " ":
                    found = True 
                elif quote["fullQuote"][j] == "<" and j + 3 <= len(quote["fullQuote"]) - 1 and quote["fullQuote"][j : j + 4] == "<br>": 
                    found = True 
                
                # I think this needs to handle the case if REPLACE_STR was found while getting next space
                # to know the full length, but right now it is working and I don't think it should be. 
                if found: 
                    nextSpace = j - i
                    break
            if len(tempChars) + nextSpace > MAX_LINE_CHAR_COUNT or (nextSpace == -1 and len(tempChars) + len(quote["fullQuote"]) - i > MAX_LINE_CHAR_COUNT):
                added = True
            elif len(tempChars) > 0:
                tempChars = tempChars + " "
        else:
            tempChars = tempChars + quote["fullQuote"][i]

        if added and len(tempChars) > 0:
            forcedLines.append(tempChars)
            tempChars = ""
            
        if addHighlight:
            # if we can't fit it in this line then add to forcedLines
            if len(tempChars) + len(quote["highlight"]) + HIGHLIGHT_SPACING > MAX_LINE_CHAR_COUNT:
                forcedLines.append(tempChars)
                tempChars = ""

            highlightIndex.append(len(forcedLines))
            highlightSubIndex.append(len(tempChars) + math.floor(HIGHLIGHT_SPACING / 2))

            for j in range(len(quote["highlight"]) + HIGHLIGHT_SPACING):
                tempChars = tempChars + " "

            #forcedLines.append(quote["highlight"])
            addHighlight = False

    if len(tempChars) == 1:
        forcedLines[len(forcedLines) - 1] = forcedLines[len(forcedLines) - 1] + tempChars
    else:
        forcedLines.append(tempChars)

    return forcedLines, highlightIndex, highlightSubIndex


def displaySource(quote, lineLength) -> None:   
    author = "by " + quote["author"]
    authorWidth = len(author) * AVERAGE_CHAR_WIDTH
    
    title = "- " + quote["book"] 

    maxSourceCharWidth = math.floor((MAX_X - (2 * AUTHOR_MARGIN)) / AVERAGE_CHAR_WIDTH)
    
    if lineLength < 13:
        if len(title) >= maxSourceCharWidth:
            title = title[: maxSourceCharWidth - 3] + "..." 
            
        titleWidth = len(title) * AVERAGE_CHAR_WIDTH
    
        titleX = math.floor(MAX_X - AUTHOR_MARGIN - titleWidth)
        authorX = math.floor(MAX_X - AUTHOR_MARGIN - authorWidth - (2 * AVERAGE_CHAR_WIDTH))

        authorTitleCombX = max(AUTHOR_MARGIN, min(titleX, authorX))
        
        display.txt_set_cursor(authorTitleCombX, math.floor(MAX_Y - (LINE_HEIGHT * 2) - AUTHOR_MARGIN))
        display.txt_write(title)
        display.txt_set_cursor(authorTitleCombX + (2 * AVERAGE_CHAR_WIDTH), math.floor(MAX_Y - LINE_HEIGHT - AUTHOR_MARGIN))
        if author != "":
            display.txt_write(author)
    else:
        combo = title + " " + author
        if len(combo) >= maxSourceCharWidth:
            combo = title[: maxSourceCharWidth - len(author) - 4] + "... " + author 
            
        comboWidth = len(combo) * AVERAGE_CHAR_WIDTH
        
        comboX = max(0, math.floor(MAX_X - AUTHOR_MARGIN - comboWidth))
        display.txt_set_cursor(comboX, math.floor(MAX_Y - LINE_HEIGHT - AUTHOR_MARGIN))
        display.txt_write(combo)

def displayQuote(lastTime) -> None:
    quote = getQuote(lastTime)

    print("-" * 40)
    print(lastTime[0] + ":" + lastTime[1])
    print(quote["fullQuote"])
    print("-" * 40)

    forcedLines, highlightIndex, highlightSubIndex = splitQuote(quote)

    tempLineHeight = LINE_HEIGHT if len(forcedLines) < 13 else 14

    topPos = math.floor(MAX_Y / 2) - (len(forcedLines) / 2) * tempLineHeight

    for index, line in enumerate(forcedLines):
        display.txt_set_cursor(QUOTE_MARGIN, math.floor(topPos + (tempLineHeight * index)))
        if index in highlightIndex:
            display.txt_set_cursor(QUOTE_MARGIN, math.floor(topPos + (tempLineHeight * index)))
            display.txt_write(line)
        else:
            display.txt_write(line)

    for i in range(len(highlightIndex)):
        display.txt_trans(HIGHLIGHT_COLOR)
        display.txt_set_cursor(QUOTE_MARGIN + math.floor(highlightSubIndex[i] * AVERAGE_CHAR_WIDTH), math.floor(topPos + (tempLineHeight * highlightIndex[i])))
        display.txt_write(quote["highlight"])
        display.txt_trans(TEXT_COLOR)

    displaySource(quote, len(forcedLines))

timesRan = 61
lastTime = ["", ""]
lastScreenState = True
while True:
    display.fill_rect(0, 0, MAX_X + 20, MAX_Y + 20, BACKGROUND_COLOR)

    lastTime, sleepTime, timesRan = getTime(timesRan, lastTime)
    
    decimalCurrentTime = timeToDecimal(lastTime)
    
    if (decimalCurrentTime >= SCREEN_OFF_TIME) and (decimalCurrentTime <= SCREEN_ON_TIME):
        if lastScreenState:
            lastScreenState = False
            display.brightness(0)
            display.turn_on(False)
        print("Sleeping: ", sleepTime, " - ", lastTime)
        time.sleep(sleepTime)
        continue
    elif not lastScreenState:
        lastScreenState = True
        display.turn_on(True)
        display.brightness(255)

    displayTime(lastTime)
    displayQuote(lastTime)

    time.sleep(sleepTime)
