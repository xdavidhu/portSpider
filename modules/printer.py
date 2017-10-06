import socket
import requests
from lxml.html import fromstring
import datetime
import sys
import ipaddress
import threading
import os

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[1;94m', '\033[1;91m', '\33[1;97m', '\33[1;93m', '\033[1;35m', '\033[1;32m', '\033[0m'

class ThreadManager(object):
    i = 0

    def __init__(self, ipList):
        self.allIps = ipList
        self.size = len(ipList)

    def getNextIp(self):
        if not (self.i >= self.size - 1):
            ip = self.allIps[self.i]
            self.i += 1
            return ip
        return 0

    def getID(self):
        return self.i + 1

def coreOptions():
    options = [["network", "IP range to scan", ""], ["port-timeout", "Timeout (in sec) for port 80.", "0.3"],
               ["title-timeout", "Timeout (in sec) for title resolve.", "3"], ["threads", "Number of threads to run.", "50"],
               ["verbose", "Show verbose output.", "true"]]
    return options


def createIPList(network):
    net4 = ipaddress.ip_network(network)
    ipList = []
    for x in net4.hosts():
        ipList.append(x)
    return ipList

def print1(data):
    if verbose:
        print("\033[K" + data)

def checkServer(address, port):
    s = socket.socket()
    s.settimeout(float(portTimeout))
    try:
        s.connect((address, port))
        s.close()
        return True
    except socket.error:
        s.close()
        return False
    except:
        s.close()
        return "FAIL"


def getHTTP(address, port):
    code = None
    title = None

    try:
        r = requests.get("http://" + address, timeout=float(titleTimeout), allow_redirects=True)
    except:
        return False

    try:
        code = r.status_code
    except:
        pass

    try:
        tree = fromstring(r.content)
        title = tree.findtext('.//title')
    except:
        pass

    return [title, code]


def writeToFile(line):
    file = open(fileName, "a")
    file.write(line)
    file.close()


def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()


def statusWidget():
    sys.stdout.write(GREEN + "[" + status + "] " + YELLOW + str(threadManager.getID()) + GREEN + " / " + YELLOW + str(
        allIPs) + GREEN + " hosts done." + END)
    restart_line()
    sys.stdout.flush()


def scan(i):
    global status
    global openPorts
    global done
    title = ""
    while True:
        if stop:
            sys.exit()
        ip = threadManager.getNextIp()
        if ip == 0:
            break
        portsOpen = []
        status = (threadManager.getID() / allIPs) * 100
        status = format(round(status, 2))
        status = str(status) + "%"
        stringIP = str(ip)

        for port in ports:
            if stop:
                sys.exit()
            if port == 80:
                if not portsOpen:
                    continue

            isUp = checkServer(stringIP, port)

            if isUp != "FAIL":
                if isUp:
                    portsOpen.append(port)
                    openPorts = openPorts + 1
                    print1(GREEN + "[+] Port " + str(port) + " is open on '" + stringIP + "'" + END)

                    if port == 80:
                        http = getHTTP(stringIP, 80)
                        if not http:
                            print1(YELLOW + "[!] Failed to get the HTTP response of '" + stringIP + "'" + END)
                            title = "NO-TITLE"
                            code = "NO-CODE"
                        else:
                            title = str(http[0])
                            code = str(http[1])
                            if code is not None:
                                print1(GREEN + "[+] Response code of '" + stringIP + "': '" + code + "'" + END)
                            else:
                                print1(YELLOW + "[!] Failed to get the response code of '" + stringIP + "'" + YELLOW)
                                code = "NO-CODE"
                            if title is not None:
                                title = title.replace("\n", "")
                                try:
                                    print1(GREEN + "[+] Title of '" + stringIP + "': '" + title + "'" + END)
                                except:
                                    print1(YELLOW + "[!] Failed to print title of '" + stringIP + "'" + END)
                                    title = "NO-TITLE"
                            else:
                                print1(YELLOW + "[!] Failed to get title of '" + stringIP + "'" + YELLOW)
                                title = "NO-TITLE"

                    logLine = stringIP + " - " + "OPEN:"
                    for port in portsOpen:
                        logLine = logLine + " " + str(port)
                    if title != "":
                        logLine = logLine + " - HTTP Title: " + title
                    logLine = logLine + "\n"
                    logLines.append(logLine)

                elif not isUp:
                    print1(RED + "[-] Port " + str(port) + " is closed on '" + stringIP + "'" + END)
            else:
                print1(RED + "[!] Failed connecting to '" + stringIP + "'" + END)
    done = done + 1


def core(moduleOptions):
    print(
        "\n" + GREEN + "PRINTER module by @xdavidhu. Scanning subnet '" + YELLOW + moduleOptions[0][2] + GREEN + "'...\n")

    global status
    global fileName
    global allIPs
    global portTimeout
    global titleTimeout
    global ips
    global threadCount
    global done
    global verbose
    global stop
    global ports
    global openPorts
    global logLines
    global threadManager
    logLines = []
    stop = False
    done = 0

    portTimeout = moduleOptions[1][2]
    titleTimeout = moduleOptions[2][2]
    network = moduleOptions[0][2]
    threadCount = int(moduleOptions[3][2])
    verbose = moduleOptions[4][2]

    if verbose == "true":
        verbose = True
    else:
        verbose = False

    try:
        ipList = createIPList(network)
        allIPs = len(ipList)
        if allIPs == 0:
            raise Exception
    except:
        print(RED + "[!] Invalid subnet. Exiting...\n")
        return

    threadManager = ThreadManager(ipList)

    i = datetime.datetime.now()
    i = str(i).replace(" ", "_")
    i = str(i).replace(":", "-")
    script_path = os.path.dirname(os.path.realpath(__file__))
    script_path = script_path.replace("modules", "")
    if not os.path.exists(script_path + "logs"):
        os.makedirs(script_path + "logs")
    fileName = script_path + "logs/log-printer-portSpider-" + i + ".log"

    file = open(fileName, 'w')
    file.write("subnet: " + network + "\n")
    file.close()

    ports = [9100, 515, 631, 80]
    openPorts = 0
    threads = []
    for i in range(threadCount):
        i -= 1
        t = threading.Thread(target=scan, args=(i,))
        t.daemon = True
        threads.append(t)
        t.start()

    try:
        while True:
            if done == threadCount and threadManager.getID() == allIPs:
                break
            statusWidget()
    except KeyboardInterrupt:
            stop = True
            verbose = False
            print("\n" + RED + "[I] Stopping..." + END)
    stop = True
    verbose = False

    for logLine in logLines:
        try:
            writeToFile(logLine)
        except:
            writeToFile("WRITING-ERROR")

    print("\n\n" + GREEN + "[I] PRINTER module done. Results saved to '" + YELLOW + fileName + GREEN + "'.\n")
