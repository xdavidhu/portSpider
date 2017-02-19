def coreOptions():
    options = [["testvar1", "testvar1 description", ""], ["testvar2", "testvar2 description", "testvar2 pre-set value"], ["var3", "var3 description", ""]]
    return options

def core(moduleOptions):

    testvar1value = moduleOptions[0][2]
    testvar2value = moduleOptions[1][2]
    var3value = moduleOptions[2][2]

    print("Hello world!")

    print("testvar1: " + str(testvar1value))
    print("testvar2: " + str(testvar2value))
    print("var3: " + str(var3value))