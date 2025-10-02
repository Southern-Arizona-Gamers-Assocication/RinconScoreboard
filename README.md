starting up ssh
% eval "$(ssh-agent -s)"
% ssh-add ~/.ssh/id_ed25519

# Must be run in a virtual environment (venv).
# Start venv:
% source venv/bin/activate
% python scoreboard.py
# to leave venv:
% deactivate

Requires libUSB-1.0 installed in system
apt-get install libusb-1.0

Bus 001 Device 006: ID 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC


# R-PI Pins used
https://pinout.xyz/ - Raspberry pi pinouts

|Pin \ #| Pi Func   | Wire Color |Abbrev.| Description |
|:----:|------------|-----------:|:-----:|------------|
|| **Light Strips** |||
|2 or 4| 5v Power   | Red        |       | Optional    |
| 6    | Ground(Gnd)| Black      |       ||
| 19   | SPI0 MOSI  | Green      |       | SPI Data to LED Array|
| 23   | SPI0 SCLK  | Yellow     |       | SPI Clock for LED Array|
|| **2 button box** |            |       ||
| 35   | GPIO19     | Orange     |  SR+  | Score Red Button: Input Pin w/ Pull-up|
|      | Gnd        |Orange/White|  SR-  | Score Red Button Return |
| 36   | GPIO16     | Brown      |  SB+  | Score Blue Button: Input Pin w/ Pull-up|
|      | Gnd        | Brown/White|  SB-  | Score Blue Button Return |
|| **Red Button Box** |||
| 12   | GPIO18     | Yellow     |  RE+  | Red Effect Button: Input Pin w/ Pull-up|
|      | Gnd        | Red        |  RE-  | Red Effect Button Return|
|| **Blue Button Box** |||
| 18   | GPI024     | Brown      |  BE+  | Blue Effect Button: Input Pin w/ Pull-up|
|      | Gnd        | Black      |  BE-  | Blue Effect Button Return|

--------------------------------------------------------
Initial venv setup using python 3.11
% python -m venv venv 
% source venv/bin/activate
% python -m pip install -r requirements.txt

RJ45 Plug Pinout T-568B:
[RJ45 Plug Pinout T-568B](./docs/RJ45_Pinout_T-568B_-_Most_Common.png)

Red-Blue Score Box Connector Pinout (Back View and See Through to the Front RJ45 Jack):
|   |   |   |   |   |   |   |   |   |   | ● | ● | ● | ● | ● | ● |   |   |   |   |   |   |   |   |   |   |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|   |   |   |   |   |   |   | ● | ● | ● |   |   |   |   |   |   | ● | ● | ● |   |   |   |   |   |   |   |
|   |   |   |   |   | ● | ● |   |   |   |   | 3 | 6 | 7 | 8 | SH|   |   |   | ● | ● |   |   |   |   |   |
|   |   |   |   | ● |   |   |   |   |   |   | 1 | 2 | 4 | 5 | SH|   |   |   |   |   | ● |   |   |   |   |
|   |   |   | ● |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ● |   |   |   |
|   |   | ● |   |   |   |   |   |   |   | ┏ | ━ | ━ | ━ | ━ | ┓ |   |   |   |   |   |   |   | ● |   |   |
|   |   | ● |   |   |   |   |   |   |   | ┃ |   |   |   |   | ┃ |   |   |   |   |   |   |   | ● |   |   |
|   | ● |   |   |   |   |   |   |   | ┏ | ┛ |   |   |   |   | ┗ | ┓ |   |   |   |   |   |   |   | ● |   |
|   | ● |   |   |   |   |   |   |   | ┃ |   |   |   |   |   |   | ┃ |   |   |   |   |   |   |   | ● |   |
|   | ● |   |   |   |   | ┏ | ━ | ━ | ┛ |   |   |   |   |   |   | ┗ | ━ | ━ | ┓ |   |   |   |   | ● |   |
| ● |   |   |   |   |   | ┃ |   |   |   |   |   |   |   |   |   |   |   |   | ┃ |   |   |   |   |   | ● |
| ● |   |   |   |   |   | ┃ |   |   |   |   |   |   |   |   |   |   |   |   | ┃ |   |   |   |   |   | ● |
| ● |   |   |   |   |   | ┃ |SH |   |SR-|SR+|   |   |   |   |SB-|SB+|   | SH| ┃ |   |   |   |   |   | ● |
| ● |   |   |   |   |   | ┃ |SH |   | OW| O | GW| Bl|BlW| G |BrW|Br |   | SH| ┃ |   |   |   |   |   | ● |
| ● |   |   |   |   |   | ┃ |SH |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   | SH| ┃ |   |   |   |   |   | ● |
| ● |   |   |   |   |   | ┃ |SH |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   | SH| ┃ |   |   |   |   |   | ● |
|   | ● |   |   |   |   | ┃ |   |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   |   | ┃ |   |   |   |   | ● |   |
|   | ● |   |   |   |   | ┃ |   |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   |   | ┃ |   |   |   |   | ● |   |
|   | ● |   |   |   |   | ┗ | ━ | ━ | ┻ | ┻ | ┻ | ┻ | ┻ | ┻ | ┻ | ┻ | ━ | ━ | ┛ |   |   |   |   | ● |   |
|   |   | ● |   |   |   |   |   |   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |   |   |   |   |   |   | ● |   |   |
|   |   | ● |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ● |   |   |
|   |   |   | ● |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ● |   |   |   |
|   |   |   |   | ● |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ● |   |   |   |   |
|   |   |   |   |   | ● | ● |   |   |   |   |   |   |   |   |   |   |   |   | ● | ● |   |   |   |   |   |
|   |   |   |   |   |   |   | ● | ● | ● |   |   |   |   |   |   | ● | ● | ● |   |   |   |   |   |   |   |
|   |   |   |   |   |   |   |   |   |   | ● | ● | ● | ● | ● | ● |   |   |   |   |   |   |   |   |   |   |


