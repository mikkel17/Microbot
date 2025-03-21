
import jpype
import jpype.imports
from jpype import JProxy, JClass, java
import time
import socket

class arm():
     
    def __init__(self):
        # Path to your JAR file
        JAR_PATH = "/opt/microbot/microbot.jar"
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

    def main(self, location, plugin_name):
        self.go_to_job_site(location['x'], location['y'], location['plane'])
        self.start_plugin(plugin_name)

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get the local machine name
    host = 'localhost'
    port = 12333  # The same port as used by the server

    # Connect to the server
    client_socket.connect((host, port))

    # Send data to the server
    message = "Hello, Server!"
    client_socket.send(message.encode('utf-8'))

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client()
'''    loc = {
        'x': 2981,
        'y': 3234,
        'plane': 0
    }
    plugin = "Auto Mining"
    arm = arm()
    arm.main(loc, plugin)'''