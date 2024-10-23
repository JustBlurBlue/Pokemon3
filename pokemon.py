from __future__ import annotations



import skills
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from skills import *
    from effects import Effect

from Ways import *
import random
class Pokemon:
    name: str
    type: str
    preparing =False
    preparing_skill:Skill=None
    preparing_opponent:Pokemon=None

    def __init__(self, num: int,owner:int,operator:str,hp: int, attack: int, defense: int,miss_rate:int) -> None:
        # 初始化 Pokemon 的属性
        self.owner_id:str = self.name+'[P'+str(owner)+f'({(num+1)})'+']'
        self.operater:str = operator
        self.index:int = num
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.skills = self.initialize_skills()
        self.alive = True
        self.statuses_begin = []
        self.status_use_skills = []
        self.statuses_defence = []
        self.miss_rate = miss_rate
        self.miss_rate0=miss_rate
        self.sleep_status: bool =False
        self.protected = False
        self.damage_history = []
        self.protected = False
        self.Agility = False

    def change_index(self):
        self.index -= 1
    def set_sleep(self,status:bool=False)->None:
        if status:
            self.sleep_status = True
            self.preparing = False
        else:
            self.sleep_status = False
    def initialize_skills(self):
        # 抽象方法，子类应实现具体技能初始化
        raise NotImplementedError
    #打印技能
    def print_skills(self):
        for i, skill in enumerate(self.skills, 1):
            print(f"{i}: {skill.name}")

    def use_skill(self, skill: Skill, opponent: Pokemon,prepared:bool=False) -> None:
        # 使用技能

        print(f"{self} 使用了 {skill.name}")
        if not prepared:
            damage = skill.execute(self, opponent)
        else:
            damage = skill.execute(self, opponent)
        if damage > 0:
            self.damage_history.append(damage)

    def heal_self(self, amount):
        # 为自身恢复生命值
        if not isinstance(amount, int):
            amount = int(amount)

        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    # 计算是否闪避,若闪避则返回True,否则返回False
    def miss_compute(self,opponent: Pokemon,ignore_miss_rate:int=0)->bool:

        if self.sleep_status == False and random.randint(1, 100) <= (self.miss_rate-ignore_miss_rate)  :
            print(f"{self}闪避了攻击!")
            return True
        return False

    def receive_damage(self, damage:float,type1:str,ignoore_defense:bool=False):
        # 计算伤害并减去防御力，更新 HP
        if not self.alive:
            return 0
        if not isinstance(damage, int):
            damage = int(damage)
        # 计算属性克制
        effectiveness = self.type_effectiveness(type1)
        damage *= effectiveness
        # 计算伤害减免
        if not ignoore_defense:
            damage -= self.defense
            if damage <= 0:
                print(f"{self}的防御力抵消了所有伤害! 当前HP: {self.hp}/{self.max_hp}")
                damage = 0

        self.hp -= damage

        if self.hp <= 0:
            self.alive = False
            self.hp=0

        return damage


    def add_status_effect(self, effect: Effect,weizhi:int):
        # 添加状态效果
        if weizhi == 1:
            self.statuses_begin.append(effect)
        elif weizhi == 2:
            self.status_use_skills.append(effect)
        elif weizhi == 3:
            self.statuses_defence.append(effect)


    def apply_status_effect_begin(self):
        # 应用所有当前的状态效果，并移除持续时间结束的效果
        for status in self.statuses_begin[:]:  # 使用切片防止列表在遍历时被修改
            status.apply(self)
            status.decrease_duration()
            if status.duration <= 0:
                print(f"{self} 的 {status.name} 效果结束.")
                self.statuses_begin.remove(status)
    def apply_status_effect_use_skills(self):
        # 应用所有当前的状态效果，并移除持续时间结束的效果
        for status in self.status_use_skills[:]:  # 使用切片防止列表在遍历时被修改
            status.apply(self)
            status.decrease_duration()
            if status.duration <= -1:
                print(f"{self} 的 {status.name} 效果结束.")
                self.status_use_skills.remove(status)
    def apply_status_effect_defence(self):
        for status in self.statuses_defence[:]:
            status.apply(self)
            status.decrease_duration()
            if status.duration <= -1:

                self.statuses_defence.remove(status)

    def type_effectiveness(self, opponent: str):
        # 计算属性克制的抽象方法，具体实现由子类提供
        raise NotImplementedError

    def begin(self):
        # 新回合开始时触发的方法
        pass

    def __str__(self) -> str:
        return f"{self.name} type: {self.type}"
    # 蓄力宝可梦专属
    def set_preparing(self,skill:Skill=None, x: bool=False,opponent:Pokemon=None):
            self.preparing= x
            self.preparing_skill=skill
            self.preparing_opponent=opponent

    def set_proptected(self, x: bool):
        if x:
            self.protected = True
        else:
            self.protected = False
    def set_miss_rate(self,miss_rate:int):
        self.miss_rate = miss_rate
    def fresh_skill(self):
        self.skills = self.initialize_skills()
    def set_Agility(self,x:bool):
        self.Agility = x


