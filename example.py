
import jpype
import jpype.imports
from jpype import JProxy
import time

# Path to your JAR file
JAR_PATH = "/opt/microbot.jar"

jvm_options = [
    "--debug"
]



import jpype
from jpype import JClass, java
import time
# Start the JVM

#jpype.startJVM(jpype.getDefaultJVMPath(), "--debug", f"-Djava.class.path={JAR_PATH}")
jpype.startJVM(classpath=[JAR_PATH])


# Load the Java class containing the main method
MainClass = JClass("net.runelite.client.RuneLite")

# Call the main method to start the GUI
MainClass.main([])

'''
time.sleep(30)
print("30 seconds went by")
print("3 seconds left")
time.sleep(3)
'''
import jpype
from jpype import JClass, java

# Start the JVM
#jpype.startJVM(classpath=["path/to/your/file.jar"])

print("starting timer")
time.sleep(35)
print("start walking")
walker = JClass("net.runelite.client.plugins.microbot.util.walker.Rs2Walker")
walker.walkTo(2981, 3234, 0)


PluginDescriptor = JClass("net.runelite.client.plugins.PluginDescriptor")

plugin_name = "Auto Mining"
microbot = JClass("net.runelite.client.plugins.microbot.Microbot")

def get_plugin_by_name(plugin_name):
    for plugin in microbot.getPluginManager().getPlugins():
        descriptor = plugin.getClass().getAnnotation(PluginDescriptor)
        if descriptor is not None and descriptor.name().contains(plugin_name):
                print(f"plugin enabled: {descriptor.name()}")
                return plugin

time.sleep(20)
print("20 seconds passed")
microbot.getPluginManager().setPluginEnabled(get_plugin_by_name(plugin_name), True)
microbot.getPluginManager().startPlugins()

#time.sleep(20)
#print('stopping mining')
#microbot.getPluginManager().stopPlugin()


'''
import jpype
from jpype import JClass, java

# Start the JVM
#jpype.startJVM(classpath=["path/to/your/file.jar"])

# Load the ConfigManager class
ConfigManager = JClass("net.runelite.client.config.ConfigManager")

# Create an instance of ConfigManager using the constructor
configManager = ConfigManager()

# Now you can use the configManager instance to set configurations
configManager.setConfiguration("runelite.autominingplugin", True)

# Similarly, load and use PluginManager
PluginManager = JClass("net.runelite.client.plugins.PluginManager")
pluginManager = PluginManager()

# Start the plugin using PluginManager
pluginManager.startPlugin("AutoMiningPlugin")
'''
'''
from jpype import JClass, java
# Start the JVM


# Load necessary classes
AutoMiningPlugin = JClass("net.runelite.client.plugins.microbot.mining.AutoMiningPlugin")
AutoMiningScript = JClass("net.runelite.client.plugins.microbot.mining.AutoMiningScript")
ConfigManager = JClass("net.runelite.client.config.ConfigManager")
OverlayManager = JClass("net.runelite.client.ui.overlay.OverlayManager")

# Create instances of the required dependencies
autoMiningScript = AutoMiningScript()
configManager = ConfigManager.getInstance()  # Assuming it's a singleton
overlayManager = OverlayManager()

# Create an instance of the plugin
plugin_instance = AutoMiningPlugin()

# Manually set the dependencies
plugin_instance.autoMiningScript = autoMiningScript
plugin_instance.configManager = configManager
plugin_instance.overlayManager = overlayManager

# Use reflection to access the protected startUp method
Method = JClass("java.lang.reflect.Method")
startUpMethod = plugin_instance.getClass().getDeclaredMethod("startUp", [])
startUpMethod.setAccessible(True)

# Call the startUp method
startUpMethod.invoke(plugin_instance)
'''