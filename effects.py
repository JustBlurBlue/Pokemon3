from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pokemon import Pokemon, PhysicalPokemon


class Effect:
    name: str
    type: str
    def __init__(self, duration: int) -> None:
        # 初始化效果持续时间
        self.duration = duration

    def apply(self, pokemon: "Pokemon") -> None:
        # 应用效果的抽象方法，子类需要实现
        raise NotImplementedError

    def decrease_duration(self) -> None:
        # 减少效果持续时间
        self.duration -= 1
        if self.duration <= 0:
            pass
        else:
            print(f"{self.name} 效果持续时间减少了. 剩余: {self.duration}")


class PoisonEffect(Effect):
    name = "中毒"
    type = "毒"#使其没有属性,保障伤害

    def __init__(self, skill_name:str, damage: float , duration: int = 3) -> None:
        super().__init__(duration)
        self.damage = damage
        self.skill_name = skill_name


    def apply(self, pokemon: "Pokemon") -> None:
        Ture_damage =pokemon.receive_damage(self.damage,self.type,True)
        print(f"{pokemon} 因 {self.skill_name} 受到了 {Ture_damage} 点中毒伤害!, 当前HP: {pokemon.hp}/{pokemon.max_hp}")


class parasitism(Effect):
    name = "寄生"
    type = None
    def __init__(self, skill_name:str,para: "Pokemon", duration: int = 3) -> None:
        super().__init__(duration)

        self.skill_name = skill_name
        self.para = para
    def apply(self, pokemon: "Pokemon") -> None:
        damage = pokemon.hp/8
        Ture_damage =pokemon.receive_damage(damage,self.type,True)
        print(f"{pokemon} 因 {self.skill_name} 受到了 {Ture_damage} 点寄生伤害!, 当前HP: {pokemon.hp}/{pokemon.max_hp}")
        if self.para.alive:
            self.para.heal_self(Ture_damage)
            print(f"{self.para} 从 {pokemon} 吸取了 {Ture_damage} 点HP! 当前HP: {self.para.hp}/{self.para.max_hp}")



class HealEffect(Effect):
    name = "治疗"

    def __init__(self,skill_name:str, amount: float, duration: int ) -> None:
        super().__init__(duration)
        self.amount = amount
        self.skill_name = skill_name
    def apply(self, pokemon: "Pokemon") -> None:
        pokemon.heal_self(self.amount)
        print(f"{pokemon} 用 {self.skill_name} 治疗了自己 {self.amount} 点HP!当前HP: {pokemon.hp}/{pokemon.max_hp}")


class SleepEffect(Effect):
    name = "麻痹"
    type = "Electric"
    def __init__(self,skill_name:str, amount: float, duration: int ) -> None:
        super().__init__(duration)
        self.amount = amount
        self.skill_name = skill_name
    def apply(self, pokemon: "Pokemon") -> None:
        # 每次应用时都把麻痹状态设置成True
        pokemon.set_sleep(True)
        pokemon.set_preparing(None,False,None)
        #如果持续时间小于1，则麻痹状态结束
        if self.duration < 1:
            pokemon.set_sleep(False)

class FireEffect(Effect):
    name = "灼烧"
    type = "Fire"
    def __init__(self,skill_name:str, amount: float, duration: int ) -> None:
        super().__init__(duration)
        self.amount = amount
        self.skill_name = skill_name

    def apply(self, pokemon: "Pokemon") -> None:
        Ture_damage = pokemon.receive_damage(self.amount+pokemon.hp/10.0, self.type, True)
        print(f"{pokemon} 因 {self.skill_name} 受到了 {Ture_damage} 点灼烧伤害!, 当前HP: {pokemon.hp}/{pokemon.max_hp}")
'''
class PreparingEffect(Effect):
    name = "蓄力"
    type = "None"
    def __init__(self,skill_name:str, amount: float, duration: int ) -> None:
        super().__init__(duration)
        self.amount = amount
        self.skill_name = skill_name
    def apply(self, user: "Pokemon") -> None:
        # 每次应用时都把蓄力状态设置成True
        user.set_preparing(True)
        #如果持续时间小于1，则蓄力状态结束
        if self.duration < 1:
            user.set_preparing(False)
            print(f"{user} 蓄力状态结束!")
            # 蓄力状态结束时，对目标进行攻击'''

class Shield(Effect):
    name = "护盾"
    type = "Water"
    def __init__(self,skill_name:str, amount: float, duration: int ) -> None:
        super().__init__(duration)
        self.amount = amount
        self.skill_name = skill_name
    def apply(self, pokemon: "Pokemon") -> None:
        # 每次应用时都把护盾状态设置成True
        pokemon.set_proptected(True)
        #如果持续时间小于1，则护盾状态结束
        if self.duration < 1:
            pokemon.set_proptected(False)
            print(f"{pokemon} {self.name} 效果结束!")

class Agility(Effect):
    name = "高速星星"
    type = "Physical"
    def __init__(self,skill_name:str, amount: int, duration: int ) -> None:
        super().__init__(duration)
        self.amount = amount
        self.skill_name = skill_name
    def apply(self, pokemon: "PhysicalPokemon") -> None:
        # 每次应用时都把高速状态设置成True
        pokemon.set_agility(True)

        #如果持续时间小于1，则高速状态结束
        if self.duration < 1:
            pokemon.set_agility(False)
            pokemon.set_miss_rate(pokemon.miss_rate0)
            print(f"{pokemon} {self.name} 效果结束!,闪避率恢复为 {pokemon.miss_rate0} !")