from probottools import RobotTools
import time

#-------------------------------
# Sotaを一通り動かすデモプログラム
#-------------------------------

rt = RobotTools('10.186.42.138', 22222)
input()

print('現在の関節角度を取得する。')
input()
axes = rt.read_axes()
print(axes)
input()


print('1秒間で左手を上げる。')
input()
servo_map = dict(L_ELBO=60)
pose = dict(Msec=1000, ServoMap=servo_map)
rt.play_pose(pose)
input()


print('0.5秒間で左手を下ろし、右手を上げ、反時計回りに30度回転し、両目の色を青にする。')
input()
servo_map = dict(L_ELBO=0, R_ELBO=-60, BODY_Y=30)
pose = dict(Msec=500, ServoMap=servo_map)
rt.play_pose(pose)
input()

print('ポーズをリセットする。')
input()
servo_map = dict(HEAD_R=0, HEAD_P=0, BODY_Y=0, L_ELBO=0, R_ELBO=0)
pose = dict(Msec=1000, ServoMap=servo_map)
rt.play_pose(pose)
input()

print('1秒間で左手を挙げる動作を0.3秒後に止める。')
input()
servo_map = dict(L_ELBO=70)
pose = dict(Msec=1000, ServoMap=servo_map)
rt.play_pose(pose)
time.sleep(0.3)
rt.stop_pose()
input()

print('モーション（ポーズのリスト）を実行する。')
input()
nod_motion = [
    dict(Msec=250, ServoMap=dict(R_ELBO=40, HEAD_P=0,   L_ELBO=-40)),
    dict(Msec=250, ServoMap=dict(R_ELBO=70, HEAD_P=-70, L_ELBO=-70)),
    dict(Msec=250, ServoMap=dict(R_ELBO=40, HEAD_P=0,   L_ELBO=-40))
]
rt.play_motion(nod_motion)
input()

print('モーションを0.25秒後に止める。')
input()
nod_motion = [
    dict(Msec=250, ServoMap=dict(R_ELBO=40, HEAD_P=0,   L_ELBO=-40)),
    dict(Msec=250, ServoMap=dict(R_ELBO=70, HEAD_P=-70, L_ELBO=-70)),
    dict(Msec=250, ServoMap=dict(R_ELBO=40, HEAD_P=0,   L_ELBO=-40))
]
rt.play_motion(nod_motion)
time.sleep(0.25)
rt.stop_motion()
input()
 
print('アイドル動作を実行する。')
input()
rt.play_idle_motion()
input()

print('アイドル動作を止める。')
input()
rt.stop_idle_motion()
input()

print('5秒のビートジェスチャを生成し実行する。')
input()
beat_motion = rt.make_beat_motion(5.0)
rt.play_motion(beat_motion)
input()

print('wavファイルを再生する。')
input()
rt.play_wav('sample1.wav')
input()

print('Wavファイルの再生とビートジェスチャを組み合わせる。')
input()
d = rt.play_wav('sample1.wav')
beat_motion = rt.make_beat_motion(d)
rt.play_motion(beat_motion)
input()

print('任意の言葉を発話する')
s = input('発話を入力してください：')
rt.say_text(s)
input()

print('発話しながらビートジェスチャをする。')
s = input('少し長めの発話を入力してください：')
d = rt.say_text(s)
beat_motion = rt.make_beat_motion(d)
rt.play_motion(beat_motion)
input()