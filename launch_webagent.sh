#!/bin/sh
# 引数の指定: <login url> <id> <passwd> <websocket url> <robot-addr> <robot-port> <targetid>
python webagent.py "https://hanazono.ca-platform.org/api/login" "CA001" "CA001" "wss://hanazono-websocket.ca-platform.org" "10.186.42.138" 22222 'OP001SA'