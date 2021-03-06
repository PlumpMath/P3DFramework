import sys
from os import system, getcwd, listdir
from direct.stdpy.file import join, isfile

if len(sys.argv) != 4:
    print("Invalid arguments!")
    print("Arguments must be: [panda-bin] [panda-libs] [panda-include]")
    sys.exit(0)

PANDA_BIN = sys.argv[1]
PANDA_LIBS = sys.argv[2]
PANDA_INCLUDE = sys.argv[3]

cwd = getcwd().replace("\\", "/").rstrip("/")

ignoreFiles = []

def checkIgnore(source):
    for f in ignoreFiles:
        if f.lower() in source.lower():
            return False
    return True

allSources = [i for i in listdir("Source") if isfile(join("Source", i)) and checkIgnore(i) and i.endswith(".h") ]

allSourcesStr = ' '.join(['"' + i + '"' for i in allSources])

print("\nRunning interrogate ..")

command = PANDA_BIN + \
    "/interrogate -D__inline -DCPPPARSER -DP3_INTERROGATE=1 -D__cplusplus "
command += "-fnames -string -refcount -assert "
command += "-Dvolatile= "
command += "-DWIN32= "
command += "-DWIN32_VC= "
command += "-D_WINDOWS= "
command += "-S" + PANDA_INCLUDE + "/parser-inc "
command += "-S" + PANDA_INCLUDE + "/ "

command += "-I" + PANDA_BIN + "/include/ "
command += "-oc Source/InterrogateModule.cxx "
command += "-od Source/InterrogateModule.in "
command += "-python-native "
command += "-module RSCoreModules "
command += "-library RSCoreModules "
command += "-srcdir \"" + join(cwd, "Source") + "\" "

command += allSourcesStr

print(command)

system(command)

print("\nRunning interrogate_module ..")
command = PANDA_BIN + "/interrogate_module "
command += "-python-native " 
command += "-module RSCoreModules " 
command += "-library RSCoreModules " 
command += "-oc Source/InterrogateWrapper.cxx " 
command += "Source/InterrogateModule.in " 
print(command)
system(command)
