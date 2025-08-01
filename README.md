starting up ssh
% eval "$(ssh-agent -s)"
% ssh-add ~/.ssh/id_ed25519


% source venv/bin/activate
% python scoreboard.py
# to leave venv:
% deactivate

Requires libUSB-1.0 installed in system
apt-get install libusb-1.0

Bus 001 Device 006: ID 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC


# R-PI Pins used
https://pinout.xyz/ - Raspberry pi pinouts

|Pin \ #| Pi Func    | Wire Color | Description |
|:----:|------------|-----------:|-------------|
|| **Light Strips** |||
|2 or 4| 5v Power   | Red        | Optional    |
| 6    | Ground     | Black      | |
| 19   | SPI0 MOSI  | Green      | SPI Data to LED Array|
| 23   | SPI0 SCLK  | Yellow     | SPI Clock for LED Array|
|| **2 button box** |||
| 35   | GPIO19     | Gray       | Red Score|
| 36   | GPIO16     | Orange/Red | Blue Score|
| 34   | Ground     | Blue       | |
|| **Red Button Box** |||
| 14   | Ground     | Red        | |
| 12   | GPIO18     | Yellow     | Red Effect|
|| **Blue Button Box** |||
| 20   | Ground     | Black      | |
| 18   | GPI024     | Brown      | Blue Effect|


---
Initial venv setup using python 3.11
% python -m venv venv 
% source venv/bin/activate
% python -m pip install -r requirements.txt
