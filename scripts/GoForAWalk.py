
import jpype
from jpype import JClass
import jpype.imports
import time
import random

from scripts.script_util.general import General
from util.logger import SimpleLogger

class GoForAWalk():
    def __init__(self, user):
        self.user = user
        self.plugin_name = "GoForAWalk"
        self.general = General()

    def get_plugin_by_name(self, microbot):
        PluginDescriptor = JClass("net.runelite.client.plugins.PluginDescriptor")
        for plugin in microbot.getPluginManager().getPlugins():
            descriptor = plugin.getClass().getAnnotation(PluginDescriptor)
            if descriptor is not None and descriptor.name().contains(self.plugin_name):
                    print(f"plugin enabled: {descriptor.name()}")
                    return plugin

    def stop(self):
        print('MANUAL STOP BY SCRIPT')

    def run(self, job_dict):
        self.set_equipment()
        coordinates = [
             [2973, 3316, 0],
             [2933, 3292, 0],
             [2960, 3208, 0],
             [2920, 3226, 0],
             [3001, 3131, 0],
             [3026, 3207, 0],
             [2956, 3496, 0],
             [3080, 3423, 0],
             [3079, 3509, 0],
             [3213, 3471, 0],
             [3227, 3408, 0],
             [3085, 3250, 0],
             [3111, 3170, 0],
             [3321, 3144, 0],
             [3284,3470, 0]
        ]
        random.shuffle(coordinates)
        for coord in coordinates[:3]:
            self.general.walkToLocation(coord[0], coord[1], coord[2])
            time.sleep(60*3)
        
    def set_equipment(self):
        
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


if __name__ == "__main__":
    JAR_PATH = "/opt/microbot/microbot.jar"
    jpype.startJVM(classpath=[JAR_PATH])
    MainClass = JClass("net.runelite.client.RuneLite")
    MainClass.main([])


    stats = GoForAWalk()
    time.sleep(10)
    stats.run()