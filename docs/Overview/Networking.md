# Networking

## Connect to Orin AGX
Most of the connections to the orin are done through SSH. The current orin may also be connected in zerotier or tailscale vpns, allowing for remote access to the orin.

In addition, VNC can also be used to control the display of the Orin remotely. This is useful for debugging and testing purposes. Currently, the VNC server is running on the Orin automatically after booting. 

### Connect to VNC

You can use any VNC client to connect to the Orin. Remmina, which is installed on some Ubuntu versions by default, can also be used. You only need to specify the IP address of the Orin and select the 'VNC' plugin.

Note: for security reasons, the VNC server can be modified to only work on the local network. If the service is running only locally, you need to forward the port using ssh and then connect to the local port. The command to do this is:

```bash
ssh -L 5900:localhost:5900 -C -N -l <orin> <orin_ip>
```

Then, you can connect to localhost:5900 using your VNC client.

### Debug VNC
If the service isn't running you may try the following commands:
```bash
sudo systemctl status x11vnc
journalctl -u x11vnc.service

sudo systemctl start x11vnc
sudo systemctl stop x11vnc

sudo systemctl enable x11vnc
sudo systemctl disable x11vnc
```

### Setup VNC server

Install x11vnc
```bash
sudo apt install x11vnc
```
Set up password
```bash
x11vnc -storepasswd your_password ~/.vnc/passwd
```

Create a service file
```bash
sudo nano /etc/systemd/system/x11vnc.service
```
Add the following content to the file:

```bash
[Unit]
Description=Start x11vnc on boot for Jetson GUI (user orin)
After=graphical.target
Requires=display-manager.service
StartLimitBurst=10

[Service]
Type=simple
ExecStart=/usr/bin/x11vnc \
  -display :0 \
  -auth /home/orin/.Xauthority \
  -rfbauth /home/orin/.vnc/passwd \
  -forever -loop -noxdamage -repeat -shared
User=orin
Group=orin
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/orin/.Xauthority

Restart=always
RestartSec=15

[Install]
WantedBy=graphical.target
```

Then, reload the systemd daemon and enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable x11vnc
```
Then, start the service:
```bash
sudo systemctl start x11vnc
```

If you want to run the service only on localhost (and forward the port using ssh), you can replace the ExecStart command in the service file:
```bash
ExecStart=/usr/bin/x11vnc \
  -display :0 \
  -auth /home/orin/.Xauthority \
  -rfbauth /home/orin/.vnc/passwd \
  -forever -loop -noxdamage -repeat -shared \
  -localhost
```

