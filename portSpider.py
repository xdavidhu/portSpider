#!/usr/bin/env python3
# -.- coding: utf-8 -.-

import os
import traceback

# MODULE IMPORT
from modules import http
from modules import template
from modules import printer
from modules import gameserver
from modules import ssh

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[1;94m', '\033[1;91m', '\33[1;97m', '\33[1;93m', '\033[1;35m', '\033[1;32m', '\033[0m'

allModules = [["http", "Scan for open HTTP ports, and get the the titles."], ["ssh", "Scan for open SSH ports."],
              ["printer", "Scan for open printer ports."], ["gameserver", "Scan for open game server ports."],
              ["template", "Template module for developers."]]
textToModule = [["http", http], ["template", template], ["printer", printer], ["gameserver", gameserver], ["ssh", ssh]]

inModule = False
currentModule = ""
moduleOptions = []

def commandHandler(command):
    command = str(command)
    command = command.lower()

    global inModule
    global currentModule
    global moduleOptions
    global currentModuleFile

    # COMMANDS

    # HELP
    def helpPrint(name, desc, usage):
        print("\t" + YELLOW + name + GREEN + ": " + BLUE + desc + GREEN + " - '" + usage + "'" + END)
    if command == "help":
        print(GREEN + "\n[I] Available commands:\n" + END)
        helpPrint("MODULES", "List all modules", "modules")
        helpPrint("USE", "Use a module", "use module_name")
        helpPrint("OPTIONS", "Show a module's options", "options")
        helpPrint("SET", "Set an option", "set option_name option_value")
        helpPrint("RUN", "Run the selected module", "run")
        helpPrint("BACK", "Go back to menu", "back")
        helpPrint("EXIT", "Shut down portSpider", "exit")
        print()

    # USE
    elif command.startswith("use "):
        if not inModule:
            tempModule = command.replace("use ", "")
            inModule = False
            for module in allModules:
                if module[0] == tempModule:
                    inModule = True
            if inModule:
                inModule = True
                currentModule = tempModule
                for text in textToModule:
                    if text[0] == currentModule:
                        currentModuleFile = text[1]
                getCoreOptions = getattr(currentModuleFile, "coreOptions", None)
                moduleOptions = getCoreOptions()
            else:
                print(RED + "[!] Module '" + YELLOW + tempModule + RED + "' not found." + END)
        else:
            print(RED + "[!] Module '" + YELLOW + currentModule + RED + "' already selected." + END)
    elif command == "use":
        print(RED + "[!] Usage: 'use " + YELLOW + "module_name" + RED + "'" + END)

    # OPTIONS
    elif command == "options":
        if inModule:
            print(GREEN + "\n Options for module '" + YELLOW + currentModule + GREEN + "':" + END)
            for option in moduleOptions:
                if option[2] == "":
                    print("\t" + YELLOW + option[0] + GREEN + " - " + BLUE + option[1] + GREEN + " ==> " + RED + "[NOT SET]" + END)
                else:
                    print("\t" + YELLOW + option[0] + GREEN + " - " + BLUE + option[1] + GREEN + " ==> '" + YELLOW +
                          option[2] + GREEN + "'" + END)
            print()
        else:
            print(RED + "[!] No module selected." + END)

    # SET
    elif command.startswith("set "):
        if inModule:
            command = command.replace("set ", "")
            command = command.split()
            error = False
            try:
                test = command[0]
                test = command[1]
            except:
                print(RED + "[!] Usage: 'set " + YELLOW + "option_name option_value" + RED + "'" + END)
                error = True
            if not error:
                inOptions = False
                for option in moduleOptions:
                    if option[0] == command[0]:
                        inOptions = True
                        option[2] = command[1]
                        print(YELLOW + option[0] + GREEN + " ==> '" + YELLOW + command[1] + GREEN + "'" + END)
                if not inOptions:
                    print(RED + "[!] Option '" + YELLOW + command[0] + RED + "' not found." + END)
        else:
            print(RED + "[!] No module selected." + END)
    elif command == "set":
        print(RED + "[!] Usage: 'set " + YELLOW + "option_name option_value" + RED + "'" + END)

    # RUN
    elif command == "run":
        if inModule:
            fail = False
            for option in moduleOptions:
                if option[2] == "":
                    fail = True
            if not fail:
                print(GREEN + "[I] Starting module '" + YELLOW + currentModule + GREEN + "'..." + END)
                coreModule = getattr(currentModuleFile, "core")
                try:
                    coreModule(moduleOptions)
                except KeyboardInterrupt:
                    print(GREEN + "[I] Stopping module..." + END)
                except Exception as e:
                    print(RED + "\n[!] Module crashed." + END)
                    print(RED + "[!] Debug info:\n'")
                    print(traceback.format_exc())
                    print("\n" + END)
            else:
                print(RED + "[!] Not all options set." + END)
        else:
            print(RED + "[!] No module selected." + END)
    # BACK
    elif command == "back":
        if inModule:
            inModule = False
            currentModule = ""
            moduleOptions = []

    # EXIT
    elif command == "exit":
        print(GREEN + "[I] Shutting down..." + END)
        raise SystemExit

    # MODULES
    elif command == "modules":
        print(GREEN + "\nAvailable modules:" + END)
        for module in allModules:
            print(YELLOW + "\t" + module[0] + GREEN + " - " + BLUE + module[1] + END)
        print()

    # CLEAR
    elif command == "clear":
        os.system("clear||cls")

    # DEBUG
    elif command == "debug":
        print("inModule: " + str(inModule))
        print(currentModule)
        print(moduleOptions)

    elif command == "":
        pass

    else:
        print(RED + "[!] Unknown command: '" + YELLOW + command + RED + "'. Type '" + YELLOW + "help" + RED + "' for all available commands." + END)

header = """
██████╗  ██████╗ ██████╗ ████████╗███████╗██████╗ ██╗██████╗ ███████╗██████╗
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
██████╔╝██║   ██║██████╔╝   ██║   ███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝
██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗
██║     ╚██████╔╝██║  ██║   ██║   ███████║██║     ██║██████╔╝███████╗██║  ██║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                             v0.1 by David Schütz (@xdavidhu)
"""
print(GREEN + header + END)

moduleList = ""
for module in allModules:
    moduleList = moduleList + YELLOW + module[0] + GREEN + ", "
moduleList = moduleList[:-2]
print(GREEN + "Loaded modules: " + moduleList + "\n")

while True:
    if inModule:
        inputHeader = BLUE + "portSpider" + RED + "/" + currentModule + BLUE + " $> " + END
    else:
        inputHeader = BLUE + "portSpider $> " + END

    try:
        commandHandler(input(inputHeader))
    except KeyboardInterrupt:
        print(GREEN + "\n[I] Shutting down..." + END)
        raise SystemExit
    except Exception as e:
        print(RED + "\n[!] portSpider crashed...\n[!] Debug info: \n")
        print(traceback.format_exc())
        print("\n" + END)
        exit()