#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-

import sys
import time
import WebSocketCapf as cwebsock

from puppettools import PuppetTools

# webスクレイピング用
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta

class websocketagent(cwebsock.WebSocketCapf) :
    def __init__(self, loginurl, selfID, selfIDPasswd, websockurl, robotIP, robotPort, targetID) :
        super(websocketagent, self).__init__(loginurl, selfID, selfIDPasswd, websockurl)

        self.robotIP = robotIP
        self.robotPort = robotPort
        self.setMessageCallback(self.sendMessageCB)

        self.selfID = selfID
        self.targetID = targetID

    def sendMessageCB(self, message) :
        pt = PuppetTools(self.robotIP, self.robotPort)

        print("[Puppet Command from CAPF]   " + message)
        # messageの構成:  cmd;gesture;1 のように、3つのパートに分かれる 以下のように取り出せる
        print('message 0: ' + message.split(';')[0])
        print('message 1: ' + message.split(';')[1])
        print('message 2: ' + message.split(';')[2])

        # コマンド内容によりpuppetの動作を仕分ける
        if 'cmd' in message.split(';')[0]:

            if 'gesture' in message.split(';')[1]:

                if '1' in  message.split(';')[2]:
                    servo_map = dict(L_ELBO=60)
                    pose = dict(Msec=1000, ServoMap=servo_map)
                    pt.play_pose(pose)

                elif '2' in  message.split(';')[2]:
                    servo_map = dict(L_ELBO=60, R_ELBO=-60)
                    pose = dict(Msec=1000, ServoMap=servo_map)
                    pt.play_pose(pose)

                elif '3' in  message.split(';')[2]:
                    servo_map = dict(R_ELBO=-60)
                    pose = dict(Msec=1000, ServoMap=servo_map)
                    pt.play_pose(pose)

                else:
                    print("そのコマンドは登録されていないよ")

            if 'rotate' in message.split(';')[1]:
                # BODY_Y の稼働範囲は -80 ~ 80　（-は反時計回りの回転）
                if '1' in  message.split(';')[2]:
                    servo_map = dict(L_ELBO=0, R_ELBO=0, BODY_Y=80)
                    pose = dict(Msec=750, ServoMap=servo_map)
                    pt.play_pose(pose)

                elif '2' in  message.split(';')[2]:
                    servo_map = dict(L_ELBO=0, R_ELBO=0, BODY_Y=45)
                    pose = dict(Msec=750, ServoMap=servo_map)
                    pt.play_pose(pose)

                elif '3' in  message.split(';')[2]:
                    servo_map = dict(L_ELBO=0, R_ELBO=0, BODY_Y=20)
                    pose = dict(Msec=750, ServoMap=servo_map)
                    pt.play_pose(pose)

                elif '4' in  message.split(';')[2]:
                    servo_map = dict(L_ELBO=0, R_ELBO=0, BODY_Y=0)
                    pose = dict(Msec=750, ServoMap=servo_map)
                    pt.play_pose(pose)

                elif '5' in  message.split(';')[2]:
                    servo_map = dict(L_ELBO=0, R_ELBO=0, BODY_Y=-20)
                    pose = dict(Msec=750, ServoMap=servo_map)
                    pt.play_pose(pose)

                elif '6' in  message.split(';')[2]:
                    servo_map = dict(L_ELBO=0, R_ELBO=0, BODY_Y=-45)
                    pose = dict(Msec=750, ServoMap=servo_map)
                    pt.play_pose(pose)

                elif '7' in  message.split(';')[2]:
                    servo_map = dict(L_ELBO=0, R_ELBO=0, BODY_Y=-80)
                    pose = dict(Msec=750, ServoMap=servo_map)
                    pt.play_pose(pose)

                else:
                    print("そのコマンドは登録されていないよ")


            if 'scenario' in message.split(';')[1]:

                if '1' in  message.split(';')[2]:
                    pt.play_wav('sample1.wav')

                elif '2' in  message.split(';')[2]:
                    d = pt.play_wav('sample1.wav')
                    beat_motion = pt.make_beat_motion(d)
                    pt.play_motion(beat_motion)

                else:
                    print("そのコマンドは登録されていないよ")


        # ウェブ上の情報のスクレイピング用
        # if 'EventInfo' in message:
        #     response = requests.get('https://startupside.jp/tokyo/event/')
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     # イベント名を取得
        #     event_title = soup.find('h3', attrs={'class':'eventBox_title'}).get_text()
        #     # 日程を取得   時間は未取得
        #     event_date = event_title[event_title.rfind('　')+1:event_title.rfind('催')+1]
        #     event_date = event_date.replace("(", "")
        #     event_date = event_date.replace(")", "曜日に")
            
        #     event_title = event_title.replace(event_title[event_title.rfind('　'):len(event_title)+1], "")
        #     print(event_title)
        #     print(event_date)
            
        #     # イベントの種類を取得
        #     event_type = soup.find('li', attrs={'class':'eventBox_type'}).get_text()
        #     print(event_type)
        #     # コマンド内容を書き換え
        #     message = (message + ";" + event_title + ";" + event_date + ";" +event_type)


if __name__ == '__main__' :
    if len(sys.argv) < 8 :
        print("Usage: {} <login url> <id> <passwd> <websocket url> <robot-addr> <robot-port> <targetid>".format(sys.argv[0]))
        sys.exit(1)
    loginurl = sys.argv[1]
    loginid = sys.argv[2]
    loginpasswd = sys.argv[3]
    websockurl = sys.argv[4]
    robotaddr = sys.argv[5]
    robotport = int(sys.argv[6])
    targetid = sys.argv[7]

    agent = websocketagent(loginurl, loginid, loginpasswd, websockurl, robotaddr, robotport, targetid)

    if not agent.connect() :
        print('cannot connect websocket')
        sys.exit(0)

    while agent.isactive() :
        time.sleep(1)
