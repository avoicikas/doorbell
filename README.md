# README

## Features

Doorbell bpt y/c 200 control via raspberry

* doorbell action logging
* open doors on events
* silence doorbell
* report on doorbell press to messenger
* website and facebook bot to control actions and settings

## Setup

* ngrok account needed for facebook bot (run command: ./ngrok http 8000)
* setup facebook page, token, webhook
* fill in parameters in settings.py:
  * doorbel_watcher_pin -> GPIO pin number that connects via optocoupler 4N35 to doorbell (CALL pin) to sense if it is pressed
  * doorPIN -> GPIO pin number that connects via relay to Speech out (relay 2) and Common pin (relay 3)
  * bellPIN -> GPIO pin number that connects via relay to Common (relay 1), bell input wire (relay 2, ( when GPIO not active it is short circuited to Common)), bell input wire (relay 3, when GPIO active it lets current flow over the bell)
  * ringRealBell -> 1 to play default doorbell sound when it is pressed, 0 to only notify via messanger
  * delayTime -> time in seconds to delay before activating sound
  * openCodeTime -> upper time in seconds of doorbell press to count the press in a combination
  * openDoors -> 0; combination counter
  * fb, ID1, ID2 -> facebook IDs to notify on doorbell press
  * PAGE_ACCESS_TOKEN -> token from facebook page for bot
* run script: python3 server.py

## Hardware

* BPT C/200 or any other similar doorbell
* raspberry pi 3
* optocoupler, relays