# GrassPokemon 类
class GrassPokemon(Pokemon):
    type = "Grass"

    def type_effectiveness(self, opponent:str):
        # 针对 技能 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponent

        if opponent_type == "Water":
            effectiveness = 0.75
        elif opponent_type == "Fire":
            effectiveness = 1.5
        return effectiveness

    def begin(self):
        self.grass_attribute()
        # 回合开始时清醒
        self.sleep_status = False

    def grass_attribute(self):
        # 草属性特性：每回合恢复 失去生命值的 10%
        amount = (self.max_hp-self.hp) * 0.18
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(
            f"{self} 在回合开始治愈了已损失生命值18% {amount} 点HP! 当前HP: {self.hp}/{self.max_hp}"
        )
# ElectricPokemon 类
class ElectricPokemon(Pokemon):
    type = "Electric"

    def __init__(self, num: int, owner: int, operator: str, hp: int, attack: int, defense: int, miss_rate: int):
        super().__init__(num, owner, operator, hp, attack, defense, miss_rate)


    def type_effectiveness(self, opponenttype:str):
        # 针对 技能 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponenttype

        if opponent_type == "Water":
            effectiveness = 0.75
        elif opponent_type == "Grass":
            effectiveness = 1.5
        return effectiveness

    def miss_compute(self, opponent: Pokemon,ignore_miss_rate: int = 0, ):

        if self.sleep_status == False and  random.randint(1, 100) <= self.miss_rate - ignore_miss_rate:
            print(f"{self}闪避了攻击!,触发电属性特性，发动技能!")
            self.electric_attribute(opponent)
            return True
        else:
            return False

    def begin(self):
        self.sleep_status = False

    # 电属性特性：闪避成功，发动技能
    def electric_attribute(self, opponent: Pokemon):
        self.print_skills()
        if self.operater != "PC":
            choose = input_check(f"{self.owner_id}:请选择你要使用的技能:")
            choose = int(choose) - 1
        else:
            choose = random.randint(0, len(self.skills)-1)
        skill = self.skills[choose]
        # 技能效果
        self.use_skill(skill,opponent)
class FirePokemon(Pokemon):
    type = "Fire"
    layer = 0

    def __init__(self, num: int, owner: int, operator: str, hp: int, attack: int, defense: int, miss_rate: int):
        super().__init__(num, owner, operator, hp, attack, defense, miss_rate)

    def type_effectiveness(self, opponenttype:str):
        # 针对 技能 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponenttype
        if opponent_type == "Grass":
            effectiveness = 0.75
        elif opponent_type == "Water":
            effectiveness = 1.5
        return effectiveness
    def begin(self):
        self.sleep_status = False
        add_layer= len(self.damage_history)-self.layer
        while self.layer < 4 and add_layer > 0:
            self.fire_attribute()
            add_layer -= 1
    #火属性特性：每次造成伤害，攻击力提升 10%
    def fire_attribute(self):
        self.attack += self.attack * 0.15
        self.layer += 1
        print(f"{self} 触发火属性特性,攻击力提升 15%,当前攻击力: {self.attack} 层数: {self.layer}")
        self.skills = self.initialize_skills()


