import socket
import requests
from lxml.html import fromstring
import datetime
import sys
import ipaddress
import threading

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[1;94m', '\033[1;91m', '\33[1;97m', '\33[1;93m', '\033[1;35m', '\033[1;32m', '\033[0m'

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
        print(data)

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
    sys.stdout.write(GREEN + "[" + status + "] " + YELLOW + str(ipID) + GREEN + " / " + YELLOW + str(
        allIPs) + GREEN + " hosts done." + END)
    restart_line()
    sys.stdout.flush()


def scan(i):
    global ipID
    global status
    global openPorts
    global done
    title = ""
    for ip in ips[i]:
        if (str(ip) == "0"):
            continue
        portsOpen = []
        ipID = ipID + 1
        status = (ipID / allIPs) * 100
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
    global ipID
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
    global ipID
    global openPorts
    global logLines
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
    fileName = "log-printer-portSpider-" + i + ".log"

    file = open(fileName, 'w')
    file.write("subnet: " + network + "\n")
    file.close()

    ports = [9100, 515, 631, 80]
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

    print("\n\n" + GREEN + "[I] PRINTER module done. Results saved to '" + YELLOW + fileName + GREEN + "'.\n")
