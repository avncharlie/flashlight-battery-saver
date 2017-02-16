'''
BatterySaver.py
Author: Alvin Charles, https://github.com/avncharlie
Description:  This is a program that toggles on and off a 'battery-saving'
mode, which, by default, turns off bluetooth, wifi, the keyboard backlight 
and dims the screen to save battery. It can also read off given default 
values through a JSON file.

To control brightness, this was used: https://github.com/nriley/brightness
To control bluetooth, this was used: http://www.frederikseiffert.de/blueutil/
To control the keyboard backlight, this was used:
https://github.com/BlueM/cliclick
'''

from subprocess import Popen, PIPE
import os
import json
import urllib2

class BatterySaver:
    '''
    Battery Saver object whose main purpose is to toggle on and off
    battery saving mode.
    '''
    BINARIES_DIR = 'binaries/'
    BRIGHTNESS = BINARIES_DIR + 'brightness/brightness'
    BLUEUTIL = BINARIES_DIR + 'blueutil/blueutil'
    CLICLICK = BINARIES_DIR + 'cliclick/cliclick'

    def run_command(self, command_list):
        '''
        Using subprocess, return the output, errors and exit code off a
        given command.
        '''
        process = Popen(command_list, stdout=PIPE)
        (output, errors) = process.communicate()
        exit_code = process.wait()
        return [output, errors, exit_code]

    def is_wifi_on(self):
        '''Check if wifi is on or off by trying to access google.'''
        try:
            urllib2.urlopen('http://google.com', timeout=1)
            return 1
        except urllib2.URLError as e:
            return 0

    def is_bluetooth_on(self):
        '''Using blueutil, check if bluetooth is on or off'''
        out = self.run_command([self.BLUEUTIL])[0]
        return int(out.split()[1])

    def backlight(self, turn_on, level=False):
        '''
        Turn the keyboard backlight off by sending keystrokes through 
        cliclick tool. If level percentage is specified to a number between
        zero and 16, turn the backlight on to that level.
        '''
        if turn_on:
            if type(level) == int:
                self.backlight(False)
                if level==16:
                    self.backlight(True)
                elif level != 0:
                    for x in xrange(1, level):
                        self.run_command([self.CLICLICK, 'kp:keys-light-up'])
            else:
                for x in xrange(16):
                    self.run_command([self.CLICLICK, 'kp:keys-light-up'])
        else:
            for x in xrange(16):
                self.run_command([self.CLICLICK, 'kp:keys-light-down'])

    def bluetooth(self, turn_on):
        '''Using blueutil, turn bluetooth on or off'''
        if turn_on:
            return self.run_command([self.BLUEUTIL, 'on'])

        return self.run_command([self.BLUEUTIL, 'off'])

    def wifi(self, turn_on):
        '''Using command line, turn wifi on or off'''
        if turn_on:
            return self.run_command(["networksetup", "-setairportpower", \
                "airport", "on"])
        return self.run_command(["networksetup", "-setairportpower", \
            "airport", "off"])

    def brightness(self, level):
        '''
        Using the brightness program, set the brightness to a specified
        level between one and zero
        '''
        return self.run_command([self.BRIGHTNESS, str(level)])

    def turn_on(self, settings={'Brightness': .3, 'Wifi': False, \
            'Bluetooth': False, 'Backlight': False}):
        '''Turn on battery saver settings'''
        self.save_info()
        self.brightness(settings['Brightness'])
        self.wifi(settings['Wifi'])
        self.bluetooth(settings['Bluetooth'])
        self.backlight(settings['Backlight'])

    def turn_off(self, file="BatterySaverInfo.json", \
            settings={'Brightness': 1.0, 'Wifi': False, 'Bluetooth': True, \
            'Backlight': True}, read_from_file=True):

        '''Turn off battery saver settings'''
        if file not in ''.join(os.listdir('.')):
            return 

        info = json.load(open(file))

        if read_from_file:
            self.wifi(info['wifi'])
            self.bluetooth(info['bluetooth'])
            self.backlight(settings['Backlight'])
            self.brightness(settings['Brightness'])

        else:
            self.wifi(settings['Wifi'])
            self.bluetooth(settings['Bluetooth'])
            self.backlight(settings['Backlight'])
            self.brightness(settings['Brightness'])

        os.remove(file)

    def save_info(self, file="BatterySaverInfo.json"):
        '''
        Save info off all settings about to be changed, so they can be
        reverted, or, if specified, save already given default values
        '''
        info_dict = {
            'wifi': self.is_wifi_on(),
            'bluetooth': self.is_bluetooth_on(),
            'brightness': '.65',
            'backlight': 1
        }

        info_file = open(file, 'w')
        json.dump(info_dict, info_file)
        info_file.close()

    def function_demo(self):
        import time
        print('Saving info...')
        self.save_info()
        print('Output of "cat BatterySaverInfo.json":\n' \
                + self.run_command(['cat', 'BatterySaverInfo.json'])[0])

        raw_input('Enter to turn bluetooth off')
        self.bluetooth(False)

        raw_input('Enter to turn bluetooth on')
        self.bluetooth(True)

        raw_input('Enter to turn backlight on ')
        self.backlight(True)

        raw_input('Enter to turn backlight off')
        self.backlight(False)

        raw_input('Enter to turn backlight to 5')
        self.backlight(True, level=5)
        
        raw_input('Enter to turn wifi off')
        self.wifi(False)

        raw_input('Enter to turn wifi on')
        self.wifi(True)

        raw_input('Enter to set the brightness to .3')
        self.brightness(.3)

        raw_input('Enter to set the brightness to .9')
        self.brightness(.9)

    def demo(self):
        raw_input('Enter to turn battery saver on')
        self.turn_on()

        raw_input('Enter to turn battery saver off')
        self.turn_off()

if __name__ == '__main__':
    b = BatterySaver()
    b.demo()
