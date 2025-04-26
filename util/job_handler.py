import random
from util.db import MariaDB
import ast

class Jobs():
    def __init__(self):
        self.db = MariaDB()
        
        self.skill_goals = {
            "Attack": 40,
            "Strength": 40,
            "Defence": 30,
            "Ranged": 50,
            "Prayer": 50,
            "Magic": 50,
            "Runecraft": 50,
            "Hitpoints": 50,
            "Crafting": 50,
            "Mining": 50,
            "Smithing": 99,
            "Fishing": 50,
            "Cooking": 50,
            "Firemaking": 50,
            "Woodcutting": 50,
            "Agility": 1,
            "Herblore": 1,
            "Thieving": 1,
            "Fletching": 1,
            "Slayer": 1,
            "Farming": 1,
            "Construction": 1,
            "Hunter": 1
        }
        

        ## TESTING GOALS
        '''self.skill_goals = {
            "Attack": 1,
            "Strength": 1,
            "Defence": 1,
            "Ranged": 1,
            "Prayer": 1,
            "Magic": 1,
            "Runecraft": 1,
            "Hitpoints": 1,
            "Crafting": 1,
            "Mining": 1,
            "Smithing": 99,
            "Fishing": 1,
            "Cooking": 1,
            "Firemaking": 1,
            "Woodcutting": 1,
            "Agility": 1,
            "Herblore": 1,
            "Thieving": 1,
            "Fletching": 1,
            "Slayer": 1,
            "Farming": 1,
            "Construction": 1,
            "Hunter": 1
        }'''
    
        self.combat_type = ['Attack', 'Defence', 'Hitpoints', 'Magic', 'Prayer', 'Ranged', 'Strength']
        self.gathering_type = ['Farming', 'Fishing', 'Hunter', 'Mining', 'Woodcutting']
        self.production_type = ['Cooking', 'Crafting', 'Fletching', 'Herblore', 'Runecraft', 'Smithing']
        self.utility_type = ['Agility', 'Construction', 'Firemaking', 'Slayer', 'Thieving']

    
    def get_least_trained_trainable_skill(self, doable_jobs, skill_values):
        trainable_skills = []
        for job in doable_jobs:
            if job['skill'] not in trainable_skills:
                trainable_skills.append(job['skill'])
        
        # Filter the dictionaries to include only trainable skills
        filtered_skill_goals = {skill: self.skill_goals[skill] for skill in trainable_skills}
        filtered_skill_values = {skill: skill_values[skill] for skill in trainable_skills}

        # Calculate the differences for the filtered skills
        skill_differences = {skill: filtered_skill_goals[skill] - filtered_skill_values[skill] for skill in filtered_skill_goals}

        # Find the skill with the biggest difference among the trainable skills
        skill_with_biggest_difference = max(skill_differences, key=skill_differences.get)
        return skill_with_biggest_difference
    
    def get_highest_ranked_job_of_skill_type(self, skill_type, doable_jobs, bank):
        rank = 0
        chosen_jobs = []
        for job in doable_jobs:
            if job['skill'] == skill_type and job['ranking'] > rank:
                chosen_job = [job]
                rank = job['ranking']
            elif job['skill'] == skill_type and job['ranking'] == rank:
                chosen_job.append(job)
            else:
                continue
        if len(chosen_job) > 1:
            for job in chosen_job:
                met_req, item_req = self.check_item_requirements(job, bank)
                if met_req:
                    return job
            return chosen_job[0]
        else:
            return chosen_job[0]
        

    def check_item_requirements(self, job, bank):
        for item_req, amount in ast.literal_eval(job['req_item']).items():
            if amount <= bank[item_req]:
                continue
            else:
                return False, item_req
        return True, 'Not in use'
    
    def check_skill_requirements(self, job, stats):
        for skill, lvl in ast.literal_eval(job['req_skill']).items():
            if lvl <= stats[skill]:
                continue
            else:
                return False, skill
        return True, 'Not in use'


    def supply_chain_method(self, job_being_checked, doable_jobs, stats, bank):
            result_skill, failing_skill = self.check_skill_requirements(job_being_checked, stats)
            result_item, failing_item = self.check_item_requirements(job_being_checked, bank)
            
            if result_skill and result_item:
                return job_being_checked, True
            elif result_skill and not result_item:
                print(f'{doable_jobs}')
                for job in doable_jobs:
                    for output_item in job['output_item'].split(','):
                        if output_item == failing_item:
                            return job, False
                        else:
                            continue
                for job in self.db.get_skill_job_types():
                    print(f'{job}')
                    for output_item in job['output_item'].split(','):
                        if output_item == failing_item:
                            return job, False
                        else:
                            continue
            elif not result_skill and result_item:
                print(f"result_skill: {result_skill}, result_item: {result_item}")
                for job in doable_jobs:
                    for output_skill in job['output_skill'].split(','):
                        if output_skill == failing_skill:
                            return job, False
                        else:
                            continue
            else:
                raise Exception
            ### at this point, if we can't find a job that can deliver the right item, we need to buy the item (COMING SOON)

   
    def get_skilling_job(self, stats, bank):
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
        
        skill_type = self.get_least_trained_trainable_skill(doable_jobs, stats)
        highest_ranked_job = self.get_highest_ranked_job_of_skill_type(skill_type, doable_jobs, bank)

        job_being_checked = highest_ranked_job

        while True:
            print('Job evaluated: ' + str(job_being_checked['name']))
            new_job, req_met = self.supply_chain_method(job_being_checked, doable_jobs, stats, bank)
            if req_met:
                print('Job chosen: ' + str(new_job['name']))
                return new_job
            else:
                job_being_checked = new_job
            

        
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

    def get_job(self, stats, bank):
        job_type = self.choose_type()
        if job_type == "skill":
            job = self.get_skilling_job(stats, bank)
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


