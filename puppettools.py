#!/usr/bin/env pythonpython3.10.6
# -*- coding: utf-8 -*-

import gtts
import json
import pydub
import random
import socket
import typing

class PuppetTools(object):
    def __init__(self, ip:str, port:int):
        self.__ip = ip
        self.__port = port

    def read_axes(self) -> dict:
        with self.__connect() as conn:
            self.__send(conn, 'read_axes'.encode('utf-8'))
            data = self.__recv(conn)
        axes = json.loads(data)
        return axes

    def play_pose(self, pose:dict):
        print("[ジェスチャ] play pose")
        data = json.dumps(pose).encode('utf-8')
        with self.__connect() as conn:
            self.__send(conn, 'play_pose'.encode('utf-8'))
            self.__send(conn, data)

    def stop_pose(self):
        with self.__connect() as conn:
            self.__send(conn, 'stop_pose'.encode('utf-8'))

    def play_motion(self, motion:typing.List[dict]):
        data = json.dumps(motion).encode('utf-8')
        with self.__connect() as conn:
            self.__send(conn, 'play_motion'.encode('utf-8'))
            self.__send(conn, data)

    def stop_motion(self):
        with self.__connect() as conn:
            self.__send(conn, 'stop_motion'.encode('utf-8'))

    def play_idle_motion(self, speed=1.0, pause=1000):
        data = json.dumps(dict(Speed=speed, Pause=pause)).encode('utf-8')
        with self.__connect() as conn:
            self.__send(conn, 'play_idle_motion'.encode('utf-8'))
            self.__send(conn, data)

    def stop_idle_motion(self):
        with self.__connect() as conn:
            self.__send(conn, 'stop_idle_motion'.encode('utf-8'))

    def play_wav(self, wav_file:str) -> float:
        with open(wav_file, 'rb') as f:
            sound = pydub.AudioSegment.from_file(wav_file, 'wav')
            data = f.read()
            with self.__connect() as conn:
                self.__send(conn, 'play_wav'.encode('utf-8'))
                self.__send(conn, data)
            return sound.duration_seconds

    def stop_wav(self):
        with self.__connect() as conn:
            self.__send(conn, 'stop_wav'.encode('utf-8'))

    def say_text(self, text:str, lang='ja', output_file_name='temp', slow=False) -> float:
        def make_wav() -> float:
            gtts.gTTS(text=text, lang=lang, slow=slow).save(f'{output_file_name}.mp3')
            sound = pydub.AudioSegment.from_mp3(f'{output_file_name}.mp3')
            sound.export(f'{output_file_name}.wav', format='wav')
            return sound.duration_seconds

        d = make_wav()
        self.play_wav(f'{output_file_name}.wav')
        return d

    def make_beat_motion(self, duration_seconds:float, speed=1.0):
        DEFAULT_ARM_SERVO_MAP = dict(HEAD_R=0, HEAD_P=0, BODY_Y=0, L_ELBO=0, R_ELBO=0)
        BEAT_ARM_SERVO_MAP_LIST = (
            dict(HEAD_R=-14, BODY_Y=-1, HEAD_P=-1,  R_ELBO=0,   L_ELBO=-59),
            dict(HEAD_R=22,  BODY_Y=-1, HEAD_P=-1,  R_ELBO=54,  L_ELBO=21),
            dict(HEAD_R=-1,  BODY_Y=0,  HEAD_P=20,  R_ELBO=54,  L_ELBO=-43),
            dict(HEAD_R=-1,  BODY_Y=-1, HEAD_P=-7,  R_ELBO=-35, L_ELBO=39),
            dict(HEAD_R=-22, BODY_Y=-1, HEAD_P=-20, R_ELBO=10,  L_ELBO=4),
            dict(HEAD_R=6,   BODY_Y=0,  HEAD_P=-20, R_ELBO=-24, L_ELBO=43),
            dict(HEAD_R=6,   BODY_Y=-1, HEAD_P=-1,  R_ELBO=40,  L_ELBO=-25),
            dict(HEAD_R=6,   BODY_Y=3,  HEAD_P=-1,  R_ELBO=-2,  L_ELBO=1)
        )
        def __choose(prev):
            while True:
                map = random.choice(BEAT_ARM_SERVO_MAP_LIST)
                if map != prev:
                    return map
        
        msec = int(1000 / speed)
        size = int(duration_seconds * 1000 / msec)
        motion = []
        prev = {}
        for _ in range(size):
            servo_map = __choose(prev)
            motion.append(dict(Msec=msec, ServoMap=servo_map))
            prev = servo_map

        motion.append(dict(Msec=1000, ServoMap=DEFAULT_ARM_SERVO_MAP))
        return motion

    def __connect(self) -> socket.socket:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.__ip, self.__port))
        return conn

    def __recvall(self, conn:socket.socket, size:int):
        chunks = []
        bytes_recved = 0
        while bytes_recved < size:
            chunk = conn.recv(size - bytes_recved)
            if chunk == b'':
                raise RuntimeError('socket connection broken')
            chunks.append(chunk)
            bytes_recved += len(chunk)
        return b''.join(chunks)

    def __recv_size(self, conn:socket.socket) -> int:
        b_size = self.__recvall(conn, 4)
        return int.from_bytes(b_size, byteorder='big')

    def __recv(self, conn:socket.socket) -> str:
        size = self.__recv_size(conn)
        data = self.__recvall(conn, size)
        return data

    def __send(self, conn:socket.socket, data:bytes):
        size = len(data)
        conn.sendall(size.to_bytes(4, byteorder='big'))
        conn.sendall(data)