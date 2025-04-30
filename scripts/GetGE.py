
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

    def buy(self):
        pass

    def run(self, input_dict, bank_inv):
        
        if not self.collect(input_dict):
            return
        else:
            if type(input_dict) == str:
                return
        
        ### NOW DO WHAT THE JOB SAYS buy/sell

        '''
        elif existing_offer[0]['state'] == 'request' and existing_offer[0]['offer'] == 'BUY':
            rs2bank.walkToBankAndUseBank()
            time.sleep(3)
            rs2bank.depositEquipment()
            time.sleep(1)
            rs2bank.depositAll()
            time.sleep(2)
            rs2bank.withdrawAll('Coins')
            time.sleep(2)
            rs2bank.closeBank()
            time.sleep(2)
            Rs2GrandExchange.openExchange()
            time.sleep(1)
            Rs2GrandExchange.buyItem(existing_offer[0]['item'], int(existing_offer[0]['price']*1.05), existing_offer[0]['quantity'])
            time.sleep(4)
            Rs2GrandExchange.closeExchange()
            time.sleep(2)
            self.db_ge.update_state(self.user_dict['osrs_user'], existing_offer[0]['item'], 'waiting')
            return
        elif existing_offer[0]['state'] == 'request' and existing_offer[0]['offer'] == 'SELL':
            rs2bank.walkToBankAndUseBank()
            time.sleep(3)
            rs2bank.depositEquipment()
            time.sleep(1)
            rs2bank.depositAll()
            time.sleep(2)
            rs2bank.withdrawAll('Coins')
            time.sleep(2)
            rs2bank.closeBank()
            time.sleep(2)
            Rs2GrandExchange.openExchange()
            time.sleep(1)
            Rs2GrandExchange.buyItem(existing_offer[0]['item'], int(existing_offer[0]['price']*1.05), existing_offer[0]['quantity'])
            time.sleep(4)
            Rs2GrandExchange.closeExchange()
            time.sleep(2)
            self.db_ge.update_state(self.user_dict['osrs_user'], existing_offer[0]['item'], 'waiting')
            return
            '''

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

    def collect(self, input_dict):
        existing_offer = self.db_ge.existing_offer(self.user_dict['osrs_user'])
        ## check if we have any things to do at GE
        if len(existing_offer) == 0:
            return True
        else:
            self.general.walkToLocation(3163, 3487, 0)

        Rs2GrandExchange = JClass("net.runelite.client.plugins.microbot.util.grandexchange.Rs2GrandExchange")
        rs2bank = JClass("net.runelite.client.plugins.microbot.util.bank.Rs2Bank")
        # Check if waiting offer is ready to be collected
        if existing_offer[0]['state'] == 'waiting':
            # Collect 
            Rs2GrandExchange.walkToGrandExchange()
            time.sleep(1)
            Rs2GrandExchange.openExchange()
            time.sleep(1)
            if Rs2GrandExchange.hasSoldOffer():
                Rs2GrandExchange.collectToBank()
                self.db_ge.update_state(self.user_dict['osrs_user'], existing_offer[0]['item'], 'collected')
                return True
            else:
                #### OFFER WASNT BOUGHT/SOLD - WAIT LONGER? CHANGE PRICE?
                Rs2GrandExchange.closeExchange()
                time.sleep(1)
                return False

if __name__ == "__main__":
    JAR_PATH = "/opt/microbot/microbot.jar"
    jpype.startJVM(classpath=[JAR_PATH])
    MainClass = JClass("net.runelite.client.RuneLite")
    MainClass.main([])

    stats = GetGE('osrs02')
    time.sleep(10)
    stats.run()