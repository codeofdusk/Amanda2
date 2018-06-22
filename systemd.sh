#! /bin/bash
USER=$(whoami)
PWD=$(pwd)
sudo bash -c "echo \"[Unit]
Description=amanda
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PWD
ExecStart=/usr/bin/env python3 $PWD/amanda.py
Restart=always

[Install]
WantedBy=multi-user.target\" > /etc/systemd/system/amanda.service"
sudo systemctl daemon-reload
