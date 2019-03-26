@ECHO OFF
SETLOCAL EnableDelayedExpansion
:START
CLS
SET n=0
FOR /F "tokens=*" %%A IN (C:\Windows\C4_Model.txt) DO (
SET /A n=n+1
SET _fav!n!=%%A
ECHO !n! %%A
)
ECHO.
SET /P MODEL=Select CAM4 Model (%M% %MODEL%): 
FOR /L %%f IN (1,1,!n!) DO (
IF /I '%MODEL%'=='%%f' SET M=%%f
)
SET n=0
FOR /F "tokens=*" %%A IN (C:\Windows\C4_Model.txt) DO (
SET /A n=n+1
IF !n!==%M% SET MODEL=%%A
)
ECHO.
SET /P MODE=EXIT(3)  START(2)  C4-SL-R(24/7)(1)  C4-SL(0)(ENTER)(%MODE%): 
IF "%MODE%"=="" GOTO C4-SL
IF "%MODE%"=="0" GOTO C4-SL
IF "%MODE%"=="1" GOTO C4-SL-R
IF "%MODE%"=="2" GOTO START
IF "%MODE%"=="3" GOTO EXIT
:C4-SL
ECHO.
CLS && ECHO #####################################################
ECHO ### C4-SL #####  R E C O R D I N G  -  C A M 4  #####
SET hour=%time:~0,2%
IF "%hour:~0,1%" == " " SET hour=0%hour:~1,1%
SET NOW=%date:~4,2%%date:~7,2%%date:~10,4%-%hour%%time:~3,2%%time:~6,2%
FOR /f "tokens=1-2 delims=/:" %%a IN ('time /t') DO (set mytime=%%a%%b)
SET OUT_DIR=C:\Videos\Cam4\
SET FILENAME=%MODEL%_C4_%NOW%.flv
SET OUTPUT=%OUT_DIR%%FILENAME%
SET FNAME=######## %FILENAME% ### %M% ##############################
SET _FNAME_=%FNAME:~5,53%
IF EXIST "%OUT_DIR%" (ECHO %_FNAME_%) ELSE (MD "%OUT_DIR%"
ECHO %_FNAME_%)
ECHO #####################################################
ECHO.
COLOR 0F
cd/
cd Python27/Scripts
START STREAMLINK "https://www.cam4.com/%MODEL%/"
PAUSE
GOTO START
:C4-SL-R
ECHO.
CLS && ECHO #####################################################
ECHO ### C4-SL-R ###  R E C O R D I N G  -  2 4 / 7  #####
SET hour=%time:~0,2%
IF "%hour:~0,1%" == " " SET hour=0%hour:~1,1%
SET NOW=%date:~4,2%%date:~7,2%%date:~10,4%-%hour%%time:~3,2%%time:~6,2%
FOR /f "tokens=1-2 delims=/:" %%a IN ('time /t') DO (set mytime=%%a%%b)
SET OUT_DIR=C:\Videos\Cam4\
SET FILENAME=%MODEL%_C4_%NOW%.flv
SET OUTPUT=%OUT_DIR%%FILENAME%
SET FNAME=######## %FILENAME% ### %M% ##############################
SET _FNAME_=%FNAME:~5,53%
IF EXIST "%OUT_DIR%" (ECHO %_FNAME_%) ELSE (MD "%OUT_DIR%"
ECHO %_FNAME_%)
ECHO #####################################################
ECHO.
COLOR 0F
cd/
cd Python27/Scripts
STREAMLINK "https://www.cam4.com/%MODEL%/"
TIMEOUT 30
GOTO C4-SL-R
:EXIT
GOTO :EOF
ENDLOCAL
