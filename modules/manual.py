import socket
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
    options = [["network", "IP range to scan", ""], ["ports", "Comma separated list of ports to scan. (e.g: '21,22,53')", ""],
               ["port-timeout", "Timeout (in sec) for port 80.", "0.3"], ["threads", "Number of threads to run.", "50"],
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
    while True:
        if stop:
            sys.exit()
        ip = threadManager.getNextIp()
        if ip == 0:
            break
        logLine = ""
        status = (threadManager.getID() / allIPs) * 100
        status = format(round(status, 2))
        status = str(status) + "%"
        stringIP = str(ip)
        for port in ports:
            if stop:
                sys.exit()
            isUp = checkServer(stringIP, port)
            if isUp != "FAIL":
                if isUp:
                    openPorts = openPorts + 1
                    print1(GREEN + "[+] Port " + str(port) + " is open on '" + stringIP + "'" + END)
                    logLine = logLine + " " + str(port)
                elif not isUp:
                    print1(RED + "[-] Port " + str(port) + " is closed on '" + stringIP + "'" + END)
            else:
                print1(RED + "[!] Failed connecting to '" + stringIP + "'" + END)

        if logLine != "":
            logLine = str(ip) + " - OPEN:" + logLine + "\n"
            logLines.append(logLine)

    done = done + 1


def core(moduleOptions):
    print(
        "\n" + GREEN + "MANUAL module by @xdavidhu. Scanning subnet '" + YELLOW + moduleOptions[0][2] + GREEN + "'...\n")

    global status
    global fileName
    global allIPs
    global portTimeout
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

    portInput = moduleOptions[1][2]
    portTimeout = moduleOptions[2][2]
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
    fileName = script_path + "logs/log-manual-portSpider-" + i + ".log"

    file = open(fileName, 'w')
    file.write("subnet: " + network + "\n")
    file.close()

    ports = []

    portInput = portInput.replace(" ", "")
    portInput = portInput.split(",")

    strPortList = ""
    try:
        for port in portInput:
            if not port.isdigit():
                raise Exception
            ports.append(int(port))
            strPortList = strPortList + " " + YELLOW + str(port) + GREEN + ","
    except:
        print(RED + "[!] Invalid list of ports! Exiting...\n" + END)
        return
    strPortList = strPortList[:-1]

    print(GREEN + "[I] PORTS => " + strPortList + END + "\n")

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

    print("\n\n" + GREEN + "[I] MANUAL module done. Results saved to '" + YELLOW + fileName + GREEN + "'.\n")
