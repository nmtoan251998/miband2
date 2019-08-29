## Source base MiBand2
Library to work with Xiaomi MiBand 2 (Support python2/python3)
[Read the Article here](https://medium.com/@a.nikishaev/how-i-hacked-xiaomi-miband-2-to-control-it-from-linux-a5bd2f36d3ad)

## Available scripts
1) Install dependencies
```sh
pip install -r requirements.txt
```
2) Turn on your Bluetooth
3) Unpair you MiBand2 from current mobile apps
4) Find out you MiBand2 MAC address
```sh
sudo hcitool lescan
```
5) Run this to auth device
```sh
python example.py --mac MAC_ADDRESS --init
```
6.1) Run this to call demo functions
```sh
python example.py --standard --mac MAC_ADDRESS
python example.py --help
```

6.2) Project script
``` sh
python3 example.py --nienluan --mac MAC_ADDRESS
```

7) If you having problems(BLE can glitch sometimes) try this and repeat from 4)
```sh
sudo hciconfig hci0 reset
```
