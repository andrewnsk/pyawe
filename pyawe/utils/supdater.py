import json
import pyowm
import serial
import sys
import time
import os.path
import logging
from time import time as tm
from pyawe import constants

__all__ = ["degree_to_rhumb", "rhumb_to_direction", "degree", "send_data"]


checker = True                      # update display, if first run
close_app = False
poll_interval = 3600                  # polling interval in seconds 3600 - 1 hour
init_time = int(tm())

device_file_name = "/dev/ttyUSB{0}"   # device file name in linux

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='system.log')

town = 'Norilsk'
area = 'ru'

########################
serial_port = '/dev/ttyUSB'
serial_baudrate = '9600'
serial_parity = 'N'
########################

owm = pyowm.OWM(constants.DEFAULT_API_KEY)

observation = owm.weather_at_place('{0},{1}'.format(town, area))
w = observation.get_weather()


def get_weather_wind_direction(mode=True):
    return str(degree(round(json.loads(json.dumps(w.get_wind()), 1)['deg']), mode))


def get_weather_wind_speed():
    return str(round(json.loads(json.dumps(w.get_wind()))['speed']))


def get_weather_temperature():
    return str(round(json.loads(json.dumps(w.get_temperature('celsius')))['temp']))


def get_weather_humidity():
    return int(round(json.loads(json.dumps(w.get_humidity()))))


def weather_wind():
    return "Ветер: " + get_weather_wind_direction() + " " + get_weather_wind_speed() + " м/с"


def weather_temp():
    return "Температура: " + get_weather_temperature()


def weather_humidity():
    return "Влажность: " + str(get_weather_humidity()) + " %"


def degree_to_rhumb(degrees):
    """
    convert degrees to rhumb
    :param degrees:
    """
    if degrees < 0 or degrees > 360:
        raise ValueError("degrees must be greater or equal than 0 and less than 361")
    i = int((degrees + 11.25) / 22.5)
    result_raw = i % 16
    return result_raw  # meteorological rhumb 1/16 of turn


def rhumb_to_direction(rhumb):
    """
    return direction
    :param rhumb:
    """
    if rhumb > 15 or rhumb < 0:
        raise ValueError("rhumb must be less than 16")
    directions = {0: "Северный",
                  1: "Северо-Северо-Восточный",
                  2: "Северо-Восточный",
                  3: "Восточный-Северо-Восточный",
                  4: "Восточный",
                  5: "Восточный-Юго-Восточный",
                  6: "Юго-Восточный",
                  7: "Юго-Юго-Восточный",
                  8: "Южный",
                  9: "Юго-Юго-Западный",
                  10: "Юго-Западный",
                  11: "Запад-Юго-Западный",
                  12: "Западный",
                  13: "Западно-Северо-Западный",
                  14: "Северо-Западный",
                  15: "Северо-Северо-Западный"}
    return directions[rhumb]


def degree(deg_val, mode=True):
    """
    Return direction of wind
    :param deg_val: degree value
    :param mode:    True - return absolute direction
                    False - return absolute direction in rhumb
    :return:
    """
    if mode:
        rhumb = degree_to_rhumb(deg_val)
        direction = rhumb_to_direction(rhumb)
    else:
        direction = degree_to_rhumb(deg_val)
    return direction


def send_data():
    ans = bytes("{temp} {wind} {winddir} {hum} \n".format(temp=get_weather_temperature(),
                                                          wind=get_weather_wind_speed(),
                                                          winddir=get_weather_wind_direction(mode=False),
                                                          hum=get_weather_humidity()), encoding="UTF-8")
    try:
        serial_instance = serial.serial_for_url(serial_port,
                                                serial_baudrate,
                                                parity=serial_parity,
                                                xonxoff=0,
                                                rtscts=0,
                                                do_not_open=True)
        serial_instance.dtr = False
        # serial_instance.rts = False
        serial_instance.open()
        time.sleep(5)  #
        serial_instance.write(ans)

    except serial.SerialException as e:
        sys.stderr.write('could not open port {}: {}\n'.format(repr(serial_port), e))
    return True


if __name__ == '__main__':
    logging.debug('search device')
    print('search device')
    for num_port in range(0, 6):

        if os.path.exists(device_file_name.format(num_port)):
            serial_port = device_file_name.format(num_port)
            device_file_name = device_file_name.format(num_port)
            print("Found: " + device_file_name.format(num_port))
            break
        if num_port == 5:
            print("not found")
            sys.exit(1)

    while not close_app:
        if int(tm()) > (init_time + poll_interval):
            checker = True
        else:
            if not os.path.exists(device_file_name):
                checker = True

        if checker & os.path.exists(device_file_name):
            time.sleep(5)
            print("{0} seconds pause".format(poll_interval))
            checker = False
            init_time = int(tm())
            try:
                if os.path.exists(device_file_name):
                    print('connected')
                    logging.debug('device connected')
                    send_data()
                else:
                    print("device not connected")

            except FileNotFoundError:
                print("not connected")
