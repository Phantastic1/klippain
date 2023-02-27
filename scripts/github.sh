#!/bin/bash
KLIPPER_CONFIG_PATH="${HOME}/printer_data/config"
cd {KLIPPER_CONFIG_PATH}
git add .
git commit -m "backup"
git push --set-upstream origin V2.1277