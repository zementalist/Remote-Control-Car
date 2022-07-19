import keyboard  # using module keyboard  pip install keyboard
import serial
import time

arduino = serial.Serial("COM10", baudrate=115200, timeout=0.1)

global keys_pressed
keys_pressed = {
    'w':False,
    'a':False,
    'd':False
}
def walk(e):
    if not keys_pressed['w']:
        keys_pressed['w'] = True
        arduino.write(bytes('w', 'utf-8'))
def unwalk(e):
    keys_pressed['w'] = False
    arduino.write(bytes('s', 'utf-8'))
    
    
def right(e):
    if not keys_pressed['d']:
        keys_pressed['d'] = True
        arduino.write(bytes('d', 'utf-8'))

def unright(e):
    keys_pressed['d'] = False
    arduino.write(bytes('s', 'utf-8'))
    
def left(e):
    if not keys_pressed['a']:
        keys_pressed['a'] = True
        arduino.write(bytes('a', 'utf-8'))
def unleft(e):
    keys_pressed['a'] = False
    arduino.write(bytes('s', 'utf-8'))
    
keyboard.on_press_key('w', walk)
keyboard.on_release_key('w', unwalk)

keyboard.on_press_key('a', left)
keyboard.on_release_key('a', unleft)

keyboard.on_press_key('d', right)
keyboard.on_release_key('d', unright)