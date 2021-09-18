# Cam4 Streamlink LIVESTREAMER Remote 24/7 Plugin v.2.0.0 by @horacio9a for Python 2.7.18
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
              timestamp = str(time.strftime("%d%m%Y-%H%M%S"))
              stime = str(time.strftime("%H:%M:%S"))
              path = Config.get('folders', 'output_folder_C4')
              fn = name + '_C4_' + timestamp + '.mp4'
              pf = (path + fn)
              livestreamer = Config.get('files', 'livestreamer')
              print
              print (colored(' => LS-247 => {}  (  Size  @   Speed   ) <=', 'white', 'on_red')).format(fn)
              print
              command = ('{} hlsvariant://{} best -Q -o {}'.format(livestreamer,hlsurl,pf))
              os.system(command)
              sys.exit()
				   
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