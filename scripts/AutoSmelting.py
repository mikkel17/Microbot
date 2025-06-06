
import jpype
from jpype import JClass
import jpype.imports
import time
import ast

from scripts.script_util.general import General
from util.logger import SimpleLogger

class AutoSmelting():
    def __init__(self, user):
        self.user = user
        self.plugin_name = "Auto Smelting"
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

    def set_equipment(self, item_dict):
        item = next(iter(item_dict))
        rs2bank = JClass("net.runelite.client.plugins.microbot.util.bank.Rs2Bank")
        rs2inventory = JClass("net.runelite.client.plugins.microbot.util.inventory.Rs2Inventory")
        while True:
            rs2bank.walkToBankAndUseBank()
            time.sleep(3)
            rs2bank.depositEquipment()
            time.sleep(1)
            rs2bank.depositAll()
            time.sleep(2)
            self.general.pick_tool(item_dict)
            time.sleep(2)
            rs2bank.closeBank()

            if rs2inventory.hasItem(item):
                break
            else:
                print('trying to set item again. Item: ' + item)

        rs2inventory.wield(item)

        ## needs to check if I can equip chosen pickaxe
    
    def plugin_config(self, job_details):
        bars = JClass("net.runelite.client.plugins.microbot.smelting.enums.Bars")
        #microbot.getConfigManager().setConfiguration("Mining", "Ore", rocks.GOLD)
        config_group = "Smithing"
        if job_details['Bar'] == "BRONZE":
            self.microbot.getConfigManager().setConfiguration(config_group, "Bar", bars.BRONZE)
        if job_details['Bar'] == "IRON":
            self.microbot.getConfigManager().setConfiguration(config_group, "Bar", bars.IRON)
#        elif job_details['ore'] == "IRON":
#            self.microbot.getConfigManager().setConfiguration("Mining", "Ore", rocks.IRON)
        
#        self.microbot.getConfigManager().setConfiguration("Mining", "DistanceToStray", job_details['stray'])
#        self.microbot.getConfigManager().setConfiguration("Mining", "UseBank", job_details['bank'])
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