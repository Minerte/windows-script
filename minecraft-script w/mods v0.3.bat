@echo off

ECHO Hello! First see if fabric loader is installed
ECHO If not press n and it will download. And if you have installed press y, and it will begin to install the mods.
ECHO NOTE! If using another launcher please change directory of the fabric installer.
ECHO Or if using Prism launcher you can Press y. The guide will continue after This action.
ECHO NOTE! I only have tested this with Prism launcher and default launcher. And the script is only build for those TWO LAUNCHER.

:Promptname
set choice=
set /P "choice=Did you have Fabric loader installed? "

if '%choice%'== 'n' goto fabric-installer
if '%choice%'== 'y' goto mods-installer

goto start
:fabric-installer
ECHO We will now start to install the fabric modloader.

cd %userprofile%/downloads
timeout /t 3
curl --output fabric-installer-1.0.1.exe https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.1/fabric-installer-1.0.1.exe

timeout /t 5
ECHO We will now execute fabric installer.
start /d %userprofile%\downloads fabric-installer-1.0.1.exe

ECHO When Fabric is done installing. Close the window and comback to this tab.

PAUSE

ECHO Now everything should be done.
ECHO Now we need to install the mods!
ECHO If user choice is Prism Launcher, Have a instance call fabric-0.15.11-1.20.1.
ECHO And launch it and the close it, This is to make it create files.
ECHO In the next ACTION you need to choose Launcher.
ECHO Default Minecraft launcher : 1
ECHO Prism Launcher : 2

:PromptName
set choose=
set /P "choose=Please select launcher:  "

if '%choose%'=='1' goto Mine
if '%choose%'=='2' goto Prism

goto start
:Mine
ECHO You will install the mods for the default launcher.

cd %AppData%\.minecraft

ECHO IF continue it will delet and remake the file/folder. If user want to backup the existing files/folder.
ECHO User need to do it manually.

PAUSE

ECHO Select yes. This will delete the file and remake it.

del %AppData%\.minecraft\mods
rmdir /S %AppData%\.minecraft\mods

timeout /t 10
mkdir %AppData%\.minecraft\mods

timeout /t 3
cd %AppData%\.minecraft\mods

ECHO Now it will install the mods.
ECHO IGNORE THE ERROR/WARNINGS AFTER DOWNLOADS COMPLETION.
timeout /t 10

curl -Lo mods.zip https://www.dropbox.com/scl/fo/qwxafrf75jx37p7n7rwjq/AJH_pzG9f2gsJiThkTIcz-U?rlkey=83ccfhqm44y6bu8ghd9yrif9w&e=1&st=tezyrw8a&dl=0
tar -xf mods.zip

timeout /t 3
del mods.zip

ECHO EVERTHING SHOULD BE FINE???? IDK man hahahhaha
goto end

goto start
:Prism
ECHO You will install the mods for Prism Launcher!

cd %AppData%\PrismLauncher\instances\fabric 0.15.11 1.20.1\.minecraft

ECHO IF continue it will delet and remake the file/folder. If user want to backup the existing files/folder.
ECHO User need to do it manually.

PAUSE

ECHO Select yes. This will delete the file and remake it.

del %AppData%\PrismLauncher\instances\fabric-0.15.11-1.20.1\.minecraft\mods
rmdir /S %AppData%\PrismLauncher\instances\fabric-0.15.11-1.20.1\.minecraft\mods

timeout /t 10
mkdir %AppData%\PrismLauncher\instances\fabric-0.15.11-1.20.1\.minecraft\mods

timeout /t 3
cd %AppData%\PrismLauncher\instances\fabric-0.15.11-1.20.1\.minecraft\mods

ECHO Now it will install the mods.
ECHO IGNORE THE ERROR/WARNINGS AFTER DOWNLOADS COMPLETION.

timeout /t 10

curl -Lo mods.zip https://www.dropbox.com/scl/fo/qwxafrf75jx37p7n7rwjq/AJH_pzG9f2gsJiThkTIcz-U?rlkey=83ccfhqm44y6bu8ghd9yrif9w&e=1&st=tezyrw8a&dl=0
tar -xf mods.zip

timeout /t 3
del mods.zip

ECHO EVERTHING SHOULD BE FINE???? IDK man hahahhaha
goto end

goto end # THIS IS THE EN OF MODS AND FABRIC INSTALLER

#THIS IS THE END OF FABRIC INSTALLER
#Space
#Space

goto start
:mods-installer

ECHO Hello! So you want to install mods.
ECHO If user choice is Prism Launcher, Have a instance call fabric-0.15.11-1.20.1.
ECHO And launch it and the close it, This is to make it create files.

ECHO In the next ACTION you need to choose Launcher.
ECHO Default Minecraft launcher : 1
ECHO Prism Launcher : 2

:PromptName
set choose=
set /P "choose=Please select launcher:  "

if '%choose%'=='1' goto Mine
if '%choose%'=='2' goto Prism

goto start
:Mine
ECHO You will install the mods for the default launcher.

cd %AppData%\.minecraft

ECHO IF continue it will delet and remake the file/folder. If user want to backup the existing files/folder.
ECHO User need to do it manually.

PAUSE

ECHO Select yes. This will delete the file and remake it.

del %AppData%\.minecraft\mods
rmdir /S %AppData%\.minecraft\mods

timeout /t 10
mkdir %AppData%\.minecraft\mods

timeout /t 3
cd %AppData%\.minecraft\mods

ECHO Now it will install the mods.
ECHO IGNORE THE ERROR/WARNINGS AFTER DOWNLOADS COMPLETION.
timeout /t 10

curl -Lo mods.zip https://www.dropbox.com/scl/fo/qwxafrf75jx37p7n7rwjq/AJH_pzG9f2gsJiThkTIcz-U?rlkey=83ccfhqm44y6bu8ghd9yrif9w&e=1&st=tezyrw8a&dl=0
tar -xf mods.zip

timeout /t 3
del mods.zip

ECHO EVERTHING SHOULD BE FINE???? IDK man hahahhaha
goto end

goto start
:Prism
ECHO You will install the mods for Prism Launcher!

cd %AppData%\PrismLauncher\instances\fabric 0.15.11 1.20.1\.minecraft

ECHO IF continue it will delet and remake the file/folder. If user want to backup the existing files/folder.
ECHO User need to do it manually.

PAUSE

ECHO Select yes. This will delete the file and remake it.

del %AppData%\PrismLauncher\instances\fabric-0.15.11-1.20.1\.minecraft\mods
rmdir /S %AppData%\PrismLauncher\instances\fabric-0.15.11-1.20.1\.minecraft\mods

timeout /t 10
mkdir %AppData%\PrismLauncher\instances\fabric-0.15.11-1.20.1\.minecraft\mods

timeout /t 3
cd %AppData%\PrismLauncher\instances\fabric-0.15.11-1.20.1\.minecraft\mods

ECHO Now it will install the mods.
ECHO IGNORE THE ERROR/WARNINGS AFTER DOWNLOADS COMPLETION.

timeout /t 10

curl -Lo mods.zip https://www.dropbox.com/scl/fo/qwxafrf75jx37p7n7rwjq/AJH_pzG9f2gsJiThkTIcz-U?rlkey=83ccfhqm44y6bu8ghd9yrif9w&e=1&st=tezyrw8a&dl=0
tar -xf mods.zip

timeout /t 3
del mods.zip

ECHO EVERTHING SHOULD BE FINE???? IDK man hahahhaha
goto end


goto end # THIS END MODS-INSTALLER???

:end
PAUSE
