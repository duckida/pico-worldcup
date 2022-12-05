import network
import urequests as requests
import time
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
#from dateutil.parser import parse
import json

ssid = 'Oasis'
password = 'N2S2LivingInUK@Now!'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)
display.set_backlight(0.6)

button_x = Button(14)
button_y = Button(15)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)
PITCH = display.create_pen(46, 209, 48)

# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(PITCH)
    display.clear()
    display.update()

index = 0
#length = 0


def displayScore():
    clear()
    
    request = requests.get("https://worldcupjson.net/matches/today")
    decoded = json.loads(request.content)
    global length
    length = len(decoded)
    #print(length)
    match = decoded[index]
    hCountry = match['home_team']['country']
    hScore = match['home_team']['goals']

    aCountry = match['away_team']['country']
    aScore = match['away_team']['goals']
    
    completed = match['status']
    if hScore != None:
        display.set_pen(WHITE)
        display.text(hCountry, 10, 20, 240, 4)
        display.text(str(hScore), 30, 60, 240, 6)

        display.text("vs", 100, 20, 240, 4)

        display.text(aCountry, 160, 20, 240, 4)
        display.text(str(aScore), 182, 60, 240, 6)
        if completed == 'completed':
           display.text('Final Score', 38, 102, 240, 3) 
    else:
        display.set_pen(WHITE)
        display.text(hCountry, 10, 20, 240, 4)

        display.text("vs", 100, 20, 240, 4)

        display.text(aCountry, 160, 20, 240, 4)
        display.text("Not Started", 43, 60, 3, 4)
        
    display.update()

displayScore()

while True:
     
    if button_x.read():
        print(index)
        print(length)
        if index == int(length-1):
            index = 0
            displayScore()
        else:
            index += 1
            displayScore()
            
    if button_y.read():
        displayScore()

