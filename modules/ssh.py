import socket
import datetime
import sys
import ipaddress
import threading

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[1;94m', '\033[1;91m', '\33[1;97m', '\33[1;93m', '\033[1;35m', '\033[1;32m', '\033[0m'

def coreOptions():
    options = [["network", "IP range to scan", ""], ["port-timeout", "Timeout (in sec) for port 80.", "0.3"],
               ["threads", "Number of threads to run.", "50"], ["verbose", "Show verbose output.", "true"]]
    return options


def createIPList(network):
    net4 = ipaddress.ip_network(network)
    ipList = []
    for x in net4.hosts():
        ipList.append(x)
    return ipList

def print1(data):
    if verbose:
        print(data)

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

def writeToFile(line):
    file = open(fileName, "a")
    file.write(line)
    file.close()


def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()


def statusWidget():
    sys.stdout.write(GREEN + "[" + status + "] " + YELLOW + str(ipID) + GREEN + " / " + YELLOW + str(
        allIPs) + GREEN + " hosts done." + END)
    restart_line()
    sys.stdout.flush()


def scan(i):
    global ipID
    global status
    global openPorts
    global done
    for ip in ips[i]:

        ipID = ipID + 1
        status = (ipID / allIPs) * 100
        status = format(round(status, 2))
        status = str(status) + "%"
        stringIP = str(ip)
        if stop:
            sys.exit()

        if (str(ip) == "0"):
            continue
        isUp = checkServer(stringIP, port)
        if isUp:
            openPorts = openPorts + 1
            print1(GREEN + "[+] Port " + str(port) +  " is open on '" + stringIP + "'" + END)
            logLine = stringIP + "\n"
            logLines.append(logLine)
        elif not isUp:
            print1(RED + "[-] Port " + str(port) + " is closed on '" + stringIP + "'" + END)
        else:
            print1(RED + "[!] Connecting failed to '" + stringIP + "'" + END)
    done = done + 1


def core(moduleOptions):
    print(
        "\n" + GREEN + "SSH module by @xdavidhu. Scanning subnet '" + YELLOW + moduleOptions[0][2] + GREEN + "'...\n")

    global status
    global ipID
    global fileName
    global allIPs
    global portTimeout
    global ips
    global threadCount
    global done
    global verbose
    global stop
    global port
    global ipID
    global openPorts
    global logLines
    logLines = []
    stop = False
    done = 0

    portTimeout = moduleOptions[1][2]
    network = moduleOptions[0][2]
    threadCount = int(moduleOptions[2][2])
    verbose = moduleOptions[3][2]

    if verbose == "true":
        verbose = True
    else:
        verbose = False

    try:
        ipList = createIPList(network)
    except:
        print(RED + "[!] Invaild subnet. Exiting...\n")
        return
    allIPs = len(ipList)

    h = threadCount
    w = int(allIPs / threadCount)
    if (w < allIPs / threadCount):
        w = w + 1
    ips = [[0 for x in range(w)] for y in range(h)]
    i = 0
    i2 = [0 for x in range(h)]


    for ip in ipList:
        if (i + 1 > threadCount):
            i = 0
        ips[i][i2[i]] = ip
        i2[i] = i2[i] + 1;
        i = i + 1
    i = datetime.datetime.now()
    i = str(i).replace(" ", "_")
    i = str(i).replace(":", "-")
    fileName = "log-ssh-portSpider-" + i + ".log"

    file = open(fileName, 'w')
    file.write("subnet: " + network + "\n")
    file.close()

    port = 22

    ipID = 0
    openPorts = 0
    threads = []
    for i in range(threadCount):
        i -= 1
        t = threading.Thread(target=scan, args=(i,))
        t.daemon = True
        threads.append(t)
        t.start()

    try:
        while done != threadCount:
                pass
                statusWidget()
    except KeyboardInterrupt:
            stop = True
            verbose = False
            print("\n" + RED + "[I] Stopping..." + END)

    for logLine in logLines:
        try:
            writeToFile(logLine)
        except:
            writeToFile("WRITING-ERROR")

    print("\n\n" + GREEN + "[I] SSH module done. Results saved to '" + YELLOW + fileName + GREEN + "'.\n")
