
import jpype
from jpype import JClass
import jpype.imports
import time
import ast

from scripts.script_util.general import General
from util.logger import SimpleLogger

class AutoCombat():
    def __init__(self, user):
        self.user = user
        self.plugin_name = "AIO Fighter"
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

        self.input_dict = input_dict
        job_details = ast.literal_eval(input_dict['var1'])
        location = ast.literal_eval(input_dict['location'])
        var3 = input_dict['var3'].split(',')


        self.set_equipment(var3)
        print('equipment set')

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

    def set_equipment(self, item_dict):
        
        rs2bank = JClass("net.runelite.client.plugins.microbot.util.bank.Rs2Bank")
        rs2inventory = JClass("net.runelite.client.plugins.microbot.util.inventory.Rs2Inventory")
        while True:
            rs2bank.walkToBankAndUseBank()
            time.sleep(3)
            rs2bank.depositEquipment()
            time.sleep(1)
            rs2bank.depositAll()
            time.sleep(2)
            equipment = self.general.pick_equipment()
            time.sleep(2)
            rs2bank.closeBank()

            if len(equipment) > 0:
                break

        for item in equipment:
            rs2inventory.wield(item)

    
    def plugin_config(self, job_details):
        playstyle = JClass("net.runelite.client.plugins.microbot.aiofighter.enums.PlayStyle")
        config_group = "PlayerAssistant"
        #microbot.getConfigManager().setConfiguration("Mining", "Ore", rocks.GOLD)

        for k, v in job_details.items():
            if k == 'PlayStyle':
                if v == 'Cautious':
                    self.microbot.getConfigManager().setConfiguration(config_group, k, playstyle.CAUTIOUS)
            else:
                self.microbot.getConfigManager().setConfiguration(config_group, k, v)
        self.microbot.getConfigManager().setConfiguration(config_group, 'attackStyleChangeDelay', 60*2)
        
################ ENABLE SKILLING
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
    mining = AutoCombat()
    mining.run(input_dict)