class WaterPokemon(Pokemon):
    type = "Water"

    def __init__(self, num: int, owner: int, operator: str, hp: int, attack: int, defense: int, miss_rate: int):
        super().__init__(num, owner, operator, hp, attack, defense, miss_rate)

    def type_effectiveness(self, opponenttype:str):
        effectiveness = 1.0
        opponent_type = opponenttype

        if opponent_type == "Fire":
            effectiveness = 0.6
        elif opponent_type == "Electric":
            effectiveness = 1.5
        effectiveness *= self.water_attribute()
        return effectiveness

    def begin(self):
        self.sleep_status = False
    def water_attribute(self):
        # 水属性特性：受到伤害时有 50% 的几率 减免 30% 的伤害
        if random.randint(1, 100) <= 50:
            print(f"{self} 触发水属性特性 减免了 30% 的伤害")
            return 0.7
        else:
            return 1.0

class PhysicalPokemon(Pokemon):
    type = "Physical"

    def __init__(self, num: int, owner: int, operator: str, hp: int, attack: int, defense: int, miss_rate: int):
        super().__init__(num, owner, operator, hp, attack, defense, miss_rate)
        self.attack0 = attack
        self.agility = False
        self.miss_rate0 = miss_rate
        self.re = True
    def set_agility(self,x:bool):
        self.agility = x

    def type_effectiveness(self, opponenttype:str):
        effectiveness = 1.0
        opponent_type = opponenttype

        if opponent_type == "Grass":
            effectiveness = 0.7
        elif opponent_type == "Fire":
            effectiveness = 1.1
        elif opponent_type == "Water":
            effectiveness = 1.2
        elif opponent_type == "Electric":
            effectiveness = 1.2
        return effectiveness
    def begin(self):
        self.sleep_status = False
        self.skills = self.initialize_skills()
        self.physical_attribute()
        self.re = True


    def physical_attribute(self):
        # 物理属性特性:攻击力加成已损失生命值的15% ,防御力为已损失生命值的 10%
        self.defense = (self.max_hp-self.hp) * 0.3
        self.attack = self.attack0 + (self.max_hp-self.hp) * 0.14
        print(f"{self} 触发物理属性特性,攻击力加成已损失生命值的 14%,防御力是已损失生命值的 30%,当前攻击力: {self.attack},防御力: {self.defense}")
    def receive_damage(self, damage:float,type1:str,ignoore_defense:bool=False):
        # 计算伤害并减去防御力，更新 HP
        if not self.alive:
            return 0
        if not isinstance(damage, int):
            damage = int(damage)
        # 计算属性克制
        effectiveness = self.type_effectiveness(type1)
        damage *= effectiveness
        # 计算伤害减免
        if not ignoore_defense:
            damage -= self.defense
            if damage <= 0:
                print(f"{self}的防御力抵消了所有伤害! 当前HP: {self.hp}/{self.max_hp}")
                damage = 0

        x=self.hp -1
        self.hp -= damage

        if self.hp <= 0:
            if self.re:
                self.re = False
                self.hp = 1

                print(f"{self} 触发一线生机,锁死 1HP! ")
                return x
            else:
             self.alive = False
             self.hp=0

        return damage




# Bulbasaur 类，继承自 GrassPokemon
class Bulbasaur(GrassPokemon):
    name = "妙蛙种子"

    def __init__(self, num, owner,operator, hp=120, attack=35, defense=2, miss_rate=5) -> None:
        # 初始化 Bulbasaur 的属性
        super().__init__(num, owner,operator, hp, attack, defense, miss_rate)
    def __str__(self) -> str:
        return self.owner_id
    def initialize_skills(self):
        # 初始化技能，具体技能是 SeedBomb 和 ParasiticSeeds
        a = self.attack*1.2
        return [skills.SeedBomb(damage=a), skills.ParasiticSeeds()]

