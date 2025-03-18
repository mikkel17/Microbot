
import jpype
import jpype.imports
from jpype import JProxy, JClass, java
import time

class arm():
     
    def __init__(self):
        # Path to your JAR file
        JAR_PATH = "/opt/microbot.jar"
        jpype.startJVM(classpath=[JAR_PATH])

        # Load the Java class containing the main method
        MainClass = JClass("net.runelite.client.RuneLite")

        # Call the main method to start the GUI
        MainClass.main([])
        self.microbot = JClass("net.runelite.client.plugins.microbot.Microbot")
        self.walker = JClass("net.runelite.client.plugins.microbot.util.walker.Rs2Walker")

    def go_to_job_site(self, x, y, plane):
        print("starting timer")
        time.sleep(35)
        print("start walking")
        
        self.walker.walkTo(x, y, plane)
        

    def get_plugin_by_name(self, plugin_name):
        PluginDescriptor = JClass("net.runelite.client.plugins.PluginDescriptor")
        for plugin in self.microbot.getPluginManager().getPlugins():
            descriptor = plugin.getClass().getAnnotation(PluginDescriptor)
            if descriptor is not None and descriptor.name().contains(plugin_name):
                    print(f"plugin enabled: {descriptor.name()}")
                    return plugin

    def start_plugin(self, plugin_name):
        time.sleep(20)
        print("20 seconds passed")
        self.microbot.getPluginManager().setPluginEnabled(self.get_plugin_by_name(plugin_name), True)
        self.microbot.getPluginManager().startPlugins()

    def main(self):
        self.go_to_job_site(2981,3234,0)
        plugin_name = "Auto Mining"
        self.start_plugin(plugin_name)

    

if __name__ == "__main__":
    arm = arm()
    arm.main()