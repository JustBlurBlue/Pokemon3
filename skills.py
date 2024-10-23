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


        if not opponent.miss_compute(user):
            # 给使用者添加治疗效果
            opponent.add_status_effect(effects.parasitism("寄生种子",user,3),1)
            print(f"{opponent} 被 {user} 寄生了!")

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

                opponent.add_status_effect(effects.FireEffect(self.name, 15, 2), 1)
                print(f"{opponent.name} 被 {self.name} 施加了灼烧！")
            else:
                print(f"{self.name} 没有使 {opponent} 灼烧！")
        return True_damage

class Flame_Charge(Skill) :
    name = "蓄能爆炎"
    type = "Fire"
    def __init__(self,damage:float,activation_chance: int = 90)->None:
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
    def __init__(self,damage:float,activation_chance: int = 90)->None:
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
                opponent.add_status_effect(effects.FireEffect(self.name, 25, 2), 1)
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

class Air_Slash(Skill) :
    name = "空气斩"
    type = "Physical"
    def __init__(self,damage:float)->None:
        super().__init__()
        self.damage = damage

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> float:
        True_damage = 0
        if not opponent.miss_compute(user, ignore_miss_rate=-5):
            True_damage = opponent.receive_damage(self.damage, self.type, False)
            print(
                f"{opponent} 受到了 {True_damage} 点伤害！ 剩余生命值: {opponent.hp}/{opponent.max_hp}"
            )
        else:
            True_damage = opponent.receive_damage(self.damage*0.8, self.type, False)
            print(
                f"{opponent} 因剑气受到了 {True_damage} 点伤害！ 剩余生命值: {opponent.hp}/{opponent.max_hp}"
            )
        user.receive_damage(self.damage * 0.15, self.type, True)
        print(
            f"{user} 因空气斩力量过大受到了 {self.damage * 0.15} 点伤害！ 剩余生命值: {user.hp}/{user.max_hp}"
        )
        return True_damage


class Agility(Skill) :
    name = "高速星星"
    type = "Physical"
    def __init__(self,amount:int)->None:
        super().__init__()
        self.amount = amount

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> float:
        user.set_Agility(True)
        for i in user.statuses_defence:
            if i.name == "高速星星":
                user.statuses_defence.remove(i)
        user.add_status_effect(effects.Agility(self.name, self.amount, 2), 3)
        print(f"{user} 的闪避率变为了 {self.amount} !")
        user.set_miss_rate(self.amount)

        return -1

class Agility_Execute(Skill) :
    name = "高速星星"
    type = "Physical"
    def __init__(self,amount:float)->None:
        super().__init__()
        self.amount = amount

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> float:

        if opponent == user:
            True_damage = opponent.receive_damage(self.amount, self.type)
            print(f"处于高速星星状态,{user}对{opponent}造成{True_damage}点伤害! {opponent} 剩余HP值: {opponent.hp}/{opponent.max_hp}")
        else:
            True_damage = opponent.receive_damage(self.amount, self.type, True)
            print(f"处于高速星星状态,{user}对{opponent}造成{True_damage}点伤害! {opponent} 剩余HP值: {opponent.hp}/{opponent.max_hp}")

        return True_damage
