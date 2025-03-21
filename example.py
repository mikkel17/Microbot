
import jpype
import jpype.imports
from jpype import JProxy
import time

# Path to your JAR file
JAR_PATH = "/opt/microbot/microbot.jar"

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

time.sleep(10)
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
        
rocks = JClass("net.runelite.client.plugins.microbot.mining.enums.Rocks")

microbot.getConfigManager().setConfiguration("Mining", "Ore", rocks.GOLD)

time.sleep(10)
print("20 seconds passed")
microbot.getPluginManager().setPluginEnabled(get_plugin_by_name(plugin_name), True)
microbot.getPluginManager().startPlugins()
time.sleep(10)
print('Stopping bot')
microbot.getPluginManager().setPluginEnabled(get_plugin_by_name(plugin_name), False)
microbot.getPluginManager().stopPlugin(get_plugin_by_name(plugin_name))

#time.sleep(20)
#print('stopping mining')
#microbot.getPluginManager().stopPlugin()
microbot.getConfigManager().setConfiguration("Mining", "Ore", rocks.IRON)
time.sleep(10)
print("20 seconds passed")
microbot.getPluginManager().setPluginEnabled(get_plugin_by_name(plugin_name), True)
microbot.getPluginManager().startPlugins()
time.sleep(10)
print('Stopping bot')
microbot.getPluginManager().setPluginEnabled(get_plugin_by_name(plugin_name), False)
microbot.getPluginManager().stopPlugin(get_plugin_by_name(plugin_name))


