import uinterface, urequests, ujson, ntp, rgb, wifi, buttons, defines, system, machine, gc
from default_icons import animation_connecting_wifi, icon_no_wifi

from time import sleep

rgb.background((0,0,0))
rgb.clear()
rgb.framerate(1)

WEATHER_API_SERVER = 'https://api.openweathermap.org/data/2.5/weather?id=2745726&mode=json&units=metric&appid=100135c6eb0eeba9bde50e165d4021c1'

action = 0
weather = None
last_update = 0
tick = 0

REFRESH_RATE = 310

rgb.setfont(0)

if not wifi.status():
    data, size, frames = animation_connecting_wifi
    rgb.clear()
    rgb.framerate(3)
    rgb.gif(data, (12, 0), size, frames)
    wifi.connect()
    if wifi.wait():
        rgb.clear()
        rgb.framerate(20)
    else:
        rgb.clear()
        rgb.framerate(20)
        data, frames = icon_no_wifi
        rgb.image(data, (12, 0), (8,8))
        sleep(3)
        rgb.clear()

def clear():
    rgb.clear()

if not wifi.status():
    print("Error connecting to wifi")
    system.reboot()

def input_B(pressed):
    global action
    if pressed:
        action = defines.BTN_B
    

def input_up(pressed):
    global action
    if pressed:
        action = defines.BTN_UP

def input_down(pressed):
    global action
    if pressed:
        action = defines.BTN_DOWN

buttons.register(defines.BTN_B, input_B)
buttons.register(defines.BTN_UP, input_up)
buttons.register(defines.BTN_DOWN, input_down)

while True:
    if not wifi.status():
        if not uinterface.connect_wifi():
            system.reboot()

    if tick < REFRESH_RATE:
        gc.collect()
        sleep(0.1)
        rgb.pixel((150, 150, 0), (int(round(tick / 10)), 7))
        tick += 1
        continue
    else:
        tick = 0

    result = urequests.get(WEATHER_API_SERVER)
    if result.status_code == 200:
        rgb.pixel((0, 255, 0), (31, 7))  # green for new data
        try:
            weather = result.json()
        except:
            rgb.pixel((255, 0, 0), (31, 7))  # red for error
    else:
        rgb.pixel((255, 0, 0), (31, 7))  # red for error
        rgb.text('E {}'.format(result.status_code))
        
    rgb.text(str(int(weather["main"]["temp"])), (255,255,255), (11,1))


system.reboot()
