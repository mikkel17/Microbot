
import jpype
from jpype import JClass
import jpype.imports
import time
import ast

from scripts.script_util.general import General
from util.logger import SimpleLogger

class AutoSmithing():
    def __init__(self, user):
        self.user = user
        self.plugin_name = "Varrock Anvil"
        self.microbot = JClass("net.runelite.client.plugins.microbot.Microbot")
        self.plugin = self.get_plugin_by_name()
        self.general = General()

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
        return

        ## needs to check if I can equip chosen pickaxe
    
    def plugin_config(self, job_details):
        stats = self.general.get_stats()
        smithing_lvl = stats['Smithing']

        item = JClass("net.runelite.client.plugins.microbot.smelting.enums.AnvilItem")
        bars = JClass("net.runelite.client.plugins.microbot.smelting.enums.Bars")
        #microbot.getConfigManager().setConfiguration("Mining", "Ore", rocks.GOLD)
        config_group = "VarrockAnvil"

        if job_details['barType'] == 'BRONZE':
            self.microbot.getConfigManager().setConfiguration(config_group, 'barType', bars.BRONZE)
            if smithing_lvl >= 18:
                self.microbot.getConfigManager().setConfiguration(config_group, 'smithObject', item.PLATE_BODY)
            elif smithing_lvl >= 16:
                self.microbot.getConfigManager().setConfiguration(config_group, 'smithObject', item.PLATE_LEGS)
            elif smithing_lvl >= 12:
                self.microbot.getConfigManager().setConfiguration(config_group, 'smithObject', item.KITE_SHIELD)
            elif smithing_lvl >= 7:
                self.microbot.getConfigManager().setConfiguration(config_group, 'smithObject', item.FULL_HELM)
            else:
                self.microbot.getConfigManager().setConfiguration(config_group, 'smithObject', item.DAGGER)

        elif job_details['barType'] == 'IRON':
            self.microbot.getConfigManager().setConfiguration(config_group, 'barType', bars.IRON)
            if smithing_lvl >= 33:
                self.microbot.getConfigManager().setConfiguration(config_group, 'smithObject', item.PLATE_BODY)
            elif smithing_lvl >= 31:
                self.microbot.getConfigManager().setConfiguration(config_group, 'smithObject', item.PLATE_LEGS)
            elif smithing_lvl >= 27:
                self.microbot.getConfigManager().setConfiguration(config_group, 'smithObject', item.KITE_SHIELD)
            elif smithing_lvl >= 22:
                self.microbot.getConfigManager().setConfiguration(config_group, 'smithObject', item.FULL_HELM)
            else:
                self.microbot.getConfigManager().setConfiguration(config_group, 'smithObject', item.DAGGER)
        else:
            raise

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
    mining = AutoSmelting()
    mining.run(input_dict)