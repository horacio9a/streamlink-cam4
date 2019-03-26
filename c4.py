# Cam4 Anonymous All Modes Recorder v.1.0.9 by horacio9a for Python 2.7.16

import sys, os, urllib, urllib3, ssl, re, time, datetime, command
urllib3.disable_warnings()
from urllib3 import PoolManager
reload(sys)
sys.setdefaultencoding('utf-8')
from colorama import init, Fore, Back, Style
from termcolor import colored
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('config.cfg')

init()
print(colored('\n => START <=\n', 'yellow', 'on_blue'))

while True:
   try:
      modellist = open(config.get('files', 'model_list'),'r')
      for (num,value) in enumerate(modellist):
         print ' =>',(num+1),value[:-1]
      mn = int(raw_input(colored('\n => Select C4 Model => ', 'yellow', 'on_blue')))
      break
   except ValueError:
      print(colored('\n => Input must be a number <=', 'yellow', 'on_red'))
model = open(config.get('files', 'model_list'), 'r').readlines()[mn-1][:-1]

url ='https://www.cam4.com/{}'.format(model)
user_agent = {'user-agent': 'Mozilla/5.0 (Android; Mobile; rv:14.0) ..'}
http = urllib3.PoolManager(10, headers=user_agent)
r = http.urlopen('GET',url)
enc = (r.data)
dec=urllib.unquote(enc).decode()

state0 = dec.split("showState: '")[1]
state = state0.split("'")[0]

