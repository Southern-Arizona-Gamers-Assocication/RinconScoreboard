starting up ssh
% eval "$(ssh-agent -s)"
% ssh-add ~/.ssh/id_ed25519


% source venv/bin/activate
% python scoreboard.py

Requires libUSB-1.0 installed in system
apt-get install libusb-1.0

Bus 001 Device 006: ID 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC


https://pinout.xyz/ - Raspberry pi pinouts

** Light Strips
- Red: 2 or 4 (5v Power) -- Optional
- Black: 6 (Ground)
- Green: 19 (SPI0 MOSI)
- Yellow: 23 (SPI0 SCLK)

** 2 button (red and blue)
- Gray: 35 (GPIO 19)
- Orange/Red: 37 (GPIO 26)
- Blue: 39 (GND)

** Red button box
- Red: 2 or 4 (5v Power)
- Yellow: 10 (GPIO 15)

** Blue button box
-  Black: 9 (Ground)
-  Brown: 5 (GPIO 3)

---
Initial venv setup using python 3.11
% python -m venv venv 
% source venv/bin/activate
% python -m pip install -r requirements.txt
