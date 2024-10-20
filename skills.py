import random
from typing import TYPE_CHECKING
import effects

if TYPE_CHECKING:
    from pokemon import Pokemon


class Skill:
    name: str
    type: str

    def __init__(self) -> None:
        pass

    def execute(self, user: "Pokemon", opponent: "Pokemon"):
        raise NotImplementedError
    def execute2(self, user: "Pokemon", opponent: "Pokemon"):
        pass
    def __str__(self) -> str:
        return f"{self.name}"



class SeedBomb(Skill):
    name = "种子炸弹"
    type = "Grass"

    def __init__(self, damage: float, activation_chance: int = 15) -> None:
        super().__init__()
        self.damage = damage
        self.activation_chance = activation_chance  # 确保激活几率被正确初始化

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> float:
        # 造成伤害
        True_damage =0
        if not opponent.miss_compute(user):
            True_damage = opponent.receive_damage(self.damage,self.type,False)
            print(
                f"{opponent} 受到了 {True_damage} 点伤害！ 剩余生命值: {opponent.hp}/{opponent.max_hp}"
            )

            # 判断是否触发状态效果
            if random.randint(1, 100) <= self.activation_chance:
                opponent.add_status_effect(effects.PoisonEffect("种子炸弹",10,3),1)
                print(f"{opponent.name} 被 {self.name}施加了中毒！")
            else:
                print(f"{self.name} 没有使 {opponent} 中毒！")
        return True_damage



class ParasiticSeeds(Skill):
    name = "寄生种子"

    def __init__(self) -> None:
        super().__init__()


    def execute(self, user: "Pokemon", opponent: "Pokemon") -> float:
        self.amount = opponent.max_hp / 8

        if not opponent.miss_compute(user):
            # 给使用者添加治疗效果
            opponent.add_status_effect(effects.PoisonEffect("寄生种子",self.amount,3),1)
            print(f"{opponent} 被 {user} 寄生,产生中毒效果!")
            # 给对手添加中毒效果
            user.add_status_effect(effects.HealEffect("寄生种子",self.amount,3),1)
        return -1


class ThunderBolt(Skill):
    name = "十万伏特"
    type = "Electric"
    def __init__(self,damage:float,activation_chance: int = 15)->None:
        super().__init__()
        self.damage = damage
        self.activation_chance = activation_chance

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> float:
        True_damage=0
        if not opponent.miss_compute(user):
            True_damage = opponent.receive_damage(self.damage,self.type,False)
            print(
                f"{opponent} 受到了 {True_damage} 点伤害！ 剩余生命值: {opponent.hp}/{opponent.max_hp}"
            )
            if random.randint(1, 100) <= self.activation_chance:
                opponent.add_status_effect(effects.SleepEffect("十万伏特", duration=1,amount=self.damage),2)
                opponent.set_sleep(True)
                print(f"{opponent} 因 {self.name} 被麻痹了 1 回合!")
        return True_damage


class Quick_Attack(Skill):
    name = "电光一闪"
    type = "Electric"
    def __init__(self,damage:float,activation_chance: int = 18)->None:
        super().__init__()
        self.damage = damage
        self.activation_chance = activation_chance

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> float:
        True_damage=0
        True_damage2 = 0
        True_damage1 = 0
        if not opponent.miss_compute(user):
            True_damage1 = opponent.receive_damage(self.damage, self.type, False)
            print(
                f"{opponent} 受到了 {True_damage1} 点伤害！ 剩余生命值: {opponent.hp}/{opponent.max_hp}"
            )


            if random.randint(1, 100) <= self.activation_chance:
                print(f"电光一闪 2 段 成功发动!")
                if not opponent.miss_compute(user,ignore_miss_rate=7):
                    True_damage2 = opponent.receive_damage(self.damage*0.8, self.type, True)
                    print(
                        f"{opponent} 受到了 {True_damage2} 点伤害！ 剩余生命值: {opponent.hp}/{opponent.max_hp}"
                    )
            else:
                print(f"电光一闪 2 段 发动失败!")

        True_damage += True_damage1
        True_damage += True_damage2
        return True_damage



class Ember(Skill):
    name = "火花"
    type = "Fire"
    def __init__(self,damage:float,activation_chance: int = 12)->None:
        super().__init__()
        self.damage = damage
        self.activation_chance = activation_chance

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> float:
        True_damage=0
        if not opponent.miss_compute(user):
            True_damage = opponent.receive_damage(self.damage, self.type, False)

            print(
                f"{opponent} 受到了 {True_damage} 点伤害！ 剩余生命值: {opponent.hp}/{opponent.max_hp}"
            )
            if random.randint(1, 100) <= self.activation_chance:

                opponent.add_status_effect(effects.FireEffect(self.name, 13, 2), 1)
                print(f"{opponent.name} 被 {self.name} 施加了灼烧！")
            else:
                print(f"{self.name} 没有使 {opponent} 灼烧！")
        return True_damage

class Flame_Charge(Skill) :
    name = "蓄能爆炎"
    type = "Fire"
    def __init__(self,damage:float,activation_chance: int = 80)->None:
        super().__init__()
        self.damage = damage
        self.opponent = None
        self.activation_chance = activation_chance
        self.user = None
    def execute(self, user: "Pokemon", opponent: "Pokemon") -> float:
        self.opponent = opponent
        self.user = user
        user.set_preparing( Flame_Charge_Execute(self.damage,self.activation_chance), True,opponent)
        user.set_miss_rate(35)
        print(f"{user.name} 开始蓄力 蓄能爆炎!")
        return -1


class Flame_Charge_Execute(Skill) :
    name = "蓄能爆炎"
    type = "Fire"
    def __init__(self,damage:float,activation_chance: int = 80)->None:
        super().__init__()
        self.damage = damage
        self.activation_chance = activation_chance
    def execute(self, user: "Pokemon", opponent: "Pokemon")->float:
        True_damage=0
        if not opponent.miss_compute(user):
            True_damage = opponent.receive_damage(self.damage, self.type, False)
            print(
                f"{opponent} 受到了 {True_damage} 点伤害！ 剩余生命值: {opponent.hp}/{opponent.max_hp}"
            )
            if random.randint(1, 100) <= self.activation_chance:
                opponent.add_status_effect(effects.FireEffect(self.name, 15, 2), 1)
                print(f"{opponent.name} 被 {self.name} 施加了灼烧！")
            else:
                print(f"{self.name} 没有使 {opponent} 灼烧！")

        user.set_preparing(None,False,None)
        user.set_miss_rate(10)
        return True_damage


class Aqua_Jet(Skill) :
    name = "水枪"
    type = "Water"
    def __init__(self,damage:float,activation_chance: int = 10)->None:
        super().__init__()
        self.damage = damage
    def execute(self, user: "Pokemon", opponent: "Pokemon") -> float:
        True_damage = 0
        if not opponent.miss_compute(user):
            True_damage = opponent.receive_damage(self.damage, self.type, False)
            print(
                f"{opponent} 受到了 {True_damage} 点伤害！ 剩余生命值: {opponent.hp}/{opponent.max_hp}"
            )
        return True_damage


class Shield(Skill) :
    name = "护盾"
    type = "Water"
    def __init__(self,defence:float)->None:
        super().__init__()
        self.defence = defence
    def execute(self, user: "Pokemon", opponent: "Pokemon") -> float:
        user.set_proptected(True)
        user.add_status_effect(effects.Shield(self.name, self.defence, 2), 3)
        return -1
