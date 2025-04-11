
import jpype
from jpype import JClass, java
import jpype.imports
import time
import sys
import random

from scripts.AutoCombat import AutoCombat
from scripts.AutoFishing import AutoFishing
from scripts.AutoCooking import AutoCooking
from scripts.AutoSmelting import AutoSmelting
from scripts.AutoMining import AutoMining 
from scripts.GetStats import GetStats
from scripts.GetBank import GetBank
from scripts.GoForAWalk import GoForAWalk
from util.db import MariaDB
from util.job_handler import Jobs
from util.logger import SimpleLogger

class jvm():
    def __init__(self, user):
        self.db = MariaDB()
        self.job = Jobs()
        self.user = user
        self.user_dict = self.db.get_user(self.user)[0]
        self.logger = SimpleLogger()

        self.class_map = {
            "AutoMining": AutoMining,
            "GetStats": GetStats,
            "AutoFishing": AutoFishing,
            "GetBank": GetBank,
            "AutoCooking": AutoCooking,
            "AutoSmelting": AutoSmelting,
            "GoForAWalk": GoForAWalk,
            "AutoCombat": AutoCombat
        }
        
        JAR_PATH = "/opt/microbot/microbot.jar"
        jpype.startJVM(classpath=[JAR_PATH])
        MainClass = JClass("net.runelite.client.RuneLite")
        MainClass.main([])
        time.sleep(10)

        self.microbot = JClass("net.runelite.client.plugins.microbot.Microbot")
        
    def get_plugin_by_name(self, plugin_name):
        PluginDescriptor = JClass("net.runelite.client.plugins.PluginDescriptor")
        for plugin in self.microbot.getPluginManager().getPlugins():
            descriptor = plugin.getClass().getAnnotation(PluginDescriptor)
            if descriptor is not None and descriptor.name().contains(plugin_name):
                    print(f"plugin enabled: {descriptor.name()}")
                    return plugin
    
    def enable_plugin(self, plugin_name):
        plugin = self.get_plugin_by_name(plugin_name)
        self.microbot.getPluginManager().setPluginEnabled(plugin, True)
        self.microbot.getPluginManager().startPlugins()
        time.sleep(15)
        self.microbot.getPluginManager().setPluginEnabled(plugin, False)
        self.microbot.getPluginManager().stopPlugin(plugin)

    def create_instance(self, job_dict):
        if type(job_dict) == str:
            class_name = job_dict
        else:
            class_name = job_dict['script']
        if class_name in self.class_map:
            return self.class_map[class_name](self.user)
        else:
            raise ValueError(f"Class name '{class_name}' is not recognized.")

    def check_dependencies(self):
        Microbot = JClass('net.runelite.client.plugins.microbot.Microbot')
        if Microbot.lastScriptMessage == "":
            return True
        else:
            self.logger.info(self.user, f'showMessage: {Microbot.lastScriptMessage}')
            print(Microbot.lastScriptMessage)
            return False

    def stop_jvm(self, job_dict):
        rs2player = JClass('net.runelite.client.plugins.microbot.util.player.Rs2Player')
        try:
            rs2player.logout()
        except:
            pass
        self.logger.info(self.user, f'Stopping job: {job_dict['script']}')

        self.play_end = time.time()
        self.duration = int(self.play_end - self.play_start)
        total_playtime_today = int(self.user_dict['played_today']) + self.duration
        total_playtime = int(self.user_dict['total_playtime']) + self.duration
        self.db.update_time_played_today(self.user_dict['osrs_user'], total_playtime_today, total_playtime)
        self.db.set_user_status(self.user, 'stopped')
        time.sleep(3)
        java.lang.System.exit(0)

    def get_session_time(self, stats):
        total_lvl = 0
        for k, v in stats.items():
            total_lvl += v
        if total_lvl > 1000:
            self.db.update_playtime(3600*4, self.user_dict['osrs_user'])
            return 30
        elif total_lvl > 500:
            self.db.update_playtime(3600*3, self.user_dict['osrs_user'])
            return 23
        else:
            self.db.update_playtime(3600*1, self.user_dict['osrs_user'])
            return 3

    def runner(self):
        
        self.enable_plugin('AutoLogin')

        self.db.set_user_status(self.user, 'working')

        self.play_start = time.time()

        stats = self.create_instance('GetStats').run()
        session_time = self.get_session_time(stats)
        bank_inv = self.create_instance('GetBank').run()
        
        job_dict = self.job.get_job(stats, bank_inv)
        print(job_dict)
        if random.random() <= 0.2:
            job = self.create_instance('GoForAWalk')
        else:
            job = self.create_instance(job_dict)
        
        first_loop = True
        now = time.time()
        print(f'Session time: {session_time} minutes')
        while time.time() < now + session_time*60:
            if first_loop:
                self.logger.info(self.user, f'Job assigned: {job_dict['script']}')
                job.run(job_dict)
                first_loop = False
            if self.check_dependencies():
                pass
            else:
                break
            time.sleep(5)
            
        job.stop()
        self.stop_jvm(job_dict)


if __name__ == "__main__":
    

    vm = jvm(sys.argv[1])
    #vm.job.get_job('st')
    vm.runner()