if len(state) > 0:
 try:
   age0 = dec.split('Age:</')[1]
   age1 = age0.split('</')[0]
   age = age1.split('">')[1]
 except:
   age = '-'

 try:
   loc0 = dec.split('Location:</')[1]
   loc1 = loc0.split('</')[0]
   loc2 = loc1.split('">')[1]
   loc3 = re.sub(',', '', loc2)
   loc = re.sub(' ', '', loc3)
 except:
   loc = '-'

 try:
   sta0 = dec.split('Status:</')[1]
   sta1 = sta0.split('</')[0]
   sta = sta1.split('">')[1]
 except:
   sta = '-'

 try:
   room0 = dec.split('room":"')[1]
   room = room0.split('"')[0]
 except:
   room = '-'

 try:
   ms0 = dec.split('Member since:</')[1]
   ms1 = ms0.split('</')[0]
   ms2 = ms1.split('">')[1]
   ms3 = re.sub(' ', '-', ms2)
   ms = re.sub(',', '', ms3)
 except:
   ms = '-'

 try:
   eth0 = dec.split('Ethnicity:</')[1]
   eth1 = eth0.split('</')[0]
   eth2 = eth1.split('">')[1]
   eth = re.sub(' ', '', eth2)
 except:
   eth = '-'

 vau0 = dec.split('rtmp://')[1]
 vau = vau0.split('/')[0]

 if len(vau) > 30:
    print(colored("\n => TRY AGAIN <=", 'yellow','on_blue'))
    time.sleep(3)
    print(colored('\n => END <=', 'yellow','on_blue'))
    time.sleep(1)
    sys.exit()
 else:
    pass

 vpu0 = dec.split('videoPlayUrl":"')[1]
 vpu = vpu0.split('"')[0]

 # room = vpu.split('-')[0]
 wcdn = vpu.split('-')[1]

 swf0 = dec.split('playerUrl":"')[1]
 swf = swf0.split('"')[0]

 print (colored('\n => Room: ({}) * State: ({}) * Member since: ({}) <=', 'white', 'on_blue')).format(room,state,ms)
 print (colored('\n => Age: ({}) * Location: ({}) * Status: ({}) * Ethnic: ({}) <=', 'yellow', 'on_blue')).format(age,loc,sta,eth)
 print (colored('\n => App URL => {} <=', 'yellow', 'on_blue')).format(vau)
 
 hlsurl1 = 'https://cam4-hls.xcdnpro.com/{}/cam4-origin-live/ngrp:{}_all/playlist.m3u8'.format(wcdn,vpu)
 hlsurl2 = 'https://cam4-hls.xcdnpro.com/{}/cam4-origin-live/amlst:{}_aac/playlist.m3u8'.format(wcdn,vpu)
 hlsurl = 'https://cam4-hls.xcdnpro.com/{}/cam4-origin-live/{}_aac/playlist.m3u8'.format(wcdn,vpu)
 hls_url0 = dec.split("hlsUrl: '")[1]
 hls_url1 = hls_url0.split("'")[0]
 hls_url2 = hls_url1.split('live/')[1]
 hls_url = hls_url2.split('/')[0]
 print (colored('\n => Play URL => {} <=', 'yellow', 'on_blue')).format(hls_url)

 while True:
    try:
       mode = int(raw_input(colored('\n => Mode => Exit(6)  URL(5)  YTDL(4)  SL(3)  FFMPEG(2)  RTMP(1)  FFPLAY(0) => ', 'white', 'on_green')))
       break
    except ValueError:
       print(colored('\n => Input must be a number <=', 'yellow', 'on_red'))
 if mode == 0:
    mod = 'FFPLAY'
 if mode == 1:
    mod = 'RTMP'
 if mode == 2:
    mod = 'FFMPEG'
 if mode == 3:
    mod = 'SL'
 if mode == 4:
    mod = 'YTDL'
 if mode == 5:
    mod = 'URL'
 if mode == 6:
    mod = 'EXIT'

 timestamp = str(time.strftime('%d%m%Y-%H%M%S'))
 stime = str(time.strftime('%H:%M:%S'))
 path = config.get('folders', 'output_folder')
 fn = room + '_C4_' + timestamp
 fn1 = room + '_C4_' + timestamp + '.flv'
 fn2 = room + '_C4_' + timestamp + '.mp4'
 fn3 = room + '_C4_' + timestamp + '.ts'
 fn4 = room + '_C4_' + timestamp + '.txt'
 pf1 = (path + fn1)
 pf2 = (path + fn2)
 pf3 = (path + fn3)
 pf4 = (path + fn4)
 rtmp = config.get('files', 'rtmpdump')
 ffplay = config.get('files', 'ffplay')
 ffmpeg = config.get('files', 'ffmpeg')
 youtube = config.get('files', 'youtube')
 streamlink = config.get('files', 'streamlink')

 if mod == 'FFPLAY':
    print (colored('\n => FFPLAY => {} <=', 'yellow', 'on_magenta')).format(fn)
    command = '{} -loglevel panic -i {} -infbuf -autoexit -x 640 -y 480 -window_title "{} * {} * {} * {}"'.format(ffplay,hlsurl,room,loc,stime,mn)
    os.system(command)
    print(colored('\n => END <=', 'yellow','on_blue'))

 if mod == 'RTMP':
    print (colored('\n => RTMP-REC => {} <=', 'yellow', 'on_red')).format(fn1)
    print
    command = '{} -r"rtmp://{}/cam4-edge-live" -a"cam4-edge-live" -W"{}" --live -y"{}" -o"{}"'.format(rtmp,vau,swf,vpu,pf1)
    os.system(command)
    print(colored('\n => END <=', 'yellow','on_blue'))

 if mod == 'FFMPEG':
    print (colored('\n => FFMPEG-REC => {} <=', 'yellow', 'on_red')).format(fn1)
    command = ('{} -loglevel panic -i {} -c:v copy -c:a aac -b:a 160k {}'.format(ffmpeg,hlsurl,pf1))
    os.system(command)
    print(colored('\n => END <=', 'yellow','on_blue'))

 if mod == 'SL':
    print (colored('\n => SL-REC >>> {} <<<\n', 'yellow', 'on_red')).format(fn2)
    command = ('{} hls://{} best -Q -o {}'.format(streamlink,hlsurl,pf2))
    os.system(command)
    print(colored('\n => END <=', 'yellow','on_blue'))

 if mod == 'YTDL':
    print (colored('\n => YTDL-REC => {} <=', 'yellow', 'on_red')).format(fn3)
    command = ('{} -i --hls-use-mpegts --no-part -q {} -o {}'.format(youtube,hlsurl,pf3))
    os.system(command)
    print(colored('\n => END <=', 'yellow','on_blue'))

 if mod == 'URL':
    print (colored('\n => URL => {} <=', 'yellow', 'on_green')).format(fn4)
    file=open(pf4,'wb')
    file.write(hlsurl)
    file.close()
    raw_input(colored('\n => Press Enter to exit <=', 'yellow', 'on_blue'))
    print(colored('\n => END <=', 'yellow','on_blue'))

 if mod == 'EXIT':
    print(colored('\n => END <=', 'yellow','on_blue'))
    time.sleep(3)
    sys.exit()

else:
   print (colored('\n => Model ({}) is OFFLINE or ERROR name <=', 'white', 'on_red')).format(model)
   time.sleep(3)
   print(colored('\n => END <=', 'yellow','on_blue'))
   time.sleep(1)
   sys.exit()
