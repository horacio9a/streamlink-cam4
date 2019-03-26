cam4-anonymous
====================
cam4-anonymous lets you follow and archive your selected models' shows on www.cam4.com
You don't need to be registered cam4 user for recording models with this cam4-anonymous script.

Requirements
============
1. [Python 2.7.16](https://www.python.org/ftp/python/2.7.16/python-2.7.16.msi) instalation. Those who need to install python should watch this [video](https://www.youtube.com/watch?v=QYUBz4mrnFU)
2. [RTMPDump(ksv)](https://github.com/K-S-V/Scripts/releases) used for recording the streams.
3. [ffmpeg and ffplay](https://ffmpeg.zeranoe.com/builds/) who must be somewere in the path, default location is 'C:/Windows'
4. [youtube-dl](https://github.com/rg3/youtube-dl) who must be somewere in the path, default location is 'C:/Windows'

Setup
=====
1. Install requirements `pip install -r Requirements.txt`
2. Download and unpack the [code](https://codeload.github.com/horacio9a/cam4-anonymous/zip/master).
3. Open console and go into the directory where you unpacked the files (default is C:/-c4-py/)
4. c4.bat can be anywhere (default is C:/Windows)
5. Edit `config.cfg` to your wish or accept default data.

Running & Output
================
It's best to use 'Command Promt' first to install `Requirements.txt`. You can also install the modules individually with the command 'pip install SomePackage==1.0.4 # specific version'
For use these scripts it would be good to make a shortcut for `c4.bat` and put it in the task bar for easier startup. 
All scripts using the same text file where is stored models for recordings, default is `C:\-c4-py\C4_Model.txt`. 
However, if you want to record a certain model permanently (24/7), then you need to use `c4.bat`, options numbers 2 to 5 for start rtmpdump, youtube-dl, ffmpeg or streamlink.
Default script is 'c4a.py' letter 'a' in the name means 'ALL' for 'all mode' record and play with hidden script traffic. 
Script 'c4aw.py' letter 'w' in the name means 'window' allow you to see what is actually happening in a separate window and make it easier to stop recording.
If you want to record more models at the same time then you need to start another copy of `c4.bat`. 
All scripts have the ability to display some basic data about the models (Age, Location, Relationship Status and Occupation - Job).
Break recording is with with Ctrl-C or by clicking 'x' at the top right corner of the script window If Ctrl-C does not react.

screenshot0:

![alt screenshot](./screenshot0.jpg)

screenshot1:

![alt screenshot](./screenshot1.jpg)

screenshot2:

![alt screenshot](./screenshot2.jpg)
