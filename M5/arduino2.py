import asyncio
import struct
import time
from bleak import BleakClient
from bleak import BleakScanner
import multiprocessing as mp
from pong import Pong

DEVICE_NAME = 'Second Nano 33 IoT'
GX_UUID = '00002104-0000-1000-8000-00805f9b34fb'

async def arduino2_BLE(gx1, gx2):
    print('Looking for ' + DEVICE_NAME + ' Peripheral Device...')

    found = False
    while True:
        devices = await BleakScanner.discover()
        for d in devices:     
            if d.name and DEVICE_NAME in d.name:
                print('Found ' + DEVICE_NAME + ' Peripheral')
                found = True
                async with BleakClient(d.address) as client:
                    print(f'Connected to {d.address}')

                    pong_proc = mp.Process(target=Pong, args=(gx1, gx2,))
                    pong_proc.start()

                    while True:
                        sensorByteVal = await client.read_gatt_char(GX_UUID)
                        gx2.value = struct.unpack('<f', sensorByteVal)[0]
                        
                        time.sleep(0.02)
                
                pong_proc.join()

        if found:
            break

def run_A2(gx1, gx2):
    asyncio.run(arduino2_BLE(gx1, gx2))