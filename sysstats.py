import uinterface, urequests, ujson, time, ntp, rgb, wifi, buttons, defines, system, machine
from default_icons import animation_connecting_wifi, icon_no_wifi

rgb.background((0,0,0))
rgb.clear()
rgb.framerate(1)

REMOTE_STATS_SERVER = 'http://204.2.68.149:55555'

direction = 0
apps = []
current_index = 1
status = 0
last_update = 0

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

def show_sensor_value(name, value):
    rgb.text(name, (255,255,255), (0,1))
    rgb.text(value, (255,255,255), (23,1))

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
        result = urequests.get(REMOTE_STATS_SERVER)
        if result.status_code == 200:
            rgb.pixel((0, 255, 0), (31, 7))  # green for new data
            try:
                apps = result.json()
            except:
                rgb.pixel((255, 0, 0), (31, 7))  # red for error
        else:
            rgb.pixel((255, 0, 0), (31, 7))  # red for error
            rgb.text('E {}'.format(result.status_code))
        

buttons.register(defines.BTN_B, input_B)
buttons.register(defines.BTN_UP, input_up)
buttons.register(defines.BTN_DOWN, input_down)

get_data()

while direction != defines.BTN_B:
    print(last_update)
    if status != 1:
        if last_update > 30:
            last_update = 0
            #get_data()
            clear()
            app = apps[current_index]
            show_sensor_value(app["SensorName"], "{0:.0f}".format(time.time()))
        else:
            last_update += 1
        time.sleep(0.1)
    else:
        time.sleep(0.1)

system.reboot()
