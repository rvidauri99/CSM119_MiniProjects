'''
What: Connecting to arduino nano 33 IoT using bluetooth on laptop/desktop
Where: https://create.arduino.cc/projecthub/sridhar-rajagopal/control-arduino-nano-ble-with-bluetooth-python-331e33?ref=part&ref_id=108462&offset=11
Why: Professor JS version was not working for me so I had to find an alternative with Python.
'''

import asyncio
import struct
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import multiprocessing as mp

from bleak import BleakClient
from bleak import BleakScanner

uuid_value = '13012F01-F8C3-4F4A-A8F4-15CD926DA146'


def update_plot(interval, ns):
    time = ns.df.loc[:,'time']
    ax = ns.df.loc[:,'ax']
    plt.xlabel('Time')
    plt.ylabel('IMU AX')
    plt.plot(time, ax, label='ax')


def show_new_plot(ns):
    ani = FuncAnimation(plt.gcf(), update_plot, fargs=(ns,), interval=10)
    plt.show()  


async def run(ns):
    print('Looking for Rod Nano 33 IoT Peripheral Device...')

    found = False
    devices = await BleakScanner.discover()
    for d in devices:     
        if d.name and 'Rod Nano 33 IoT' in d.name:
            print('Found Rod Nano 33 IoT Peripheral')
            found = True
            async with BleakClient(d.address) as client:
                print(f'Connected to {d.address}')
                while True:
                    sensorByteVal = await client.read_gatt_char(uuid_value)
                    sensorVal = struct.unpack('<f', sensorByteVal)[0]
                    print(sensorVal)
                    data = {'time': [time.time()], 'ax': [sensorVal]}
                    row = pd.DataFrame(data)
                    ns.df = pd.concat([ns.df, row], ignore_index=True)
                    ns.df.reset_index()
                    time.sleep(0.02)               

    if not found:
        print('Could not find Arduino Nano 33 IoT')



if __name__ == "__main__":
    try:
        manager = mp.Manager()
        ns = manager.Namespace()
        ns.df = pd.DataFrame(columns=['time', 'ax'])

        graphing = mp.Process(target=show_new_plot, args=(ns,))

        graphing.start()
        asyncio.run(run(ns))
        graphing.join()
        
    except KeyboardInterrupt:
        print('\nReceived Keyboard Interrupt')
    finally:
        print('Program finished')
        