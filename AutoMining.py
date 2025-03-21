
import jpype
from jpype import JClass
import jpype.imports
import time

def get_plugin_by_name(plugin_name, microbot):
    PluginDescriptor = JClass("net.runelite.client.plugins.PluginDescriptor")
    for plugin in microbot.getPluginManager().getPlugins():
        descriptor = plugin.getClass().getAnnotation(PluginDescriptor)
        if descriptor is not None and descriptor.name().contains(plugin_name):
                print(f"plugin enabled: {descriptor.name()}")
                return plugin

def walkToLocation(x, y, plane):
    print("start walking")
    walker = JClass("net.runelite.client.plugins.microbot.util.walker.Rs2Walker")
    walker.walkTo(x, y, plane)

def run(input_dict):
    plugin_name = "Auto Mining"

    time.sleep(10)
    walkToLocation(input_dict['x'], input_dict['y'], input_dict['plane'])

    microbot = JClass("net.runelite.client.plugins.microbot.Microbot")

    rocks = JClass("net.runelite.client.plugins.microbot.mining.enums.Rocks")
    #microbot.getConfigManager().setConfiguration("Mining", "Ore", rocks.GOLD)

    if input_dict['ore'] == "IRON":
        microbot.getConfigManager().setConfiguration("Mining", "Ore", rocks.IRON)
    microbot.getConfigManager().setConfiguration("Mining", "DistanceToStray", input_dict['stray'])
    microbot.getConfigManager().setConfiguration("Mining", "UseBank", input_dict['bank'])

    time.sleep(5)
    plugin = get_plugin_by_name(plugin_name, microbot)
    microbot.getPluginManager().setPluginEnabled(plugin, True)
    microbot.getPluginManager().startPlugins()
    
    time.sleep(3600)

    microbot.getPluginManager().setPluginEnabled(plugin, False)
    microbot.getPluginManager().stopPlugin(plugin)
    print('MANUAL STOP BY SCRIPT')
    exit()

if __name__ == "__main__":
    JAR_PATH = "/opt/microbot/microbot.jar"
    jpype.startJVM(classpath=[JAR_PATH])
    MainClass = JClass("net.runelite.client.RuneLite")
    MainClass.main([])

    input_dict = {
        'x': 2981,
        'y': 3234,
        'plane': 0,
        'ore': "IRON",
        'stray': 10,
        'bank': True
    }

    run(input_dict)