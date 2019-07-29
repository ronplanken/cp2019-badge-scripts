import uinterface, urequests, ujson, ntp, rgb, wifi, buttons, defines, system, machine, gc
from default_icons import animation_connecting_wifi, icon_no_wifi

from time import sleep

rgb.background((0,0,0))
rgb.clear()
rgb.framerate(20)

WEATHER_API_SERVER = 'https://api.openweathermap.org/data/2.5/weather?id=2745726&mode=json&units=metric&appid=100135c6eb0eeba9bde50e165d4021c1'

action = 0
weather = None
last_update = 0
tick = 0

REFRESH_RATE = 31

rgb.setfont(0)

def disconnect_wifi():
    if wifi.status():
        wifi.disconnect()
        rgb.pixel((255, 0, 0), (31, 0))  # red for no wifi

def connect_wifi():
    rgb.pixel((255, 255, 0), (31, 0))  # yellow connecting to wifi
    if not wifi.status():
        wifi.connect()
        if wifi.wait():
            rgb.pixel((0, 255, 0), (31, 0))  # green for wifi
            rgb.framerate(20)
        else:
            rgb.clear()
            rgb.framerate(20)
            data, frames = icon_no_wifi
            rgb.image(data, (12, 0), (8,8))
            time.sleep(3)
            rgb.clear()
            machine.reboot()
        

def clear():
    rgb.clear()

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

gc.collect()

while True:
    if tick < REFRESH_RATE:
        gc.collect()
        sleep(0.1)
        rgb.pixel((150, 150, 0), (int(round(tick)), 7))
        tick += 1
        continue
    else:
        tick = 0

    try:
        connect_wifi()
        print('retrieving result')
        result = urequests.get(WEATHER_API_SERVER)
        disconnect_wifi()
        if result.status_code == 200:
            rgb.pixel((0, 255, 0), (31, 7))  # green for new data
            try:
                print(gc.mem_free())
                weather = result.json()
            except:
                print('Error during json parse')
                print(result.text())
                rgb.pixel((255, 0, 0), (31, 7))  # red for error
        else:
            print('Status: ' + result.status_code)
            rgb.pixel((255, 0, 0), (31, 7))  # red for error
            rgb.text('E {}'.format(result.status_code))
    except Exception as e:
        text = str(e)
        print(text)
        wifi.disconnect()
        rgb.pixel((255, 0, 0), (31, 0))  # red for error
        rgb.setfont(1)
        rgb.text('No wifi')
        sleep(10)
        
    
    rgb.text(str(int(weather["main"]["temp"])), (255,255,255), (11,1))
