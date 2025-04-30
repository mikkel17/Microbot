
import jpype
from jpype import JClass
import jpype.imports
import time

from scripts.script_util.general import General
from util.logger import SimpleLogger
from util.db_ge import MariaDB_ge
from util.db import MariaDB

class GetGE():
    def __init__(self, user):
        self.user = user
        self.plugin_name = "GetGE"
        self.general = General()
        self.db_ge = MariaDB_ge()
        self.db = MariaDB()

        self.user_dict = self.db.get_user(self.user)[0]


    def get_plugin_by_name(self, microbot):
        PluginDescriptor = JClass("net.runelite.client.plugins.PluginDescriptor")
        for plugin in microbot.getPluginManager().getPlugins():
            descriptor = plugin.getClass().getAnnotation(PluginDescriptor)
            if descriptor is not None and descriptor.name().contains(self.plugin_name):
                    print(f"plugin enabled: {descriptor.name()}")
                    return plugin

    def run(self):

        if not self.db_ge.existing_offer(self.user_dict['osrs_user']):
            return
        
        


        MAX_RETRIES = 3
        DELAY_BETWEEN_RETRIES = 1  # seconds

        for attempt in range(MAX_RETRIES):
            try:
                bank_inv = self.general.get_bank_items(self.items)
                
                for k, v in bank_inv.items():
                    print(f"{k}: {v}")
                
                return bank_inv

            except:
                print("GetBank failed")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(DELAY_BETWEEN_RETRIES)
                else:
                    print("All retries failed. Giving up.")
                    raise  # re-raise the last exception if all attempts fail


if __name__ == "__main__":
    JAR_PATH = "/opt/microbot/microbot.jar"
    jpype.startJVM(classpath=[JAR_PATH])
    MainClass = JClass("net.runelite.client.RuneLite")
    MainClass.main([])

    stats = GetGE('osrs02')
    time.sleep(10)
    stats.run()