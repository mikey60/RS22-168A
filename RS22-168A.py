#!/bin/python
# Thanks to https://github.com/Ostheer/Voltcraft_ME-32_RS-232 for their progam that I used as a starting point.
# Mike Secord 02-03-2021
# Program that displays, saves to CSV file and plots the Radio Shack RS22-168A meter readings
#     using the RS232 port.  I actually use a CH340 USB to serial Cable.  
# The correct serial port must be specified.
# User can change the sample_time in integer seconds.  The time is not exact using this method.
# Program overwrites the CSV file and plot image file if they already exist.
# Ctrl-c stops the program and displays the plot.  User must close plot to end the program.

serial_port = 'COM5'
sample_time = 1  # sample time in  integer seconds
import serial  # pip3 install pyserial
import time
import matplotlib.pyplot as plt  # pip3 install matplotlib
import numpy as np
f = open("data.txt", "wt")
try:
    ser = serial.Serial(port=serial_port,
                        baudrate=1200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_TWO,
                        bytesize=serial.SEVENBITS,
                        timeout=1,
                        rtscts=False,
                        dsrdtr=False,
                        xonxoff=False)
    ser.setRTS(False)
    ser.setDTR(True)
except serial.SerialException:
    print("failed to connect")
    ser.close()
    raise SystemExit



vals = []
ts = []
t0 = time.time()
i = 0

while True:
    try:
        ser.write("D".encode("utf-8"))
        recv = ser.read(14)
        recv = recv.decode("utf-8")
        recv = recv.split(" ")
        for i,r in reversed(list(enumerate(recv))):
            if len(r) == 0:
                del recv[i]
                
        mode = recv[0].strip()
        try:
            val = str(float(recv[1]))
            vals.append(float(val))
        except ValueError:
            vals.append(np.nan)
        unit = recv[-1].strip()
        t = str(int(time.time()-t0))
        ts.append(int(time.time()-t0))
        #print(time.ctime(time.time()), recv)
        print(t, val, unit+mode)
        f.write(t + "," + val + "," + unit+mode + "\r\n")
        i = i + 1
        time.sleep(sample_time -0.5)
    except KeyboardInterrupt:
        ser.close()
        f.close()
        plt.figure(1)
        plt.plot(ts, vals, linewidth=1.0)
        plt.xlabel("Time (sec)")
        plt.ylabel(unit+mode)
        plt.grid(True)
        plt.title("Meter Reading Plot")
        plt.savefig("data_plot")
        plt.show() 
        break
    except serial.SerialException:
        ser.close()
        break
    except IndexError:
        print("Could not parse input. Is the DMM turned on?")
        pass

