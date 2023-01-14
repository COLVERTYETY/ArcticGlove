# ArcticGlove
This is the repo of the Arctic GLove project.

## What is ArcticGlove?

ArcticGlove is an exploration of human-computer interaction in the context of a wearable glove for the Arctic.

## How to use this repo?

The code for the esp32 can be found in the ```esp32MUCASerial``` folder. This project uses PlatformIO to compile and upload the code to the esp32. The code is written in C++ and uses the Arduino framework.

You can find a visulaisation tool in the ```SerialPlotter.py``` scr'ipt. This tool is written in Python and uses the PySerial library to communicate with the esp32.

You might need to change the serial port in the ```SerialPlotter.py``` script to match your setup.

