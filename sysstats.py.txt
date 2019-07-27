import uinterface, urequests, ujson, time, ntp, rgb, wifi, buttons, defines, system, machine
from default_icons import animation_connecting_wifi, icon_no_wifi

rgb.background((0,0,0))
rgb.clear()
rgb.framerate(1)

direction = 0
apps = []
current_index = 0
status = 0

rgb.setfont(1)

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
        print('No wifi')
        rgb.clear()
        rgb.framerate(20)
        data, frames = icon_no_wifi
        rgb.image(data, (12, 0), (8,8))
        time.sleep(3)
        rgb.clear()

def show_sensor_name(text):
    rgb.scrolltext(text, (255,255,255), (0,0), rgb.PANEL_WIDTH)

def show_sensor_value(text):
    rgb.text(text, (255,255,255), (0,0))

def clear():
    rgb.clear()

def render_current_sensor():
    global status
    status = 1
    clear()
    app = apps[current_index]
    show_sensor_name(app["SensorName"])
    time.sleep(5)
    status = 0
    clear()

if not wifi.status():
    print("Error connecting to wifi")
    system.reboot()

def input_B(pressed):
    global direction
    direction = defines.BTN_B

def input_up(pressed):
    global current_index
    if pressed:
        current_index = (current_index - 1) % len(apps)
        render_current_sensor()

def input_down(pressed):
    global current_index
    if pressed:
        current_index = (current_index + 1) % len(apps)
        render_current_sensor()

def get_data():
    global apps
    result = urequests.get('http://IP_ADDRESS:55555')
    apps = result.json()

buttons.register(defines.BTN_B, input_B)
buttons.register(defines.BTN_UP, input_up)
buttons.register(defines.BTN_DOWN, input_down)

get_data()

while direction != defines.BTN_B:
    if status != 1:
        clear()
        app = apps[current_index]
        show_sensor_value(app["SensorValue"])
        time.sleep(0.2)
    else:
        time.sleep(1)
