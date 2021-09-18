# Cam4 Streamlink FFMPEG/STREAMLINK/LIVESTREAM/YOUTUBE-DL Plugin v.2.0.0 by @horacio9a for Python 2.7.18
# coding: utf-8

import os, sys, re, time, command

reload(sys)
sys.setdefaultencoding('utf-8')
from streamlink.plugin import Plugin
from streamlink.plugin.api import validate
from streamlink.stream import HLSStream
from datetime import datetime
from colorama import init, Fore, Back, Style
from termcolor import colored
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read('config.ini')

init()

STREAM_INFO = "https://www.cam4.com/rest/v1.0/profile/{0}/streamInfo"
INFO_URL = "https://www.cam4.com/rest/v1.0/search/performer/{0}"
PROFILE_URL = "https://www.cam4.com/rest/v1.0/profile/{0}/info"

_url_re = re.compile(r"https?://(\w+\.)?cam4\.com/(?P<username>\w+)")

class Cam4(Plugin):
    @classmethod
    def can_handle_url(cls, url):
        return _url_re.match(url)

    def _get_streams(self):
        match = _url_re.match(self.url)
        username = match.group("username")

        res = self.session.http.get(INFO_URL.format(username))
        data = self.session.http.json(res)
        print
        self.logger.info("Username: {0}".format(data["username"]))
        name = data["username"]
        online = data["online"]
        self.logger.info("Online: {0}".format(data["online"]))
        self.logger.info("Country: {0}".format(data["country"]))
        res = self.session.http.get(PROFILE_URL.format(username))
        data = self.session.http.json(res)
        self.logger.info("City: {0}".format(data["city"]))
        self.logger.info("Sex Preference: {0}".format(data["sexPreference"]))
        self.logger.info("Ethnicity: {0}".format(data["ethnicity"]))
        self.logger.info("Main Language: {0}".format(data["mainLanguage"]))
        self.logger.info("Breast Size: {0}".format(data["breastSize"]))
        self.logger.info("Birthdate: {0}".format(data["birthdate"]))
        self.logger.info("Age: {0}".format(int((datetime.now() - datetime.strptime(data["birthdate"], "%Y-%m-%d")).days / 365)))

        if online:
            res = self.session.http.get(STREAM_INFO.format(username))
            data = self.session.http.json(res)
            if data["canUseCDN"]:
              hlsurl = data["cdnURL"]
              while True:
               try:
                print
                mode = int(raw_input(colored(" => MODE => EXIT(6) => URL(5) => YTDL(4) => LS(3) => SL(2) => FFMPEG(1) => PLAYER(0) => ", "white", "on_blue")))
                break
               except ValueError:
                print(colored("\n => Input must be a number <=", "white", "on_red"))
              if mode == 0:
                mod = 'PLAYER'
              if mode == 1:
                mod = 'FFMPEG'
              if mode == 2:
                mod = 'SL'
              if mode == 3:
                mod = 'LS'
              if mode == 4:
                mod = 'YTDL'
              if mode == 5:
                mod = 'URL'
              if mode == 6:
                mod = 'EXIT'

              timestamp = str(time.strftime("%d%m%Y-%H%M%S"))
              stime = str(time.strftime("%H:%M:%S"))
              path = Config.get('folders', 'output_folder_C4')
              fn = name + '_C4_' + timestamp
              fn1 = name + '_C4_' + timestamp + '.flv'
              fn2 = name + '_C4_' + timestamp + '.mp4'
              fn3 = name + '_C4_' + timestamp + '.ts'
              fn4 = name + '_C4_' + timestamp + '.txt'
              pf1 = (path + fn1)
              pf2 = (path + fn2)
              pf3 = (path + fn3)
              pf4 = (path + fn4)
              player = Config.get('files', 'player')
              ffmpeg = Config.get('files', 'ffmpeg')
              streamlink = Config.get('files', 'streamlink')
              livestreamer = Config.get('files', 'livestreamer')
              youtube = Config.get('files', 'youtube')

              if mod == 'PLAYER':
                 print
                 print (colored(' => PLAYER => {} <=', 'white', 'on_magenta')).format(fn)
                 print
                 command = ('{} -p {} hlsvariant://{} best'.format(livestreamer, player, hlsurl))
                 os.system(command)
                 while True:
                    try:
                       print
                       prog = int(raw_input(colored(' => Mode => URL(5) - YTDL(4) - LS(3) - SL(2) - FFMPEG(1) - Exit(0) => ', 'white', 'on_green')))
                       break
                    except ValueError:
                       print
                       print(colored(' => Input must be a number <=', 'white', 'on_red'))
                 if prog > 5:
                    print
                    print(colored(' => Too big number <=', 'white', 'on_red'))
                    mod = 'EXIT'
                 if prog == 0:
                    mod = 'EXIT'
                 if prog == 1:
                    mod = 'FFMPEG'
                 if prog == 2:
                    mod = 'SL'
                 if prog == 3:
                    mod = 'LS'
                 if prog == 4:
                    mod = 'YTDL'
                 if prog == 5:
                    mod = 'URL'

              if mod == 'FFMPEG':
                 print (colored("\n => FFMPEG-REC => {} <=","white","on_red")).format(fn1)
                 print
                 command = ('{} -hide_banner -loglevel panic -i {} -c:v copy -c:a aac -b:a 160k {}'.format(ffmpeg,hlsurl,pf1))
                 os.system(command)

              if mod == 'SL':
                 print
                 print (colored(' => SL-REC => {}  (  Size  @   Speed   ) <=', 'white', 'on_red')).format(fn2)
                 print
                 command = ('{} hls://{} best -Q --hls-live-edge 1 --hls-playlist-reload-attempts 9 --hls-segment-threads 3 --hls-segment-timeout 5.0 --hls-timeout 20.0 -o {}'.format(streamlink,hlsurl,pf2))
                 os.system(command)

              if mod == 'LS':
                 print
                 print (colored(' => LS-REC => {}  (  Size  @   Speed   ) <=', 'white', 'on_red')).format(fn2)
                 print
                 command = ('{} hlsvariant://{} best -Q -o {}'.format(livestreamer,hlsurl,pf2))
                 os.system(command)

              if mod == 'YTDL':
                 print
                 print (colored(' => YTDL-REC => {} <=', 'white', 'on_red')).format(fn3)
                 command = ('{} -i --geo-bypass --hls-use-mpegts --no-part -q --no-warnings --no-check-certificate {} -o {}'.format(youtube,hlsurl,pf3))
                 os.system(command)

              if mod == 'URL':
                 print
                 print (colored(' => URL => {} <=', 'white', 'on_green')).format(fn4)
                 file=open(pf4,'w')
                 file.write(hlsurl)
                 file.close()
				   
            else:
                 print
                 print(colored(' => Performer is in PRIVATE SHOW <=',"white","on_red"))
                 print
                 print(colored(' => END <= ', 'white','on_blue'))
                 time.sleep(3)
                 sys.exit()
				 				
        else:
             print
             print(colored(' => Performer is OFFLINE <=', 'white','on_red'))
             print
             print(colored(' => END <=', 'white','on_blue'))
             time.sleep(3)
             sys.exit()

__plugin__ = Cam4