
import jpype
from jpype import JClass
import jpype.imports
import time

from scripts.script_util.general import General


class GetStats():
    def __init__(self):
        self.plugin_name = "GetStats"
        self.general = General()

    def get_plugin_by_name(self, microbot):
        PluginDescriptor = JClass("net.runelite.client.plugins.PluginDescriptor")
        for plugin in microbot.getPluginManager().getPlugins():
            descriptor = plugin.getClass().getAnnotation(PluginDescriptor)
            if descriptor is not None and descriptor.name().contains(self.plugin_name):
                    print(f"plugin enabled: {descriptor.name()}")
                    return plugin

    def walkToLocation(self, x, y, plane):
        print("start walking")
        walker = JClass("net.runelite.client.plugins.microbot.util.walker.Rs2Walker")
        walker.walkTo(x, y, plane)

    def run(self):

        stats = self.general.get_stats()

        player = JClass("net.runelite.client.plugins.microbot.util.player.Rs2Player")

        rocks = JClass("net.runelite.client.plugins.microbot.mining.enums.Rocks")
        




        for k, v in stats.items():
            print(f"{k}: {v}")



        rs2bank = JClass("net.runelite.client.plugins.microbot.util.bank.Rs2Bank")
        
        rs2bank.walkToBank()
        rs2bank.openBank()
        print(rs2bank.findBankItem('Iron ore'))

        #rs2bank.openBank()
        time.sleep(2)
        print(rs2bank.hasBankItem(JClass("java.lang.String")("Iron ore")))
        print(rs2bank.hasBankItem(JClass("java.lang.String")("Iron ore"), jpype.JInt(2)))
        print(rs2bank.hasBankItem(JClass("java.lang.String")("Iron ore"), jpype.JInt(9999)))
        
        rs2bank.closeBank()
        '''
        print("INVENTORY TEST")
        item_list = ["Camo top", "Camo bottoms", "leather gloves", "Leather boots", "Staff of fire"]
        
        Rs2Inventory = JClass("net.runelite.client.plugins.microbot.util.inventory.Rs2Inventory")
        
        rs2bank.openBank()
        
        rs2bank.depositEquipment()

        rs2bank.depositAll()

        for item in item_list:
            rs2bank.withdrawItem(item)
            time.sleep(2)        

        self.general.pick_tool('axe')

        rs2bank.closeBank()
        
        for item in item_list:
            Rs2Inventory.wield(item)
            time.sleep(2)
        '''
        
        return stats

        #microbot.getConfigManager().setConfiguration("Mining", "Ore", rocks.GOLD)

        #if input_dict['ore'] == "IRON":
        #    microbot.getConfigManager().setConfiguration("Mining", "Ore", rocks.IRON)
        #microbot.getConfigManager().setConfiguration("Mining", "DistanceToStray", input_dict['stray'])
        #microbot.getConfigManager().setConfiguration("Mining", "UseBank", input_dict['bank'])

        #time.sleep(5)
        #plugin = get_plugin_by_name(plugin_name, microbot)
        #microbot.getPluginManager().setPluginEnabled(plugin, True)
        #microbot.getPluginManager().startPlugins()
        
        #time.sleep(3600)

        #microbot.getPluginManager().setPluginEnabled(plugin, False)
        #microbot.getPluginManager().stopPlugin(plugin)
        
        
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

    stats = GetStats()
    time.sleep(10)
    stats.run(input_dict)