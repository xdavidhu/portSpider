
    ██████╗  ██████╗ ██████╗ ████████╗███████╗██████╗ ██╗██████╗ ███████╗██████╗
    ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
    ██████╔╝██║   ██║██████╔╝   ██║   ███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝
    ██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗
    ██║     ╚██████╔╝██║  ██║   ██║   ███████║██║     ██║██████╔╝███████╗██║  ██║
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                 v1.0 by David Schütz (@xdavidhu)
[![Build Status](https://travis-ci.org/xdavidhu/portSpider.svg?branch=master)](https://travis-ci.org/xdavidhu/portSpider)
[![Compatibility](https://img.shields.io/badge/python-3.3%2C%203.4%2C%203.5%2C%203.6-brightgreen.svg)](https://github.com/xdavidhu/portSpider)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/xdavidhu/portSpider/blob/master/LICENSE)
[![Stars](https://img.shields.io/github/stars/xdavidhu/portSpider.svg)](https://github.com/xdavidhu/portSpider)

### ⚠️ Warning! This project is no longer maintained and may not work as excepted.

<h3>A lightning fast multithreaded network scanner framework with modules.</h3>
<h4>portSpider is a tool for scanning huge network ranges to find open ports and vulnerable services. This tool is not intended to scan one target, rather a whole IP range. (eg. 192.168.0.0/24) Most of the time companies/organizations have public information about their owned public IP ranges, so portSpider will help you to scan all of their machines at once for vulnerable devices/services.</h4>

# modules:
  * **http** - Scan for open HTTP ports, and get the titles.<br>
  * **mysql** - Scan for open MySQL servers, and try to log in with the default credentials.<br>
  * **mongodb** - Scan for open MongoDB instances, and check if they are password protected.<br>
  * **ssh** - Scan for open SSH ports.<br>
  * **printer** - Scan for open printer ports and websites.<br>
  * **gameserver** - Scan for open game server ports.<br>
  * **manual** - Scan custom ports.<br>

# commands:
  * **modules** - List all modules.<br>
  * **use** - Use a module.<br>
  * **options** - Show a module's options.<br>
  * **set** - Set an option.<br>
  * **run** - Run the selected module.<br>
  * **back** - Go back to menu.<br>
  * **exit** - Shut down portSpider.<br>

# installing:

  <h3>Debian based systems:</h3>

```
$ sudo apt-get update && sudo apt-get install python3 python3-pip -y

$ git clone https://github.com/xdavidhu/portSpider

$ cd portSpider/

$ python3 -m pip install -r requirements.txt
```

  <h3>macOS / OSX:</h3>

```
$ brew install python3

$ git clone https://github.com/xdavidhu/portSpider

$ cd portSpider/

$ python3 -m pip install -r requirements.txt
```
**NOTE**: You need to have [Homebrew](http://brew.sh/) installed before running the macOS/OSX installation.<br>
**WARNING**: portSpider is only compatible with Python 3.3 & 3.4 & 3.5 & 3.6

# usage:

  <h3>Start portSpider with Python3:</h3>

```
python3 portSpider.py
```

  <h3>Select a module: (eg. 'mysql')</h3>

```
portSpider $> use mysql
```

  <h3>View the module's options:</h3>

```
portSpider/mysql $> options
```

  <h3>Set all '[NOT SET]' options: (eg. option 'network' to '192.168.0.0/24')</h3>

```
portSpider/mysql $> set network 192.168.0.0/24
```

  <h4>(You can also modify already set options, but that is not required.)</h4>

  <h3>If you have every option set, run the scan:</h3>

```
portSpider/mysql $> run
```

  <h4>You will see the results on the screen as well as in a text file in the 'logs/' folder.</h4>


# developers:
  * David Schütz ([@xdavidhu](https://twitter.com/xdavidhu))
  * László Simonffy ([@Letsgo00HUN](https://twitter.com/Letsgo00HUN)) - Multithreading

# contribution:
  <h4>If you have any ideas about new modules and improvements in portSpider, feel free to contribute.</h4>
  
  * Check out the `template` module to get a better understanding of the framework.<br>
  * Make sure to include a description about your module in the pull request.<br>
  * If you create a module, you will be mentioned here in the readme with a link to your social media.

# disclaimer:
  I'm not responsible for anything you do with this program, so please only use it for good and educational purposes.

# legal:
  Copyright (c) 2017 by David Schütz. Some rights reserved.

  portSpider is under the terms of the [MIT License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the [license file](https://github.com/xdavidhu/portSpider/blob/master/LICENSE). You can also go ahead and email me at xdavid{at}protonmail{dot}com.
