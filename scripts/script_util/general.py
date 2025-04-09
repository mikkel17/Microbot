from jpype import JClass
import jpype
import time


class General():
    
    def get_stats(self):
        Skill = JClass("net.runelite.api.Skill")
        microbot = JClass("net.runelite.client.plugins.microbot.Microbot")
        skill_attack = int(microbot.getClient().getBoostedSkillLevel(Skill.ATTACK))
        skill_strength = int(microbot.getClient().getBoostedSkillLevel(Skill.STRENGTH))
        skill_defence = int(microbot.getClient().getBoostedSkillLevel(Skill.DEFENCE))
        skill_ranged = int(microbot.getClient().getBoostedSkillLevel(Skill.RANGED))
        skill_prayer = int(microbot.getClient().getBoostedSkillLevel(Skill.PRAYER))
        skill_magic = int(microbot.getClient().getBoostedSkillLevel(Skill.MAGIC))
        skill_runecraft = int(microbot.getClient().getBoostedSkillLevel(Skill.RUNECRAFT))
        skill_hitpoints = int(microbot.getClient().getBoostedSkillLevel(Skill.HITPOINTS))
        skill_crafting = int(microbot.getClient().getBoostedSkillLevel(Skill.CRAFTING))
        skill_mining = int(microbot.getClient().getBoostedSkillLevel(Skill.MINING))
        skill_smithing = int(microbot.getClient().getBoostedSkillLevel(Skill.SMITHING))
        skill_fishing = int(microbot.getClient().getBoostedSkillLevel(Skill.FISHING))
        skill_cooking = int(microbot.getClient().getBoostedSkillLevel(Skill.COOKING))
        skill_firemaking = int(microbot.getClient().getBoostedSkillLevel(Skill.FIREMAKING))
        skill_woodcutting = int(microbot.getClient().getBoostedSkillLevel(Skill.WOODCUTTING))
        skill_agility = int(microbot.getClient().getBoostedSkillLevel(Skill.AGILITY))
        skill_herblore = int(microbot.getClient().getBoostedSkillLevel(Skill.HERBLORE))
        skill_thieving = int(microbot.getClient().getBoostedSkillLevel(Skill.THIEVING))
        skill_fletching = int(microbot.getClient().getBoostedSkillLevel(Skill.FLETCHING))
        skill_slayer = int(microbot.getClient().getBoostedSkillLevel(Skill.SLAYER))
        skill_farming = int(microbot.getClient().getBoostedSkillLevel(Skill.FARMING))
        skill_construction = int(microbot.getClient().getBoostedSkillLevel(Skill.CONSTRUCTION))
        skill_hunter = int(microbot.getClient().getBoostedSkillLevel(Skill.HUNTER))

        stats = {
            "Attack": skill_attack,
            "Strength": skill_strength,
            "Defence": skill_defence,
            "Ranged": skill_ranged,
            "Prayer": skill_prayer,
            "Magic": skill_magic,
            "Runecraft": skill_runecraft,
            "Hitpoints": skill_hitpoints,
            "Crafting": skill_crafting,
            "Mining": skill_mining,
            "Smithing": skill_smithing,
            "Fishing": skill_fishing,
            "Cooking": skill_cooking,
            "Firemaking": skill_firemaking,
            "Woodcutting": skill_woodcutting,
            "Agility": skill_agility,
            "Herblore": skill_herblore,
            "Thieving": skill_thieving,
            "Fletching": skill_fletching,
            "Slayer": skill_slayer,
            "Farming": skill_farming,
            "Construction": skill_construction,
            "Hunter": skill_hunter
        }

        return stats
    
    def get_bank_items(self, items):
        rs2bank = JClass("net.runelite.client.plugins.microbot.util.bank.Rs2Bank")
        items_result = {}
        while True:

            MAX_RETRIES = 3
            DELAY_BETWEEN_RETRIES = 1  # seconds

            for attempt in range(MAX_RETRIES):
                try:
                    rs2bank.walkToBank()
                    break  # success, exit the loop
                except jpype.JException as e:
                    print(f"[Attempt {attempt + 1}] Java Exception: {e}")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(DELAY_BETWEEN_RETRIES)
                    else:
                        print("All retries failed. Giving up.")
                        raise  # re-raise the last exception if all attempts fail
            time.sleep(5)
            rs2bank.openBank()
            time.sleep(1)
            rs2bank.depositEquipment()
            time.sleep(1)
            rs2bank.depositAll()
            time.sleep(1)
            for item in items:
                items_result[item] = rs2bank.count(item)
            if items_result != {}:
                break
        rs2bank.closeBank()
        return items_result
    
    def pick_tool(self, tool_dict):
        stats = self.get_stats()
        rs2bank = JClass("net.runelite.client.plugins.microbot.util.bank.Rs2Bank")
        tool = next(iter(tool_dict))

        if tool == 'pickaxe':
            skill = 'Mining'
        elif tool == 'axe':
            skill = 'Woodcutting'
        else:
            skill = 'xxx'
        
        axes = {
            f'rune {tool}': 41,
            f'adamant {tool}': 31,
            f'mithril {tool}': 21,
            f'steel {tool}': 6,
            f'iron {tool}': 1,
            f'bronze {tool}': 1
        }

        for axe, lvl in axes.items():
            if stats[skill] >= lvl and rs2bank.hasBankItem(JClass("java.lang.String")(axe)):
                rs2bank.withdrawItem(axe)
                return axe
        
        return 'No tool found' #### IF NO TOOL FOUND, CALL TO BUY ONE!
