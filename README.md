**This python program displays, saves and plots the readings from the Radio Shack RS22-168A multi-meter serial port**
 
 Thanks to https://github.com/Ostheer/Voltcraft_ME-32_RS-232 for their progam that I used as a starting point.
 

 I actually use a CH340 USB to serial Cable with Windows 10.
 The correct serial port must be specified.  User can change the sample_time in integer seconds.  The time is not exact using this method.  Program overwrites the CSV file and plot image file if they already exist.  Ctrl-c stops the program and displays the plot.  User must close plot to end the program.

 **Program Dependencies**

- matplotlib
- pyserial