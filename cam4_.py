# Cam4 Streamlink RTMPDUMP/FFMPEG/FFPLAY/STREAMLINK/YOUTUBE-DL Plugin v.1.0.0 by @horacio9a for Python 2.7.14

import os, sys, re, time, datetime, command

from streamlink.plugin import Plugin
from streamlink.plugin.api import http, useragents, validate
from streamlink.stream import HLSStream, RTMPStream
from streamlink.utils import update_scheme
from streamlink.utils import parse_json
from colorama import init, Fore, Back, Style
from termcolor import colored
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('config.cfg')

init()

class cam4(Plugin):
    _url_re = re.compile(r'http(s)?://([a-z]+\.)?(cam4\.com)/.+')
    _video_data_re = re.compile(r"flashData: (?P<flash_data>{.*}), hlsUrl: '(?P<hls_url>.+?)'")
    _flash_data_schema = validate.Schema(
        validate.all(
            validate.transform(parse_json),
            validate.Schema({
                'playerUrl': validate.url(),
                'flashVars': validate.Schema({
                    'videoPlayUrl': validate.text,
                    'videoAppUrl': validate.url(scheme='rtmp')
                })
            })
        )
    )
    @classmethod
    def can_handle_url(cls, url):
        return cam4._url_re.match(url)

    def _get_streams(self):
        res = http.get(self.url, headers={'User-Agent': useragents.ANDROID})
        match = self._video_data_re.search(res.text)
        if match is None:
           print(colored("\n => Performer is OFFLINE <=","yellow","on_red"))
           print(colored("\n => END <= ", 'yellow','on_blue'))
           time.sleep(6)
           sys.exit()

        if match:
         try:
          hls_streams = HLSStream.parse_variant_playlist(self.session,match.group('hls_url'),headers={'Referer': self.url})
          print (colored("\n => HLS STREAMS => {} <=", "yellow", "on_blue")).format(hls_streams)
          for s in hls_streams.items():
           rtmp_video = self._flash_data_schema.validate(match.group('flash_data'))
           swf = rtmp_video['playerUrl']
           flashvars = rtmp_video['flashVars']
           rtmp_stream = RTMPStream(self.session, {'rtmp': rtmp_video['flashVars']['videoAppUrl'],'playpath': rtmp_video['flashVars']['videoPlayUrl'],'swfUrl': rtmp_video['playerUrl']})
           vpu = flashvars['videoPlayUrl']
           rname = vpu.split('-')[0]
           wcdn = vpu.split('-')[1]
           print (colored("\n => PLAY URL => {} <=\n", "yellow", "on_blue")).format(vpu)
           vau = flashvars['videoAppUrl']
           print (colored(" => APP URL => {} <=\n", "yellow", "on_blue")).format(vau)
           hlsurl = 'https://lwcdn-{}.cam4.com/cam4-origin-live/{}_aac/chunklist.m3u8'.format(wcdn,vpu)
           print (colored(" => HLS URL => {} <=", "yellow", "on_blue")).format(hlsurl)
           while True:
            try:
             print
             mode = int(raw_input(colored(" => MODE => EXIT(5) => YTDL(4) => SL(3) => FFMPEG(2) => FFPLAY(1) => RTMP(0) => ", "yellow", "on_blue")))
             break
            except ValueError:
             print(colored("\n => Input must be a number <=", "yellow", "on_red"))
           if mode == 0:
             mod = 'RTMP'
           if mode == 1:
             mod = 'FFPLAY'
           if mode == 2:
             mod = 'FFMPEG'
           if mode == 3:
             mod = 'SL'
           if mode == 4:
             mod = 'YTDL'
           if mode == 5:
             mod = 'EXIT'

           timestamp = str(time.strftime("%d%m%Y-%H%M%S"))
           stime = str(time.strftime("%H:%M:%S"))
           path = config.get('folders', 'output_folder_C4')
           fn = rname + '_C4_' + timestamp
           fn1 = rname + '_C4_' + timestamp + '.flv'
           fn2 = rname + '_C4_' + timestamp + '.mp4'
           fn3 = rname + '_C4_' + timestamp + '.ts'
           pf1 = (path + fn1)
           pf2 = (path + fn2)
           pf3 = (path + fn3)
           rtmp = config.get('files', 'rtmpdump')
           ffmpeg = config.get('files', 'ffmpeg')
           ffplay = config.get('files', 'ffplay')
           streamlink = config.get('files', 'streamlink')
           youtube = config.get('files', 'youtube')

           if mod == 'RTMP':
              print
              print (colored(' => RTMP-REC => {} <=', 'yellow', 'on_red')).format(fn1)
              print
              command = '{} -r"{}" -a"cam4-edge-live" -W"{}" --live -q -y"{}" -o"{}"'.format(rtmp,vau,swf,vpu,pf1)
              os.system(command)
              print(colored(" => END <=", 'yellow','on_blue'))

           if mod == 'FFPLAY':
              print (colored("\n => FFPLAY => {} <=", "yellow", "on_magenta")).format(fn)
              command = ('{} -hide_banner -loglevel panic -i {} -infbuf -autoexit -window_title "{} * {}"'.format(ffplay,hlsurl,rname,stime))
              os.system(command)
              print(colored(" => END <= ", "yellow","on_blue"))

           if mod == 'FFMPEG':
              print (colored("\n => FFMPEG-REC => {} <=","yellow","on_red")).format(fn1)
              print
              command = ('{} -hide_banner -loglevel panic -i {} -c:v copy -c:a aac -b:a 160k {}'.format(ffmpeg,hlsurl,pf1))
              os.system(command)
              print(colored(" => END <= ", "yellow","on_blue"))

           if mod == 'SL':
              print (colored('\n => SL-REC >>> {} <<<', 'yellow', 'on_red')).format(fn2)
              print
              command = ('{} hls://"{}" best -Q -o "{}"'.format(streamlink,hlsurl,pf2))
              os.system(command)
              print(colored(" => END <= ", 'yellow','on_blue'))

           if mod == 'YTDL':
              print (colored('\n => YTDL-REC => {} <=', 'yellow', 'on_red')).format(fn3)
              command = ('{} --hls-use-mpegts --no-part -q {} -o {}'.format(youtube,hlsurl,pf3))
              os.system(command)
              print(colored("\n => END <= ", 'yellow','on_blue'))

           if mod == 'EXIT':
              print(colored("\n => END <= ", 'yellow','on_blue'))
              time.sleep(3)
              sys.exit()

         except Exception as e:
            if '404' in str(e):
               print(colored("\n => Performer is AWAY or PRIVATE <=","yellow","on_red"))
               print(colored("\n => END <= ", 'yellow','on_blue'))
               time.sleep(6)
               sys.exit()

__plugin__ = cam4