class Pikachu(ElectricPokemon):
    name = "皮卡丘"

    def __init__(self, num, owner,operator, hp=75, attack=35, defense=6, miss_rate=35) -> None:
        super().__init__(num, owner,operator, hp, attack, defense, miss_rate)
    def __str__(self) -> str:
        return self.owner_id
    def initialize_skills(self):
        # 初始化技能，具体技能是 Thunderbolt 和 Quick Attack
        a = self.attack*1.3
        b = self.attack*1.2
        return [skills.ThunderBolt(damage=a), skills.Quick_Attack(damage=b)]


class Charmander(FirePokemon):
    name = "小火龙"
    type = "Fire"

    def __init__(self, num, owner,operator, hp=90, attack=30, defense=9, miss_rate=10) -> None:
        super().__init__(num, owner,operator, hp, attack, defense, miss_rate)


    def __str__(self) -> str:
        return self.owner_id
    def initialize_skills(self):
        # 初始化技能，具体技能是 Ember 和 Flame_Charge
        a = self.attack*1.2
        b = self.attack*2.35
        return [skills.Ember(damage=a),skills.Flame_Charge(damage=b)]#





class Squirtle(WaterPokemon):
    name = "杰尼龟"
    type = "Water"
    def __init__(self, num, owner,operator, hp=110, attack=28, defense=15, miss_rate=18) -> None:
        super().__init__(num, owner,operator, hp, attack, defense, miss_rate)

    def __str__(self) -> str:
        return self.owner_id
    def initialize_skills(self):
        # 初始化技能，具体技能是 Water_Gun 和 BubbleBeam
        a = self.attack*1.0+self.hp*0.15
        b = self.attack*0
        return [skills.Aqua_Jet(damage=a), skills.Shield(defence=b)]
    def begin(self):
        self.sleep_status = False
        self.skills = self.initialize_skills()

    def type_effectiveness(self, opponenttype:str):
        effectiveness = 1.0
        opponent_type = opponenttype

        if opponent_type == "Fire":
            effectiveness = 0.7
        elif opponent_type == "Electric":
            effectiveness = 2.0
        effectiveness *= self.water_attribute()
        if self.protected:
            effectiveness *= 0.35
            print(f"{self} 有护盾,受到伤害降低 35%")
        return effectiveness


class Farfetchd(PhysicalPokemon):
    name = "大葱鸭"
    type = "Physical"
    def __init__(self, num, owner,operator, hp=95, attack=30, defense=0, miss_rate=10) -> None:
        super().__init__(num, owner,operator, hp, attack, defense, miss_rate)
        self.defense0 = defense
        self.re =True

    def __str__(self) -> str:
        return self.owner_id

    def initialize_skills(self):
        #air slash ,Agility
        a = self.attack*1.35
        b = int((self.max_hp-self.hp)*0.45 +20)
        return [skills.Air_Slash(damage=a),skills.Agility(amount=b)]
    def miss_compute(self, opponent: Pokemon,ignore_miss_rate: int = 0,):

        if self.sleep_status == False and  random.randint(1, 100) <= self.miss_rate - ignore_miss_rate :
            if self.agility:
                print(f"{self}闪避了攻击! ")
                self.Farfetchd_attribute(opponent)
            return True
        else:
            if self.agility:
                self.defense += 3
                print(f"{self}没有成功闪避攻击! 添加临时防御 3 点! 当前防御力: {self.defense}")
                self.Farfetchd_attribute(self)

            return False

    def begin(self):
        self.sleep_status = False
        self.skills = self.initialize_skills()
        self.defense = self.defense0
        self.physical_attribute()


    # 电属性特性：闪避成功，发动技能
    def Farfetchd_attribute(self, opponent: Pokemon):
        self.use_skill(skills.Agility_Execute(opponent.attack*0.3),opponent)









