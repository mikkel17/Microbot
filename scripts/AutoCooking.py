
import jpype
from jpype import JClass
import jpype.imports
import time
import ast

from scripts.script_util.general import General
from util.logger import SimpleLogger

class AutoCooking():
    def __init__(self, user):
        self.user = user
        self.plugin_name = "Auto Cooking"
        self.microbot = JClass("net.runelite.client.plugins.microbot.Microbot")
        self.plugin = self.get_plugin_by_name()
        self.general = General()
        self.logger = SimpleLogger()

    def get_plugin_by_name(self):
        PluginDescriptor = JClass("net.runelite.client.plugins.PluginDescriptor")
        for plugin in self.microbot.getPluginManager().getPlugins():
            descriptor = plugin.getClass().getAnnotation(PluginDescriptor)
            if descriptor is not None and descriptor.name().contains(self.plugin_name):
                    print(f"plugin enabled: {descriptor.name()}")
                    return plugin

    def run(self, input_dict):

        job_details = ast.literal_eval(input_dict['var1'])
        location = ast.literal_eval(input_dict['location'])
        req_item = ast.literal_eval(input_dict['req_item'])

        #self.set_equipment(req_item)
        #print('equipment set')

        self.general.walkToLocation(location['x'], location['y'], location['plane'])

        self.plugin_config(job_details)
        self.enable_plugin()
    
    def enable_plugin(self):
        self.microbot.getPluginManager().setPluginEnabled(self.plugin, True)
        self.microbot.getPluginManager().startPlugins()
        
    def stop(self):
        self.general.disable_all_plugins()
        print('MANUAL STOP BY SCRIPT')
        time.sleep(10)
    
    def plugin_config(self, job_details):
        CookingItem = JClass("net.runelite.client.plugins.microbot.cooking.enums.CookingItem")
        CookingLocation = JClass("net.runelite.client.plugins.microbot.cooking.enums.CookingLocation")
        #CookingActivity = JClass("net.runelite.client.plugins.microbot.cooking.enums.CookingActivity")
        #microbot.getConfigManager().setConfiguration("Mining", "Ore", rocks.GOLD)

        #self.microbot.getConfigManager().setConfiguration("autocooking", "cookingActivity", CookingItem.COOKING)

        if job_details['itemToCook'] == "Raw shrimp":
            self.microbot.getConfigManager().setConfiguration("autocooking", "itemToCook", CookingItem.RAW_SHRIMP)
        elif job_details['itemToCook'] == "Raw anchovies":
            self.microbot.getConfigManager().setConfiguration("autocooking", "itemToCook", CookingItem.RAW_ANCHOVIES)
        if job_details['cookingLocation'] == "Al Kharid":
            self.microbot.getConfigManager().setConfiguration("autocooking", "cookingLocation", CookingLocation.AL_KHARID)
        time.sleep(5)


if __name__ == "__main__":
    JAR_PATH = "/opt/microbot/microbot.jar"
    jpype.startJVM(classpath=[JAR_PATH])
    MainClass = JClass("net.runelite.client.RuneLite")
    MainClass.main([])
    # get dict from database
    input_dict = {
        'x': 2981,
        'y': 3234,
        'plane': 0,
        'ore': "IRON",
        'stray': 10,
        'bank': True
    }
    mining = AutoCooking()
    mining.run(input_dict)