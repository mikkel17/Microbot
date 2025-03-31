import random
from util.db import MariaDB
import ast

class Jobs():
    def __init__(self):
        self.db = MariaDB()

    def get_skilling_job(self, stats):
        doable_jobs = []
        for job in self.db.get_skill_job_types():
            doable = True
            for req, lvl in ast.literal_eval(job['req_skill']).items():
                if stats[req] >= lvl:
                    doable = True
                else:
                    doable = False
                    break
            if doable:
                doable_jobs.append(job)
            
        if len(doable_jobs) == 1:
            return doable_jobs[0]
        else:
            lowest_lvl = 999
            chosen_job = {}
            for job in doable_jobs:
                if stats[job['name']] <= lowest_lvl:
                    lowest_lvl = stats[job['name']]
                    chosen_job = job
                else:
                    continue
        return chosen_job
        
    def get_mm_job(self, stats):
        pass

    '''
    def get_skill(self, stats):
        lowest_lvl = 999
        for stat, lvl in stats.items():
            if lvl < lowest_lvl:
                chosen_skill = stat
                lowest_lvl = lvl
            else:
                continue
        return chosen_skill
    '''

    def get_job(self, stats):
        job_type = self.choose_type()
        if job_type == "skill":
            job = self.get_skilling_job(stats)
            return job
        else:
            pass

    def choose_type(self):
        rand_num = random.random()
        #change when mm is added
        if rand_num <= 3/3:
            return "skill"
        else:
            return "mm"


