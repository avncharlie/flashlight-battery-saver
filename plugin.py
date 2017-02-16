'''
plugin.py
Author: Alvin Charles, https://github.com/avncharlie
Description:  This is a Flashlight plugin that lowers the screen brightness, 
turns off bluetooth, wifi, the keyboard backlight and dims the screen to save
battery. To do this, it uses BatterySaver.py, made by me.

The icon used was from http://simpleicon.com/battery-low.html
'''
import json
import os

from BatterySaver import BatterySaver

def preferences(option):
    data = json.load(open('preferences.json'))

    if option in ['activation', 'deactivation']:
        dict = {x['option']: x['enable'] for x in data[option]}
        for key, value in dict.iteritems():
            if value[0] in '1234567890':
                dict[key] = float(value)
            if value == 'off':
                dict[key] = False
            if value == 'on':
                dict[key] = True
        return dict

    return data['remember_settings']

def results(fields, original_query):
    '''Preview what is about to be run'''
    turn_on = True
    title = ''

    # This file is only there if the battery saver is running
    if ('BatterySaverInfo.json' in os.listdir('.')):
        title = 'Turn battery saver off'
        turn_on = False

    else:
        title = 'Turn battery saver on'

    return {
        "title": title,
        "run_args": [turn_on],
    }

def run(turn_on):
    '''Toggle on or off battery saver mode'''
    b = BatterySaver()
    if turn_on:
        b.turn_on(settings=preferences('activation'))
    else:
        b.turn_off(settings=preferences('deactivation'), \
            read_from_file=preferences('remember'))
