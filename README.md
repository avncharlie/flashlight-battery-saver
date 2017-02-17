# Battery saver Plugin for [Flashlight](http://flashlight.nateparrott.com/)
Battery saver plugin for Flashlight

This is a Spotlight search plugin that turns on a customisable battery saver mode.
It can control:

- Screen brightness (through [brightness](https://github.com/nriley/brightness))
- Wifi
- Bluetooth (through [blueutil](http://www.frederikseiffert.de/blueutil/))
- Keyboard backlight (through [cliclick](https://github.com/BlueM/cliclick))

Problems:

- The keyboard backlight is controlled by sending virtual key presses. By default, Macs don't allow changing the keyboard backlight in low light. This could interfere with your settings. See [this](http://apple.stackexchange.com/questions/45378/how-can-i-force-my-keyboard-backlight-to-turn-on) for more information.
- Macs automatically adjust screen brightness based on the current ambient light level. This means that your brightness may automatically become brighter or dimmer right after it is set by activating or deactivating the plugin. See [this](http://apple.stackexchange.com/questions/107692/screen-brightness-automatically-adjusting-in-os-x-mavericks) for more information.
- There [isn't much documentation](https://github.com/nate-parrott/Flashlight/wiki/Settings-API) on the Flashlight settings API, so the settings screen looks really horrible right now.

See the [original repository](https://github.com/avncharlie/flashlight-battery-saver) for any questions about this plugin.

![Screenshot](https://github.com/avncharlie/flashlight-battery-saver/raw/master/Screenshot.png)
![Screenshot](https://github.com/avncharlie/flashlight-battery-saver/raw/master/Settings%20screenshot.png)
