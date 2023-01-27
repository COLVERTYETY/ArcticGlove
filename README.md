[![PlatformIO CI](https://github.com/COLVERTYETY/ArcticGlove/actions/workflows/main.yml/badge.svg?event=push)](https://github.com/COLVERTYETY/ArcticGlove/actions/workflows/main.yml)

# ArcticGlove
This is the repo of the Arctic GLove project.

## What is ArcticGlove?

ArcticGlove is an exploration of human-computer interaction in the context of a wearable glove for the Arctic.

## How to use this repo?

The code for the esp32 can be found in the ```esp32MUCASerial``` folder. This project uses PlatformIO to compile and upload the code to the esp32. The code is written in C++ and uses the Arduino framework.

You can find a visulaisation tool in the ```SerialPlot.py``` scr'ipt. This tool is written in Python and uses the PySerial library to communicate with the esp32.

You might need to change the serial port in the ```SerialPlot.py``` script to match your setup.

## TODO:

- [ ] Add a schematic of the circuit
-  [ ] Add a picture of the glove
-  [ ] Add a ble plotter
-  [ ] Add a ble example code
-  [ ] Add a socket plotter
-  [ ] Add a socket example code
-  [ ] Fix MucaTouch library
-  [ ] Contribute to main MUCA library
-  [ ] Add gesture recognition
