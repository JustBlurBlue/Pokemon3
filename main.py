from __future__ import annotations
from pokemon import Pokemon, Bulbasaur, Pikachu, Charmander, Squirtle, Farfetchd
from Ways import *
import random
###宝可梦词典
pokemon_dict = {"1": Bulbasaur,"2":Pikachu,"3":Charmander,"4":Squirtle,"5":Farfetchd}
##定义玩家类
class Player:
    def __init__(self, operater: str, num: int, pokemonlist: list[Pokemon]):
        self.operater = operater
        self.Num = num+1
        self.pokemonlist_live = pokemonlist
        self.alive = True
        self.current_pokemon = int()
        self.index = num
        self.pokemonlist_dead = []
        self.opr = False
    #以字符串形式输出时  ：玩家在list中的下标+1       （玩家的操作者）
    def __str__(self)->str:
        return 'P'+str(self.Num)+f'({self.operater})'
    #输出玩家的活着的宝可梦
    def print_pokemon(self)->None:
        for i in self.pokemonlist_live:
            print(f"{i.index+1}.{i},属性：{i.type}")
    #切换当前宝可梦，并输出。参数是选择的宝可梦的下标
    def change_current_pokemon(self, index: int)->None:
        self.current_pokemon = index
        print(f"{self},就是你了,{self.pokemonlist_live[index]}")
    #玩家使用技能？？
    def use_skill_p(self):
        pass
    #改变宝可梦列表--有宝可梦死亡时调用（参数应为死亡的宝可梦），需要改变live列表，以及后方的index
    def change_pokemon_list(self,pokemon):
        self.pokemonlist_live.remove(pokemon)
        self.pokemonlist_dead.append(pokemon)
        for i in self.pokemonlist_live:
            if i.index > pokemon.index:
                i.change_index()
    #改变玩家的index，其他玩家阵亡时调用，参数是阵亡玩家
    def change_index(self):
        self.index -= 1
    #选择宝可梦
    def choose_pokemon(self) :
        for i in pokemon_dict:
            print(f"{i}.{pokemon_dict[i].__name__}")
        if self.operater != "PC":
            choose = input_check(f"P{self.Num}({self.operater})请选择3个宝可梦用于组成你的队伍:")
        else:
            print(f"P{self.Num}({self.operater})请选择3个宝可梦用于组成你的队伍:")
            choose = str(self.random(len(pokemon_dict),1)) + " "+ str(self.random(len(pokemon_dict),1))+" "+str(self.random(len(pokemon_dict),1))         #'''pc_rad(3)'''待接入随机数生成器
        list_c = choose.strip().split()[:3]  ###限制输入3个宝可梦,后续无效
        num = 0  ###宝可梦编号

        for x in list_c:
            pokemonx = pokemon_dict[x](num, self.Num,self.operater)
            self.pokemonlist_live.append(pokemonx)
            num += 1
        print(f"{self}选择的宝可梦为:")
        self.print_pokemon()
    #随机数生成器--PC专属（参数是最大值）
    def random(self,num2,num1=0):
        return random.randint(num1,num2)
    #设置玩家生死
    def set_dead(self)->None:
        self.alive = False
    def set_opr(self,x:bool)->None:
        self.opr = x


###初始化玩家宝可梦###选择宝可梦




###初始化玩家与宝可梦
def init_player() -> list[Player]:
    playerlist = []
    ###输入玩家数量
    players = input_check("请输入玩家 PC的数量:")
    pc = int(players.split()[1])
    human = int(players.split()[0])
    #playernum = pc + human
    ###初始化玩家
    for i in range(human):
        player =Player(input_check(f"P{i+1},请输入你的名称:"), i, [])
        playerlist.append(player)
        print(f"P{player.Num}({playerlist[player.index].operater})初始化成功")
    ###初始化PC
    for i in range(pc):
        player =Player("PC", i+human, [])
        playerlist.append(player)
        print(f"P{player.Num}({playerlist[player.index].operater})初始化成功")
    ###初始化宝可梦
    for i in playerlist:
        i.choose_pokemon()
    return playerlist

PlayerList = init_player()


