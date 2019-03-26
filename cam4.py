# Cam4 Streamlink RTMPDUMP Remote 24/7 Plugin v.1.0.1 by @horacio9a for Python 2.7.16

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
           time.sleep(3)
           sys.exit()

        if match:
         try:
          hls_streams = HLSStream.parse_variant_playlist(self.session,match.group('hls_url'),headers={'Referer': self.url})
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

           timestamp = str(time.strftime("%d%m%Y-%H%M%S"))
           path = config.get('folders', 'output_folder_C4')
           fn = rname + '_C4_' + timestamp + '.flv'
           pf1 = (path + fn)
           rtmp = config.get('files', 'rtmpdump')
           print (colored(' => RTMP-24/7-REC => {} <=', 'yellow', 'on_red')).format(fn)
           print
           command = '{} -r"{}" -a"cam4-edge-live" -W"{}" --live -y"{}" -o"{}"'.format(rtmp,vau,swf,vpu,pf1)
           os.system(command)
           sys.exit()

         except Exception as e:
          if '404' in str(e):
           print(colored("\n => Performer is AWAY or PRIVATE <=","yellow","on_red"))
           print
           print(colored("\n => END <= ", 'yellow','on_blue'))
           time.sleep(3)
           sys.exit()

__plugin__ = cam4
