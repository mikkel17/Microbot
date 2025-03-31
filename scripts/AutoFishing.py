
import jpype
from jpype import JClass
import jpype.imports
import time
import ast

from scripts.script_util.general import General

class AutoFishing():
    def __init__(self):
        self.plugin_name = "Auto Fishing"
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

    def walkToLocation(self, x, y, plane):
        print("start walking")
        walker = JClass("net.runelite.client.plugins.microbot.util.walker.Rs2Walker")
        walker.walkTo(x, y, plane)

    def run(self, input_dict):
        job_details = ast.literal_eval(input_dict['var1'])
        location = ast.literal_eval(input_dict['location'])
        req_item = input_dict['req_item']


        self.set_equipment(req_item)
        print('equipment set')

        self.walkToLocation(location['x'], location['y'], location['plane'])
       

        self.plugin_config(job_details)
        self.enable_plugin()
    
    def enable_plugin(self):
        self.microbot.getPluginManager().setPluginEnabled(self.plugin, True)
        self.microbot.getPluginManager().startPlugins()
        
    def stop(self):
        self.microbot.getPluginManager().setPluginEnabled(self.plugin, False)
        self.microbot.getPluginManager().stopPlugin(self.plugin)
        print('MANUAL STOP BY SCRIPT')
        time.sleep(3)
        return

    def set_equipment(self, item):
        rs2bank = JClass("net.runelite.client.plugins.microbot.util.bank.Rs2Bank")
        rs2bank.walkToBankAndUseBank()
        time.sleep(3)
        rs2bank.depositEquipment()
        time.sleep(1)
        rs2bank.depositAll()
        time.sleep(2)
        rs2bank.withdrawItem(item)
        time.sleep(2)
        rs2bank.closeBank()

        Rs2Inventory = JClass("net.runelite.client.plugins.microbot.util.inventory.Rs2Inventory")
        Rs2Inventory.wield(item)

        ## needs to check if I can equip chosen pickaxe
    
    def plugin_config(self, job_details):
        fish = JClass("net.runelite.client.plugins.microbot.nateplugins.skilling.natefishing.enums.Fish")
        #microbot.getConfigManager().setConfiguration("Mining", "Ore", rocks.GOLD)

        if job_details['fish'] == "shrimp":
            self.microbot.getConfigManager().setConfiguration("Fishing", "Fish", fish.SHRIMP)
        self.microbot.getConfigManager().setConfiguration("Fishing", "UseBank", job_details['bank'])
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
    mining = AutoFishing()
    mining.run(input_dict)