class Play:
    def __init__(self, playerlist: list[Player]):
        self.playerlist = playerlist
        self.round = 0
        self.playerlist_dead = []
        self.all_num = len(playerlist)
        self.happened = False
    #打印玩家信息
    def print_players(self,index):
        for i in self.playerlist:
            if i.index != index:
                try:
                    print(f"{i.index+1}.{i},当前宝可梦：{i.pokemonlist_live[i.current_pokemon]}")
                except:
                    pass

    #初始选择宝可梦
    def init_select_pokemon(self):
        for i in self.playerlist:
            print_departure()
            i.print_pokemon()
            if i.operater != "PC":
                i.change_current_pokemon(int(input_check(f"{i})请选择你要使用的宝可梦:"))-1)
            else:
                i.change_current_pokemon(i.random(len(i.pokemonlist_live) - 1))
    #检查玩家是否阵亡，如果阵亡，则加入dead列表，从playerlist中删除,并调用 change_index 改变index，返回False，否则返回True
    def check_player(self, player):
        if len(player.pokemonlist_live) == 0:
            print(f"{player}失去了所有宝可梦，输了")
            self.playerlist_dead.append(player)
            self.playerlist.remove(player)
            player.set_dead()
            self.check_game()
            for i in self.playerlist:
                if i.index >= player.index:
                    i.change_index()
            return False
        return True
    #检查宝可梦是否阵亡，如果阵亡，则从live列表中删除，并加入dead列表  ,然后检查玩家宝可梦列表是否为空
    def check_pokemon_alive(self, player, pokemon):
        if pokemon.hp <= 0:
            print(f"{pokemon} 陷入昏厥")
            player.change_pokemon_list(pokemon)
            if  len(player.pokemonlist_live) != 0:
                self.dead_select_pokemon(player)
            return False
        return True
    def check_pokemon_alive_none(self, pokemon):
        if pokemon.hp <= 0:
            return False
        return True
    #开始游戏
    #检查游戏是否结束
    def check_game(self)->bool:
        if len(self.playerlist) == 1:
            print(f"{self.playerlist[0]}胜利")
            return True
        elif  len(self.playerlist) == 0:
            print(f"{self.playerlist_dead[self.all_num-1]}与玩家{self.playerlist_dead[self.all_num-2]}平局")
            return True
        else:
            return False
    def check_game_none(self)->bool:
        if len(self.playerlist) == 1:
            return True
        elif  len(self.playerlist) == 0:
            return True
        else:
            return False
    #阵亡选定
    def dead_select_pokemon(self, player: Player):
        player.print_pokemon()
        print(f"{player}你的宝可梦昏厥了，请选择宝可梦:")
        if player.operater != "PC":
            choose = input_check(f"{player})请选择你要使用的宝可梦:")
            choose =int(choose) - 1
        else:
            choose = player.random(len(player.pokemonlist_live) - 1)
        player.change_current_pokemon(choose)
    #效果结算与被动结算
    def round_s_effect(self):
        print("被动结算")
        for i in range(len(self.playerlist)):

            self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].begin()
            self.check_pokemon_alive(self.playerlist[i], self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon])


            if not self.check_player(self.playerlist[i]):
                return False
            print("-")
        print("-----")
        print("效果结算")
        for i in range(len(self.playerlist)):

            self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].apply_status_effect_begin()
            self.check_pokemon_alive(self.playerlist[i], self.playerlist[i].pokemonlist_live[
            self.playerlist[i].current_pokemon])

            if not self.check_player(self.playerlist[i]):
                return False
            print("-")
            if not self.check_player(self.playerlist[i]):
                return False
            print("-")
        return True
    #玩家操作
    def round_use_skill(self,i)->int:
        self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].fresh_skill()

        self.print_players(self.playerlist[i].index)
        if self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].preparing:
            print(f"{self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon]}: 蓄力完成")
            #请确认目标
            print(f"你先前选择的目标是: {self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].preparing_opponent}")
            if not self.check_pokemon_alive_none(self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].preparing_opponent):
                print("目标已阵亡，请重新选择")
            if self.playerlist[i].operater != "PC":
                choose_p = input_check(f"{self.playerlist[i]}:确认你要攻击的目标:")
                choose_p = int(choose_p) - 1
            else:
                choose_p = self.playerlist[i].random(len(self.playerlist) - 1)
                while choose_p == self.playerlist[i].index or self.playerlist[i].alive == False:
                    choose_p = self.playerlist[i].random(len(self.playerlist) - 1)
            target_player = self.playerlist[choose_p]
            print(f"{self.playerlist[i]}选择了{target_player}作为目标！")
            self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].use_skill(self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].preparing_skill,target_player.pokemonlist_live[target_player.current_pokemon] , True)
            self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].preparing = False
        else:
            if self.playerlist[i].operater != "PC":
                choose_p = input_check(f"{self.playerlist[i]}:请选择你要攻击的目标:")
                choose_p = int(choose_p) - 1
            else:
                choose_p = self.playerlist[i].random(len(self.playerlist) - 1)
                while choose_p == self.playerlist[i].index or self.playerlist[i].alive == False:
                    choose_p = self.playerlist[i].random(len(self.playerlist) - 1)
            target_player = self.playerlist[choose_p]
            print(f"{self.playerlist[i]}选择了{target_player}作为目标！")
            # 选择技能
            self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].print_skills()
            if self.playerlist[i].operater != "PC":
                choose = input_check(f"{self.playerlist[i]}:请选择你要使用的技能:")
                choose = int(choose) - 1
            else:
                choose = self.playerlist[i].random(
                    len(self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].skills) - 1)
            skill = self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].skills[choose]

            # 技能效果

            self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].use_skill(
                skill,
                self.playerlist[choose_p].pokemonlist_live[self.playerlist[choose_p].current_pokemon]
            )



        # 刷新技能
        self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].fresh_skill()
        self.playerlist[choose_p].pokemonlist_live[self.playerlist[choose_p].current_pokemon].fresh_skill()
        return choose_p


    def round_s(self,x,y,shunxu):

        for i in range(x,y,shunxu):
            #是否操作过了
            if  not self.playerlist[i].opr :
                # 设置玩家为操作过
                self.playerlist[i].set_opr(True)
                choose_p = -1
                # 应用于技能使用前的效果
                self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].apply_status_effect_use_skills()
                print(
                    f"轮到{self.playerlist[i]}进行操作，你当前的宝可梦是 {self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon]}")

                # 判断是否被麻痹
                if self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].sleep_status:
                    print(f"{self.playerlist[i]}被麻痹了，无法行动")

                else:
                    choose_p = self.round_use_skill(i)
                    self.playerlist[i].set_opr(True)

                    ###判断是否死亡,如果死亡，则返回 False
                    # 检测攻击对象是否死亡
                    # 应用于技能使用前的效果
                if self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].alive:
                    self.playerlist[i].pokemonlist_live[self.playerlist[i].current_pokemon].apply_status_effect_defence()
                if choose_p != -1:

                    self.check_pokemon_alive(self.playerlist[choose_p], self.playerlist[choose_p].pokemonlist_live[
                        self.playerlist[choose_p].current_pokemon])
                    self.check_pokemon_alive(self.playerlist[i], self.playerlist[i].pokemonlist_live[
                        self.playerlist[i].current_pokemon])
                    x = self.check_player(self.playerlist[i])
                    if not x and choose_p > i:
                        choose_p -= 1
                    y = self.check_player(self.playerlist[choose_p])
                    if (not y or not x):
                        return False


        return True




    def run(self):
        while True:
            #检查点1
            if self.check_game_none():
                sys.exit()
            self.round += 1
            print_departure()
            if self.round == 1:
                print("游戏开始")
                self.init_select_pokemon()
            #检查点2
            if self.check_game_none() :
                sys.exit()
            else:
                if self.round != 1:
                    self.happen = False
                    while not self.happen:
                        #检查点3
                        if self.check_game_none():
                            sys.exit()
                        self.happen = self.round_s_effect()
            #检查点4
            if self.check_game_none():
                sys.exit()
            else:
                print_departure()
                print(f"第{self.round}回合开始")
                print_departure()
                for i in self.playerlist:
                    i.set_opr(False)
                self.happen = False
                while not self.happen:
                    #检查点5
                    if self.check_game_none():
                        sys.exit()
                    #如果是奇数回合，则从左到右，否则从右到左
                    if self.round % 2 == 0:
                        self.happen = self.round_s( len(self.playerlist)-1,-1,-1)
                    else:
                        self.happen = self.round_s(0,len(self.playerlist), 1)




if __name__ == '__main__':
    play1 = Play(PlayerList)
    play1.run()


play=Play(PlayerList)
play.init_select_pokemon()
