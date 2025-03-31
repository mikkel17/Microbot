
import jpype
from jpype import JClass
import jpype.imports
import time
from scripts.AutoMining import AutoMining
from scripts.AutoFishing import AutoFishing
from scripts.GetStats import GetStats
from util.db import MariaDB
from util.job_handler import Jobs

class jvm():
    def __init__(self):
        self.db = MariaDB()
        self.job = Jobs()


        self.class_map = {
            "AutoMining": AutoMining,
            "GetStats": GetStats,
            "AutoFishing": AutoFishing
        }
        
        JAR_PATH = "/opt/microbot/microbot.jar"
        jpype.startJVM(classpath=[JAR_PATH])
        MainClass = JClass("net.runelite.client.RuneLite")
        MainClass.main([])
        time.sleep(10)
        
        self.playtime = self.get_time()

    def create_instance(self, job_dict):
        if type(job_dict) == str:
            class_name = job_dict
        else:
            class_name = job_dict['script']
        if class_name in self.class_map:
            return self.class_map[class_name]()
        else:
            raise ValueError(f"Class name '{class_name}' is not recognized.")

    def check_dependencies(self):
        pass

    def get_skilling_job(self, stats):
        lowest_lvl = 999
        for stat, lvl in stats.items():
            if lvl < lowest_lvl:
                chosen_skill = stat
                lowest_lvl = lvl
            else:
                continue
        return chosen_skill
    
    def get_mm_job(self, stats):
        pass

        print(self.db.get_all_job_types())
        for job in self.db.get_all_job_types():
            print(job)
        return "mining"

    def get_time(self):
        playtime = 180
        return playtime

    def runner(self):

        input_dict = {
            'x': 2981,
            'y': 3234,
            'plane': 0,
            'ore': "IRON",
            'stray': 5,
            'bank': True
        }
        t_end = time.time() + 60 * self.playtime

        while time.time() < t_end:
            stat_job = self.create_instance('GetStats')
            stats = stat_job.run()
            
            job_dict = self.job.get_job(stats)
            print(job_dict)
            job = self.create_instance(job_dict)
            
            first_loop = True
            while time.time() < time.time() + 60*60:
                if first_loop:
                    job.run(job_dict)
                    first_loop = False
                self.check_dependencies()
                time.sleep(5)
                print('loop done')

            job.stop()


if __name__ == "__main__":
    

    vm = jvm()
    #vm.job.get_job('st')
    vm.runner()