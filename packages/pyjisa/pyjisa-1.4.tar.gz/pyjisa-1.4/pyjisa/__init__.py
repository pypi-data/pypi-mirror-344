# Import JPype
import os
import jpype
import jpype.imports
import atexit
from jpype import JProxy

# Where are we?
path = os.path.dirname(os.path.realpath(__file__))

def load(jvmPath=None):
    
    import site

    if jpype.isJVMStarted():
        return

    javaPath = findJava(jvmPath)

    # If no java installation has been found, install our own JRE
    if (javaPath is None) or (not os.path.exists(javaPath)):
        javaPath = installJVM()
        
    # Start the JVM
    jpype.startJVM(jvmpath=javaPath, convertStrings=True)

    # Make sure to shut everything down when Python exits
    atexit.register(shutdown)
    
    if (not os.path.exists(os.path.join(site.getusersitepackages(), "jisa-stubs"))):
        updateStubs()


def findJava(jvmPath = None):
    
    # If nothing was specified, and a local JRE is present, then use it
    if (jvmPath is None) and (os.path.exists(os.path.join(path, "JVM"))):
        jvmPath = os.path.join(path, "JVM")

    fullPath = None
    
    # If we still don't have a path, then get jpype to search for one
    if jvmPath is None:
        
        try:
            fullPath = jpype.getDefaultJVMPath()
        except:
            pass
        
        
    else:
        
        linux = os.path.join(jvmPath, "lib", "server", "libjvm.so")
        win   = os.path.join(jvmPath, "bin", "server", "jvm.dll")
        mac   = os.path.join(jvmPath, "lib", "server", "libjvm.dylib")

        if os.path.exists(linux):
            fullPath = linux 
        elif os.path.exists(win):
            fullPath = win
        elif os.path.exists(mac):
            fullPath = mac
            
            
    return fullPath


def shutdown():
    
    if jpype.isJVMStarted():
        
        try:
            from jisa.gui import GUI
            GUI.stopGUI()
        except:
            pass
        
        try:
            jpype.shutdownJVM()
        except:
            pass


def updateStubs():

    import jisa
    import site
    import stubgenj
    
    print("Updating python stubs...", end=" ", flush=True)
    stubgenj.generateJavaStubs([jisa], True, site.getusersitepackages())
    print("Done.")


def updateJISA(branch="devices_revamp"):

    import urllib.request
    import site
    from shutil import rmtree

    print("Downloading latest JISA.jar library...", end=" ", flush=True)

    urllib.request.urlretrieve("https://github.com/OE-FET/JISA/raw/%s/JISA.jar" % branch, os.path.join(path, "JISA.jar"))

    print("Done.")
    rmtree(os.path.join(site.getusersitepackages(), "jisa-stubs"), ignore_errors=True)
    

def installJVM() -> str:
    
    from distutils.dir_util import copy_tree
    from shutil import rmtree
    
    import jdk
    
    print("No Java Runtime Environment found on system, downloading JRE 11...", end=" ", flush=True)
    
    installed = jdk.install(version="11", jre=True, path=path)
    
    copy_tree(installed, os.path.join(path, "JVM"))
    rmtree(installed, ignore_errors=True)
    
    print("Done.")
    
    return findJava(os.path.join(path, "JVM"))


# If no JISA.jar file is present, download the latest
if not os.path.exists(os.path.join(path, "JISA.jar")):
    updateJISA()


# Link in JISA.jar classes
jpype.addClassPath(os.path.join(path, "JISA.jar"))
jpype.imports.registerDomain("jisa")
