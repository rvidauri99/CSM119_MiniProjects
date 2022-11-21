import multiprocessing as mp
import asyncio
from arduino1 import arduino1_BLE

if __name__ == "__main__":
    
    manager = mp.Manager()
    gx1 = manager.Value('d', 0.0)
    gx2 = manager.Value('d', 0.0)

    try:
        asyncio.run(arduino1_BLE(gx1, gx2))
    except KeyboardInterrupt:
        print('\nReceived Keyboard Interrupt')
    finally:
        print('Program finished')
