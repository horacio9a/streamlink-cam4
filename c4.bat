@ECHO OFF
SETLOCAL EnableDelayedExpansion
:START
CLS
ECHO.
SET /P MODE=EXIT(6)  START(5)  C4YTR(4)  C4SLR(3)  C4FFR(2)  C4RR(1)  C4(0)(ENTER)(%MODE%): 
IF "%MODE%"=="" GOTO C4
IF "%MODE%"=="0" GOTO C4
IF "%MODE%"=="1" GOTO C4RR
IF "%MODE%"=="2" GOTO C4FFR
IF "%MODE%"=="3" GOTO C4SLR
IF "%MODE%"=="4" GOTO C4YTR
IF "%MODE%"=="5" GOTO START
IF "%MODE%"=="6" GOTO EXIT
:C4
ECHO.
CLS && ECHO #################################################
ECHO ### C4 #####  P Y T H O N   R E C / P L A Y  ####
ECHO #################################################
cd C:/
COLOR 0F
cd -c4-py
start python c4.py
ECHO.
PAUSE
GOTO START
:C4RR
ECHO.
SET n=0
FOR /F "tokens=*" %%A IN (C:/Windows/C4_Model.txt) DO (
SET /A n=n+1
SET _fav!n!=%%A
ECHO !n! %%A
)
ECHO.
SET /P MODEL=Choose C4 Model Name (%M% %MODEL%): 
FOR /L %%f IN (1,1,!n!) DO (
IF /I '%MODEL%'=='%%f' SET M=%%f
)
SET n=0
FOR /F "tokens=*" %%A IN (C:/Windows/C4_Model.txt) DO (
SET /A n=n+1
IF !n!==%M% SET MODEL=%%A
)
:C4RR_
ECHO.
SET MODELNAME=%MODEL% ############ %M% ############################
SET _MODEL_=%MODELNAME:~0,33%
ECHO.
CLS && ECHO #################################################
ECHO ### C4RR ###### P Y T H O N   R E C #### 24/7 ###
ECHO ### RTMP ###### %_MODEL_%
ECHO #################################################
cd C:/
COLOR 0F
cd -c4-py
python c4rr.py %MODEL%
TIMEOUT 30
GOTO C4RR_
:C4FFR
ECHO.
SET n=0
FOR /F "tokens=*" %%A IN (C:/Windows/C4_Model.txt) DO (
SET /A n=n+1
SET _fav!n!=%%A
ECHO !n! %%A
)
ECHO.
SET /P MODEL=Choose C4 Model Name (%M% %MODEL%): 
FOR /L %%f IN (1,1,!n!) DO (
IF /I '%MODEL%'=='%%f' SET M=%%f
)
SET n=0
FOR /F "tokens=*" %%A IN (C:/Windows/C4_Model.txt) DO (
SET /A n=n+1
IF !n!==%M% SET MODEL=%%A
)
:C4FFR_
ECHO.
SET MODELNAME=%MODEL% ############ %M% ############################
SET _MODEL_=%MODELNAME:~0,33%
ECHO.
CLS && ECHO #################################################
ECHO ### C4FFR ##### P Y T H O N   R E C #### 24/7 ###
ECHO ### FFMPEG #### %_MODEL_%
ECHO #################################################
cd C:/
COLOR 0F
cd -c4-py
python c4ffr.py %MODEL%
TIMEOUT 30
GOTO C4FFR_
:C4SLR
ECHO.
SET n=0
FOR /F "tokens=*" %%A IN (C:/Windows/C4_Model.txt) DO (
SET /A n=n+1
SET _fav!n!=%%A
ECHO !n! %%A
)
ECHO.
SET /P MODEL=Choose C4 Model Name (%M% %MODEL%): 
FOR /L %%f IN (1,1,!n!) DO (
IF /I '%MODEL%'=='%%f' SET M=%%f
)
SET n=0
FOR /F "tokens=*" %%A IN (C:/Windows/C4_Model.txt) DO (
SET /A n=n+1
IF !n!==%M% SET MODEL=%%A
)
:C4SLR_
ECHO.
SET MODELNAME=%MODEL% ############ %M% ############################
SET _MODEL_=%MODELNAME:~0,33%
ECHO.
CLS && ECHO #################################################
ECHO ### C4SLR ##### P Y T H O N   R E C #### 24/7 ###
ECHO ### SL ######## %_MODEL_%
ECHO #################################################
cd C:/
COLOR 0F
cd -c4-py
python c4slr.py %MODEL%
TIMEOUT 30
GOTO C4SLR_
:C4YTR
ECHO.
SET n=0
FOR /F "tokens=*" %%A IN (C:/Windows/C4_Model.txt) DO (
SET /A n=n+1
SET _fav!n!=%%A
ECHO !n! %%A
)
ECHO.
SET /P MODEL=Choose C4 Model Name (%M% %MODEL%): 
FOR /L %%f IN (1,1,!n!) DO (
IF /I '%MODEL%'=='%%f' SET M=%%f
)
SET n=0
FOR /F "tokens=*" %%A IN (C:/Windows/C4_Model.txt) DO (
SET /A n=n+1
IF !n!==%M% SET MODEL=%%A
)
:C4YTR_
ECHO.
SET MODELNAME=%MODEL% ############ %M% ############################
SET _MODEL_=%MODELNAME:~0,33%
ECHO.
CLS && ECHO #################################################
ECHO ### C4YTR ##### P Y T H O N   R E C #### 24/7 ###
ECHO ### YTDL ###### %_MODEL_%
ECHO #################################################
cd C:/
COLOR 0F
cd -c4-py
python c4ytr.py %MODEL%
TIMEOUT 30
GOTO C4YTR_
:EXIT
GOTO :EOF
ENDLOCAL
