import scrollphathd as sphd
from gpiozero import Button, PWMOutputDevice 
import time
from signal import pause
import threading
from neopixel import *

piezo = PWMOutputDevice(18)
btntime = Button(17)
btnalarm = Button(27)
btnhour = Button(22)
btnmin = Button(24)
btnsw = Button(23)
btnhead = Button(25)

# LED strip configuration:
LED_COUNT      = 2      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()
        
pressed = False 
def press(pin):
    global pressed
    pressed = True

btntime.when_pressed =  press
btnalarm.when_pressed = press
#btnhour.when_pressed = press
#btnmin.when_pressed = press
#btnsw.when_pressed = press
btnhead.when_pressed = press

#pause()

bpm = 140
beat_duration = 1/(bpm/60)
print(beat_duration)
silent = False
def buzz(frequency, beats):
    if frequency > 0 and not silent:
        piezo.frequency = frequency
        piezo.value = 0.5
    time.sleep(beat_duration * beats )
    piezo.off()

def play_note(note, beats=1):
    freq = 0
    if note == 'C':
        freq = 262
    if note == 'D':
        freq = 294
    if note == 'E':
        freq = 330
    if note == 'F':
        freq = 349
    if note == 'G':
        freq = 392
    if note == 'A':
        freq = 440
    if note == 'B':
        freq = 494
    if note == 'C5':
        freq = 523
    if note == 'D5':
        freq = 587
    if note == 'E5':
        freq = 659
    if note == 'F5':
        freq = 698
    if note == 'G5':
        freq = 783
    buzz(freq,beats)


text = ""
threadrun = True
def show_text():
    global threadrun
    threadrun = True
    while threadrun:
        last_text = ""
        if text != last_text:
            sphd.clear()
            sphd.write_string(text, brightness=0.5)
            sphd.show()
            last_text = text


x = Color(0,0,0)
r = Color(0,128,0)
g = Color(128,0,0)
b = Color(0,0,128)
y = Color(128,128,0)
c = Color(0,128,128)
m = Color(128,128,0)
w = Color(128,128,128)
eyes = [x,x]
def show_eyes_worker():
    last_eyes = [-1,-1]
    while True:
        if last_eyes != eyes:
            show_eyes()
            last_eyes = eyes
            time.sleep(0.01)

def show_eyes():
    global strip
    #print("show_eyes")
    strip.setPixelColor(0, eyes[0])
    strip.setPixelColor(1, eyes[1])
    strip.show()
 
            
def birthday_tune():
    global text, threadrun, eyes
    t = threading.Thread(target=show_text)
    t.start()

    text = "Hap"
    eyes=[b,b]
    play_note('G')
    time.sleep(0.01)
    text = "py"
    play_note('G')
    eyes=[g,g]
    text = "Bth"
    play_note('A')
    text = "day"
    play_note('G')
    eyes=[r,r]
    text = "to"
    play_note('C5')
    eyes=[m,m]
    text = "you"
    play_note('B')
    play_note('')

    text = "Hap"
    eyes=[b,b]
    play_note('G')
    time.sleep(0.01)
    text = "py"
    play_note('G')
    eyes=[g,g]
    text = "Bth"
    play_note('A')
    text = "day"
    play_note('G')
    eyes=[r,r]
    text = "to"
    play_note('D5')
    eyes=[m,m]
    text = "you"
    play_note('C5')
    play_note('')

    text = "Hap"
    eyes=[b,b]
    play_note('G')
    time.sleep(0.01)
    text = "py"
    play_note('G')
    text = "Bth"
    eyes=[g,g]
    play_note('G5')
    text = "day"
    play_note('E5')
    time.sleep(0.01)

    text = "Dear"
    eyes=[r,r]
    play_note('C5')
    text = "AL"
    eyes=[w,w]
    play_note('B',1.25)
    text = " EX"
    play_note('A',1.25)
    play_note('')

    text = "Hap"
    eyes=[b,b]
    play_note('F5')
    time.sleep(0.01)
    text = "py"
    play_note('F5')
    time.sleep(0.01)
    text = "Bth"
    eyes=[g,g]
    play_note('E5')
    text = "day"
    play_note('C5')
    text = "to"
    eyes=[r,r]
    play_note('D5')
    text = "you"
    eyes=[m,m]
    play_note('C5')

    threadrun=False
    t.join()
    eyes=[y,y]
    bat_signal(5)
    eyes =[x,x]
def batman_tune():
    global text, threadrun, eyes
    t = threading.Thread(target=show_text)
    t.start()
    for n in range(0,2):
        text = "Na"
        eyes=[x,b]
        buzz(147, 0.5) # D
        text = " Na"
        eyes=[b,x]
        buzz(147, 0.5)
        text = "Na"
        eyes=[x,c]
        buzz(139, 0.5) # C#
        text = " Na"
        eyes=[c,x]
        buzz(139, 0.5)
        text = "Na"
        eyes=[x,g]
        buzz(131, 0.5) # C
        text = " Na"
        eyes=[g,x]
        buzz(131, 0.5)
        text = "Na"
        eyes=[x,y]
        buzz(139, 0.5) # C#
        text = " Na"
        eyes=[y,x]
        buzz(139, 0.5)
    text = "Bat"
    eyes=[r,r]
    buzz(175, 0.5)  # F
    buzz(0, 0.5)
    text = "MAN"
    eyes=[m,m]
    buzz(175, 1)    # 370
    eyes=[x,x]

    threadrun=False
    t.join()
    
def bat_signal(wait=0):
    img = [
        "11100110101100111",
        "10001110001110001",
        "00000100000100000",
        "00000000000000000",
        "00000000000000000",
        "10001110001110001",
        "11100111011100111"]
    sphd.clear()
    for y in range(0,7):
        for x in range(0,17):
            if img[y][x] == "0":
                sphd.set_pixel(x,y,0.5)
    sphd.show()  
    if wait == 0:
        while pressed == False:
            time.sleep(0.1)
    else:
        time.sleep(wait)

# Auto scroll using a while + time mechanism (no thread)
eyes = [r,r]
show_eyes()
n = threading.Thread(target=show_eyes_worker)
n.start()
reset = True
val = 0
diff = 10
while True:
    global pressed, reset 

    try:
        if reset:
            sphd.clear()
            sphd.write_string(" I'm Batman!  Happy Birthday Alex ", brightness=0.5)
            reset = False 
        while pressed == False:
            # Show the buffer
            sphd.show()
            # Scroll the buffer content
            sphd.scroll()

            val += diff
            if val > 127:
                diff = diff * -1
            if val < 0:
                val = 0
                diff = diff * -1
                
            eyes = [Color(val,val,val), Color(val,val,val)]
            # Wait for 0.1s
            time.sleep(0.1)
        pressed = False 
        if btntime.is_pressed:
            batman_tune()
        if btnhead.is_pressed:
            birthday_tune()
        if btnalarm.is_pressed:
            bat_signal()
    except KeyboardInterrupt:
        eyes = [x,x]
        break
    except:
        print("oops")
 
    pressed = False 
    reset = True



