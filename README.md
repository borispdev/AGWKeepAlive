![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PowerShell](https://img.shields.io/badge/PowerShell-%235391FE.svg?style=for-the-badge&logo=powershell&logoColor=white)

# AGW KeepAlive

> Easy to use connectivity test and communication keep alive windows service.
> Intended to use with Alaris Gateway Workstations with firmware v1.3.x.

## Table of Contents

- [AGW KeepAlive](#agw-keepalive)
  - [Table of Contents](#table-of-contents)
  - [General Information](#general-information)
  - [Technologies Used](#technologies-used)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Get latest release](#get-latest-release)
    - [Install service](#install-service)
    - [Configure](#configure)
  - [Usage](#usage)
    - [Run service](#run-service)
    - [Stop service](#stop-service)
    - [Test connectivity](#test-connectivity)
    - [Uninstall](#uninstall)
  - [Project Status](#project-status)
  - [Contact](#contact)
  - [License](#license)


## General Information

- Alaris Gateway Workstations (AGW) act as a passive component on a network, without getting requests from external software they remain "silent". Some network appliances like layer 3 switch or a plain layer 2 switch with "port sleep" option enabled can disconnect AGW and delete its MAC from arp table resulting in AGW disconnection.
- This service is built to prevent AGW passive behavior and disconnection in absence of infusion data acquisition software like ACE or Digistat. AGW KeepAlive service sending http GET requests to the `portal.xml` endpoint of each AGW and checks response code for any errors.
- In addition to keep alive function, a simple log file functionality is provided and can help identify various connectivity problems.


## Technologies Used
- Python - v3.11
- Pywin32 - v306
- Requests - v2.31
- Pyinstaller - v6.5.0

## Features

- Keeping AGW constantly connected.
- Logging connectivity errors and service status.
- Easy `*.toml` file configuration.

## Prerequisites
- Windows PC on the same network with AGW. Compatible OS:
	- Windows 10.
	- Windows 11.
	- Windows Server 2016, 2019 or 2022.
- Local administrator permissions.
- List of AGW IP addresses to be kept alive. 


## Setup
### Get latest release
- Download `AGWKeepAlive_X_X.zip` latest version from [releases section](https://github.com/borispdev/AGWKeepAlive/releases).
- Transfer zipped archive to the target PC or server on the same network with AGW.
- Unzip to a directory of your choice.
> It is recommended to choose directory with shortest path possible without whitespaces.
> E.g.: `C:\AGWKeepAlive`

### Install service
- Go to start menu and find *Windows PowerShell*, right-click on it and choose *Run as administrator*.
- After confirmation message, a terminal window should open. Navigate to the folder where unzipped files are, to the same folder where `AGWKeepAlive.exe` file is located.
	```powershell
	cd C:\My\service\installation\folder\AGWKeepAlive
	`````
- Run installation command:
	```powershell
	.\AGWKeepAlive.exe install
	```
	> If you like to set the service for automatic startup run:
	>```powershell
	>.\AGWKeepAlive.exe --startup=auto install
	>```
### Configure
- In Windows explorer navigate to `\_internal` directory.
- Find and open `config.toml` file in text editor of your choice.
- Find the following parameter:
	```toml
	ip_list = ["192.168.0.1", "192.168.0.2", "192.168.0.3", "192.168.0.4"]
	```
	Replace IP addresses in square brackets with those of real AGWs. **Each address must be in double quotes and separated from each other by a comma sign.**
- At this point the service is configured and ready to use.
- Additional configuration parameters are:
	- `interval` - Time interval in sec. between requests sent to AGWs.
	- `request_timeout` - HTTP request timeout threshold in sec.
	- `log_file` - Log file to save service messages.
	- `log_success` - Determine whether to log connection success messages.

## Usage
### Run service
In PowerShell navigate to the folder where `AGWKeepAlive.exe` is located and run as administrator:
```powershell
.\AGWKeepAlive.exe start
```
Alternatively you can start *AGW KeepAlive* service form windows service manager.
### Stop service
In PowerShell navigate to the folder where `AGWKeepAlive.exe` is located and run as administrator:
```powershell
.\AGWKeepAlive.exe stop
```
Alternatively you can stop *AGW KeepAlive* service form windows service manager.

### Test connectivity
Open `*.log` file (`agw_connection.log` by default) and inspect for errors.
>Recommended way of error tracking is to use real time log file monitoring tool e.g. [BareTail](https://www.baremetalsoft.com/baretail/)
>Open log file with BareTail while service is running to see real time progress.

### Uninstall
- Stop the service
- In PowerShell navigate to the folder where `AGWKeepAlive.exe` is located and run as administrator:
	```powershell
	.\AGWKeepAlive.exe remove
	```
- Delete installation directory and its contents.


## Project Status

Project is: _in progress_
>Beta release available for testing with AGWs.

## Contact

Created by [@borisp](mailto:boris.petrov@bd.com) - feel free to contact me!

## License
MIT License
<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->
