import socket
import requests
from lxml.html import fromstring
import datetime
import sys
import ipaddress

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[1;94m', '\033[1;91m', '\33[1;97m', '\33[1;93m', '\033[1;35m', '\033[1;32m', '\033[0m'

def coreOptions():
    options = [["network", "IP range to scan", ""], ["port-timeout", "Timeout (in sec) for port 80.", "0.3"], ["title-timeout", "Timeout (in sec) for title resolve.", "3"]]
    return options

def createIPList(network):
    net4 = ipaddress.ip_network(network)
    ipList = []
    for x in net4.hosts():
        ipList.append(x)
    return ipList

def checkServer(address, port):
    s = socket.socket()
    s.settimeout(float(portTimeout))
    try:
        s.connect((address, port))
        s.close()
        return True
    except KeyboardInterrupt:
        s.close()
        return "STOP"
    except socket.error:
        s.close()
        return False
    except:
        s.close()
        return "FAIL"

def getTitle(address, port):
    try:
        r = requests.get("http://" + address, timeout=float(titleTimeout))
        tree = fromstring(r.content)
        return tree.findtext('.//title')
    except KeyboardInterrupt:
        return "/=PORTSPIDER-STOP=/"
    except:
        return False

def writeToFile(line):
    file = open(fileName, "a")
    file.write(line)
    file.close()

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

def statusWidget():
    sys.stdout.write(GREEN + "[" + status + "] " + YELLOW + str(ipID) + GREEN + " / " + YELLOW + str(allIPs) + GREEN + " hosts done." + END)
    restart_line()
    sys.stdout.flush()

def core(moduleOptions):

    print("\n" + GREEN + "HTTP module by @xdavidhu. Scanning subnet '" + YELLOW + moduleOptions[0][2] + GREEN + "'...\n")

    global status
    global ipID
    global fileName
    global allIPs
    global portTimeout
    global titleTimeout

    portTimeout = moduleOptions[1][2]
    titleTimeout = moduleOptions[2][2]
    network = moduleOptions[0][2]
    try:
        ipList = createIPList(network)
    except:
        print(RED + "[!] Invaild subnet. Exiting...\n")
        return
    allIPs = len(ipList)

    i = datetime.datetime.now()
    i = str(i).replace(" ", "_")
    fileName = "log-http-portSpider-" + i + ".log"

    file = open(fileName,'w')
    file.write("subnet: " + network + "\n")
    file.close()

    port = 80
    ipID = 0
    openPorts = 0
    for ip in ipList:
        ipID = ipID + 1
        status = (ipID / allIPs) * 100
        status = format(round(status,2))
        status = str(status) + "%"
        stringIP = str(ip)

        statusWidget()

        isUp = checkServer(stringIP, port)
        if isUp == "STOP":
            print("\n\n" + GREEN + "[I] HTTP module stopped. Results saved to '" + YELLOW + fileName + GREEN + "'.\n")
            return
        if isUp:
            openPorts = openPorts + 1
            print(GREEN + "[+] Port 80 is open on '" + stringIP + "'" + END)
            statusWidget()
            title = getTitle(stringIP, 80)
            if not title:
                print( YELLOW + "[!] Failed to get the title of '" + stringIP + "'" + END)
                statusWidget()
                title = "NONE"
            else:
                if title is not None:
                    if title == "/=PORTSPIDER-STOP=/":
                        print("\n\n" + GREEN + "[I] PRINTER module stopped. Results saved to '" + YELLOW + fileName + GREEN + "'. (title)\n")
                        return
                    title = title.replace("\n", "")
                    try:
                        print(GREEN + "[+] Title of '" + stringIP  +"': '" + title + "'" + END)
                        statusWidget()
                    except:
                        print(YELLOW + "[!] Failed to print title of '" + stringIP + "'" + END)
                        statusWidget()
                        title = "NONE"
                else:
                    print(YELLOW + "[!] Failed to get title of '" + stringIP + "'" + YELLOW)
                    statusWidget()
                    title = "NONE"
            logLine = stringIP + " - " + "80 OPEN" + " - " + title + "\n"
            writeToFile(logLine)
        elif not isUp:
            print(RED + "[-] Port 80 is closed on '" + stringIP + "'" + END)
        else:
            print(RED + "[!] Connecting failed to '" + stringIP + "'" + END)

    print("\n" + GREEN + "[I] HTTP module done. Results saved to '" + YELLOW + fileName + GREEN + "'.\n")
