import uinterface, urequests, ujson, time, ntp, rgb, wifi, buttons, defines, system, machine
from default_icons import animation_connecting_wifi, icon_no_wifi

rgb.background((0,0,0))
rgb.clear()
rgb.framerate(1)

direction = 0
apps = []
current_index = 0
status = 0
last_update = 0

rgb.setfont(0)

if not wifi.status():
    data, size, frames = animation_connecting_wifi
    rgb.clear()
    rgb.framerate(3)
    rgb.gif(data, (12, 0), size, frames)
    wifi.connect()
    if wifi.wait():
        if not ntp.set_NTP_time():
            print("Error setting time")
            system.reboot()
        print("First ts: " + str(time.time()))
        last_update = time.time()
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
    global status, apps
    status = 1
    clear()
    app = apps[current_index]
    show_sensor_name(app["SensorName"])
    time.sleep(3)
    status = 0

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
    if wifi.wait():
        result = urequests.get('http://204.2.68.149:55555')
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
        if time.time() - last_update > 30:
            last_update = time.time()
            get_data()
        time.sleep(0.2)
    else:
        time.sleep(0.2)

system.reboot()
