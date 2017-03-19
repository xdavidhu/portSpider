
    ██████╗  ██████╗ ██████╗ ████████╗███████╗██████╗ ██╗██████╗ ███████╗██████╗
    ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
    ██████╔╝██║   ██║██████╔╝   ██║   ███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝
    ██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗
    ██║     ╚██████╔╝██║  ██║   ██║   ███████║██║     ██║██████╔╝███████╗██║  ██║
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                 v1.0 by David Schütz (@xdavidhu)
  
<h3>A lightning fast multithreaded network scanner framework with modules.</h3>

# modules:
  * **http** - Scan for open HTTP ports, and get the the titles.<br>
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
**NOTE**: You need to have [Homebrew](http://brew.sh/) installed before running the macOS/OSX installation.

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
