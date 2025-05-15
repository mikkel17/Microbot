
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
from scripts.AutoSmtihing import AutoSmithing
from scripts.AutoMining import AutoMining 
from scripts.GetStats import GetStats
from scripts.GetBank import GetBank
from scripts.GetGE import GetGE
from scripts.script_util.general import General
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
            "AutoCombat": AutoCombat,
            "AutoSmithing": AutoSmithing,
            "GetGE": GetGE
        }
        
        JAR_PATH = "/opt/microbot/microbot.jar"
        jpype.startJVM(classpath=[JAR_PATH])
        MainClass = JClass("net.runelite.client.RuneLite")
        MainClass.main([])
        time.sleep(10)

        self.microbot = JClass("net.runelite.client.plugins.microbot.Microbot")
        self.general = General()

    def create_instance(self, job_dict):
        if type(job_dict) == str:
            class_name = job_dict
        else:
            class_name = job_dict['script']
        if class_name in self.class_map:
            return self.class_map[class_name](self.user)
        else:
            raise ValueError(f"Class name '{class_name}' is not recognized.")

    def check_dependencies(self, job_dict):
        Microbot = JClass('net.runelite.client.plugins.microbot.Microbot')
        if Microbot.lastScriptMessage == "":
            return True
        elif Microbot.lastScriptMessage == "WebWalker troubles":
            self.logger.info(self.user, f'WebWalker troubles - trying again. Script: {job_dict['script']}')
            Microbot.lastScriptMessage = ""
            return True
        else:
            self.logger.info(self.user, f'showMessage: {Microbot.lastScriptMessage}')
            print(Microbot.lastScriptMessage)
            return False
    
    def logged_in(self):
        if self.microbot.isLoggedIn():
            return True
        else:
            time.slee(60)
            if self.microbot.isLoggedIn():
                return True
            else:
                return False

        
    def stop_jvm(self, job_dict):
        exp_total = self.general.get_total_exp()
        exp_earned = exp_total - self.exp_before
        self.db.update_exp(self.user_dict['osrs_user'], exp_total, exp_earned)

        rs2player = JClass('net.runelite.client.plugins.microbot.util.player.Rs2Player')
        try:
            rs2player.logout()
        except:
            pass
        self.logger.info(self.user, f'Stopping job: {job_dict['script']}. Exp earned: {exp_earned}')

        self.play_end = time.time()
        self.duration = int(self.play_end - self.play_start)
        total_playtime_today = int(self.user_dict['played_today']) + self.duration
        total_playtime = int(self.user_dict['total_playtime']) + self.duration
        self.db.update_time_played_today(self.user_dict['osrs_user'], total_playtime_today, total_playtime)
        self.db.set_user_status(self.user_dict['osrs_user'], 'stopped')
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
            return 15

    def total_playtime_check(self):
        if self.user_dict['account_status'] == "trial" and self.user_dict['total_playtime'] >= 60*60*20:
            self.db.set_account_status(self.user_dict['osrs_user'], 'ready')
            self.logger.info(self.user, f'{self.user_dict['osrs_user']} out of trial and ready')


    def runner(self):
        try:
            self.general.disable_all_plugins()
            self.general.login()
            self.general.configure_WebWalker()
            self.exp_before = self.general.get_total_exp()

            self.db.set_user_status(self.user_dict['osrs_user'], 'working')

            self.play_start = time.time()

            stats = self.create_instance('GetStats').run()
            session_time = self.get_session_time(stats)
            bank_inv = self.create_instance('GetBank').run()
            
            if random.random() <= 0.1:
                job = self.create_instance('GoForAWalk')
                walking = True
                job_dict = {'script': 'GoForAWalk'}
                print(job_dict)
            elif self.user_dict['account_status'] == 'trial':
                job = self.create_instance('GoForAWalk')
                walking = True
                job_dict = {'script': 'GoForAWalk'}
                print(job_dict)
            else:
                job_dict = self.job.get_job(stats, bank_inv)
                print(job_dict)
                job = self.create_instance(job_dict)
                walking = False
            
            first_loop = True
            now = time.time()
            print(f'Session time: {session_time} minutes')
            while time.time() < now + session_time*60:
                if walking:
                    self.logger.info(self.user, f'Job assigned: "GoForAWalk"')
                    job.run(job_dict)
                    break
                elif first_loop:
                    self.logger.info(self.user, f'Job assigned: {job_dict['name']}')
                    job.run(job_dict)
                    first_loop = False

                if not self.check_dependencies(job_dict):
                    break
                if not self.logged_in():
                    break
                
                time.sleep(5)
                
            job.stop()
            self.stop_jvm(job_dict)
        except Exception as e:
            self.logger.info(self.user, f'An exception happened: \n {e}')
            self.stop_jvm(job_dict)

if __name__ == "__main__":
    

    vm = jvm(sys.argv[1])
    #vm.job.get_job('st')
    vm.runner()