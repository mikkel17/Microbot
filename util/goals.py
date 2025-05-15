class Goals():
    def __init__(self):        
        self._1 = {
            "Attack": 14,
            "Strength": 10,
            "Defence": 10,
            "Ranged": 1,
            "Prayer": 1,
            "Magic": 1,
            "Runecraft": 1,
            "Hitpoints": 1,
            "Crafting": 1,
            "Mining": 15,
            "Smithing": 15,
            "Fishing": 15,
            "Cooking": 15,
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
        }


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
            "Smithing": 70,
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
        self.skill_sets = [self._1, self.skill_goals]
        
    def get_goal(self, player_skills):
        for skill_set in self.skill_sets:
            for player_skill, player_lvl in player_skills.items():
                if player_lvl < skill_set[player_skill]:
                    return skill_set

