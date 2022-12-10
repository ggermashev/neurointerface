import time

import serial
import matplotlib.pyplot as plt
import numpy as np

import bluetooth
from bluetooth.btcommon import Protocols

def whats_nearby():
    name_by_addr = {}
    nearby = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
    for bd_addr in nearby:
        #name = bluetooth.lookup_name(bd_addr, 5)
        print(bd_addr[0], bd_addr[1], bd_addr[2])
        name_by_addr[bd_addr] = bd_addr[1]
    return name_by_addr


def what_services(addr, name):
    # print(" %s - %s" % (addr, name))
    # if (addr == "20:14:08:26:02:80"):
    for services in bluetooth.find_service(address=addr, name=name):
        print("\t Name:           %s" % (services["name"]))
        print("\t Description:    %s" % (services["description"]))
        print("\t Protocol:       %s" % (services["protocol"]))
        print("\t Provider:       %s" % (services["provider"]))
        print("\t Port:           %s" % (services["port"]))
        print("\t service-classes %s" % (services["service-classes"]))
        print("\t profiles        %s" % (services["profiles"]))
        print("\t Service id:  %s" % (services["service-id"]))
        print("")


def read_blue():
    server = "20:14:08:26:02:80"
    port = 3
    backlog = 1
    size = 1024
    s = bluetooth.BluetoothSocket()
    print(s)
    s.bind((server, port))
    s.listen(backlog)
    try:
        client, clientInfo = s.accept()
        while 1:
            data = client.recv(size)
            if data:
                print(data)
                client.send(data)  # Echo back to client
    except:
        print("Closing socket")
        client.close()
        s.close()


def socket():
    import socket

    baddr = '20:14:08:26:02:80'
    channel = 3
    with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as s:
        s.connect((baddr, channel))
        data = s.recv(1024)
        print("received [%s]" % data)


socket()

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
