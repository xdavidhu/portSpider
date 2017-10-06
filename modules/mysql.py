import pymysql
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

def checkSQL(host, port):
    loginFail = False
    try:
        con = pymysql.connect(host=host, connect_timeout=sqlTimeout)
    except:
        loginFail = True

    if loginFail:
        try:
            con = pymysql.connect(host=host, user='root', passwd='', connect_timeout=sqlTimeout)
        except:
            return ["login-error"]

    try:
        cursor = con.cursor()
        cursor.execute("SHOW DATABASES")
        dbs = cursor.fetchall()
    except:
        dbs = ["-"]

    try:
        cursor = con.cursor()
        cursor.execute("SELECT VERSION()")
        serverVersion = str(cursor.fetchone())
    except:
        serverVersion = "-"

    return ["success", serverVersion, dbs]


def coreOptions():
    options = [["network", "IP range to scan", ""], ["port", "Port to scan.", "3306"],
               ["port-timeout", "Timeout (in sec) for port 80.", "0.3"],
               ["sql-timeout", "Timeout (in sec) for the database connection.", "3"],
               ["threads", "Number of threads to run.", "50"],
               ["checkauth", "Connect to the server and perform tests.", "true"],
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
        status = (threadManager.getID() / allIPs) * 100
        status = format(round(status, 2))
        status = str(status) + "%"
        stringIP = str(ip)
        isUp = checkServer(stringIP, port)

        if isUp != "FAIL":
            if isUp:
                openPorts = openPorts + 1
                print1(GREEN + "[+] Port " + str(port) + " is open on '" + stringIP + "'" + END)

                if checkauth:
                    mysqlStatusReason = "UNKNOWN ERROR"
                    mysql = checkSQL(stringIP, port)
                    if mysql[0] == "login-error":
                        mysqlStatus = False
                        mysqlStatusReason = "CONNECTION ERROR"
                        print1(
                            RED + "[!] Failed connecting to the database on '" + stringIP + "'. ERROR: " + mysqlStatusReason + END)
                    elif mysql[0] == "permission-error":
                        mysqlStatus = False
                        mysqlStatusReason = "PERMISSION ERROR"
                        print1(
                            RED + "[!] Failed connecting to the database on '" + stringIP + "'. ERROR: " + mysqlStatusReason + END)
                    elif mysql[0] == "success":
                        mysqlStatus = True
                        version = mysql[1]
                        dbs = mysql[2]

                        dbsList = ""
                        for db in dbs:
                            dbsList = dbsList + str(db) + ", "
                        if dbsList != "":
                            dbsList = dbsList[:-2]
                        else:
                            dbsList = "-"

                        print1(GREEN + "[+] Open database found:\n\tIP: " + stringIP + "\n\t" + "MySQL version: " + str(
                            version) + "\n\tDB's: " + dbsList + "\n")

                    else:
                        print1(
                            RED + "[!] Failed connecting to the database on '" + stringIP + "'. ERROR: " + mysqlStatusReason + END)
                        mysqlStatus = False

                    if mysqlStatus:
                        logLine = stringIP + " - " + str(
                            port) + " OPEN" + " - " + "OPEN DATABASE - Version: " + version + " - " + " DB's: " + dbsList + "\n"
                    else:
                        logLine = stringIP + " - " + str(
                            port) + " OPEN" + " - DB SCAN ERROR: " + mysqlStatusReason + "\n"
                    logLines.append(logLine)
                else:
                    logLine = stringIP + " - " + str(port) + " OPEN\n"
                    logLines.append(logLine)
            elif not isUp:
                print1(RED + "[-] Port " + str(port) + " is closed on '" + stringIP + "'" + END)
        else:
            print1(RED + "[!] Failed connecting to '" + stringIP + "'" + END)
    done = done + 1


def core(moduleOptions):
    print(
        "\n" + GREEN + "MYSQL module by @xdavidhu. Scanning subnet '" + YELLOW + moduleOptions[0][2] + GREEN + "'...\n")

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
    global port
    global openPorts
    global logLines
    global checkauth
    global sqlTimeout
    global threadManager
    logLines = []
    stop = False
    done = 0

    try:
        port = int(moduleOptions[1][2])
    except:
        print(RED + "[!] Invalid port. Exiting...\n")
        return
    portTimeout = moduleOptions[2][2]
    network = moduleOptions[0][2]
    sqlTimeout = moduleOptions[3][2]
    threadCount = int(moduleOptions[4][2])
    checkauth = moduleOptions[5][2]
    verbose = moduleOptions[6][2]

    try:
        sqlTimeout = int(sqlTimeout)
    except:
        print(RED + "[!] Invalid sql-timeout. Exiting...\n")
        return

    if verbose == "true":
        verbose = True
    else:
        verbose = False

    if checkauth == "true":
        checkauth = True
    else:
        checkauth = False

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
    fileName = script_path + "logs/log-mysql-portSpider-" + i + ".log"

    file = open(fileName, 'w')
    file.write("subnet: " + network + "\n")
    file.close()

    openPorts = 0
    threads = []
    for i in range(threadCount):
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
    print("\n\n" + GREEN + "[I] MYSQL module done. Results saved to '" + YELLOW + fileName + GREEN + "'.\n")