Red Effect and Blue Effect Button Boxes Shared Connector Pinout (Back View and See Through to the Front RJ45 Jack):
| ┏ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ┓ |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ┃ |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   |   |   |   |   | ┏ | ━ | ━ | ━ | ━ | ┓ |   |   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   |   |   |   |   | ┃ |   |   |   |   | ┃ |   |   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   |   |   |   | ┏ | ┛ |   |   |   |   | ┗ | ┓ |   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   |   |   |   | ┃ |   |   |   |   |   |   | ┃ |   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   | ┏ | ━ | ━ | ┛ |   |   |   |   |   |   | ┗ | ━ | ━ | ┓ |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   | ┃ |   |   |   |   |   |   |   |   |   |   |   |   | ┃ |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   | ┃ |   |   |   |   |   |   |   |   |   |   |   |   | ┃ |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   | ┃ |   |   |RE-|RE+|   |   |   |   |BE-|BE+|   |   | ┃ |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   | ┃ |   |   | OS| O | GW| Bl|BlW| G |BrW|Br |   |   | ┃ |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   | ┃ |   |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   |   | ┃ |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   | ┃ |   |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   |   | ┃ |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   | ┃ |   |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   |   | ┃ |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   | ┃ |   |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   |   | ┃ |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   | ┗ | ━ | ━ | ┻ | ┻ | ┻ | ┻ | ┻ | ┻ | ┻ | ┻ | ━ | ━ | ┛ |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   |   |   |   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   |   |   |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   |   |   |   | W | O | Bk| R | G | Y | Bu| Br|   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   |   |   |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |   |   | ⦿ | ━ |   |   |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   |   |   | ━ | ⦿ |   |   |   | ┃ |
| ┃ |   |   |   |   |   |   |   |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |   |   | ⦿ | ━ |   |   |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   |   |   | ━ | ⦿ |   |   |   | ┃ |
| ┃ |   |   |   |   |   |   |   |   | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ | ┃ |   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |RE-| W | ⦿ | ━ | W | ━ | ━ | ┛ | ┃ | ◯ | ◯ | ◯ | ◯ | ┃ | ┗ | ━ | ━ |Br | ━ | ⦿ |Br |BE+|   | ┃ |
| ┃ |   |   |   |   |   |   |   |   |   | ┃ | Bk| R | G | Y | ┃ |   |   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |RE+| O | ⦿ | ━ | O | ━ | ━ | ━ | ┛ |   |   |   |   | ┗ | ━ | ━ | ━ |Bu | ━ | ⦿ |BrW|BE-|   | ┃ |
| ┃ |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ┃ |
| ┃ |   |   |   |   |   |   |   |   |   |   |   | ┏ | ┓ |   |   |   |   |   |   |   |   |   |   |   | ┃ |
| ┖ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ┛ | ┗ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ━ | ┚ |


