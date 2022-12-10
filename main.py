import time

import serial
import matplotlib.pyplot as plt
import numpy as np


def serial_port():
    ser = serial.Serial('COM4', timeout=1)
    sum = 0
    n = 1
    count = 0
    while (1):
        arr = []
        count += 1
        sum = 0
        for i in range(n):
            res = ser.read(50000)
            res = list(res)
            print(res)
            furie_arr = np.fft.fft(res)
            arr = np.hstack([arr, np.abs(furie_arr)])
            print(len(furie_arr))
            sum += len(furie_arr)
        freq = np.fft.fftfreq(len(arr), n/sum)
        plt.plot(freq, arr)
        plt.savefig(f"./mixed/{count}.png")
        plt.show()
    ser.close()


serial_port()
