import random
import os

#################
# Configuration #
#################

id_card = { # ID da carta : ['Nome da carta', Preço, ação extra 1, ação extra 2...]
    # -2 = id para terceira ação
    -2 : ['KillByHands', 8],
    # -1 = id de carta morta
    -1 : ['', 0],
    0 : ['Kamikaze', 0],
    1 : ['Paladina', 5],
    2 : ['Assassino', 4],
    3 : ['Coveiro', 6],
    4 : ['Bufão', 2],
    # preço = juros | ação extra 1 = valor de serpentes pegas no round
    5 : ['Duque', 0, 4],
    6 : ['Condessa', 0],
    #ação extra 1 = valor recebido ao aumentar os preços
    7 : ['Marquês', 0, 1],
    #ação extra 1 = valor retirado do inimigo
    8 : ['Traira', 0, 2],
    #ação extra 1 = valor reduzido dos preços
    9 : ['Rebelde', 1, 1],
}

Total_Cards = len(id_card) -  2
silver_initial = 8
probability = [0,0,0,0,1]

def VerifyDupCards():
    if player1.CardsInHand[1] == player1.CardsInHand[0]:
        player1.CardsInHand[1] = random.randrange(Total_Cards)
        VerifyDupCards()
    if IAplayer.CardsInHand[1] == IAplayer.CardsInHand[0]:
        IAplayer.CardsInHand[1] = random.randrange(Total_Cards)
        VerifyDupCards()

class player:
    def __init__(self):
        self.CardsInHand = [random.randrange(Total_Cards) for card in range(2)]
        self.SilverSerpents = silver_initial
        self.debt = [9]
        self.angry_duke = False

class IA():
    def __init__(self):
        self.CardsInHand = [random.randrange(Total_Cards) for card in range(2)]
        self.SilverSerpents = silver_initial
        self.debt = []
        self.angry_duke = False

    def IAdecision(self):
        if random.choice(probability) == 1:
            return True
        else:
            return False

#EnableIA = input('Bem vindo ao HoodWink, Gostaria de jogar com a IA? Sim (1) ou não (0)?')

#if EnableIA == 1:
#   IAplayer = IA()

player1, IAplayer = player(), IA()
VerifyDupCards()
os.system('cls')

####################
# Game Starts Here #
####################

Ia_use_this = []

def player1_round():
    os.system('cls')
    demand_debt()
    os.system('cls')
    translated_ids = [id_card[card] for card in player1.CardsInHand]
    if translated_ids[0][0] != '' and translated_ids[1][0] != '': TranslatedHand = f'{translated_ids[0][0]} e {translated_ids[1][0]}'
    elif translated_ids[0][0] == '': TranslatedHand = translated_ids[1][0]
    else: TranslatedHand = translated_ids[0][0]
    print(f'''Você tem em mãos: {TranslatedHand}. E Você tem {player1.SilverSerpents} Serpente(s) de Prata
Seu Adversário tem {IAplayer.SilverSerpents} serpentes de prata.

    O turno é seu! (digite o comando que está entre parenteses, para realizar a ação): 
    Pegar 1 serpentes de prata - (1)

    Pegar 2 serpentes de prata - (2)

    Gastar {id_card[-2][1]} serpentes de pratas para matar uma carta adversária - (3)

    Usar uma habilidade de uma das seguintes cartas:
    Assassino, diz: "A lâmina que não se vê, é a mais mortifera" - (4)  | Preço: {id_card[2][1]}

    Coveiro, diz: "Só mais um pouco e então, descanse" - (5)            | Preço: {id_card[3][1]}

    Traíra, diz:"Um virar de costas merece uma faca" - (6)              | Preço: {id_card[8][1]}

    Marquês, diz: "É necessário aumentar as taxas" - (7)                | Preço: {id_card[7][1]}

    Bufão, diz: "Que tal um truque de mágica?" - (8)                    | Preço: {id_card[4][1]}

    Duque, diz: "Gostaria de um emprestimo?" - (9)                      | Preço por turno: {id_card[5][1]}

    Kamikaze, diz: "Preparar para voar!" - (10)                         | Preço: Uma de suas cartas

    Rebelde, diz: "Vivam a rebelião!" (11)                              | Preço: {id_card[9][1]}

    ''')
    actionPlayer1 = input('Sua ação: ')
    
    if actionPlayer1 == '1':
        os.system('cls')
        player1.SilverSerpents += 1
        input(f'Você pegou 1 serpente de prata. Agora você tem {player1.SilverSerpents} delas!')
        EnemyTurn()
    elif actionPlayer1 == '2':
        if IAplayer.IAdecision() or 'countess' in Ia_use_this:
            if 'countess' not in Ia_use_this: Ia_use_this.append('countess'), probabilityReset()
            contested = input('O adversário útilizou a condessa, você não pegou serpentes de prata. Gostaria de contestar? sim (1), não (0)\nSua ação: ')
            if contested == '1':
                if 6 in IAplayer.CardsInHand:
                    if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                    elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                    else: lostCard = random.choice(player1.CardsInHand)
                    input(f'O adversário tinha a condessa, você perdeu a seguinte carta: {id_card[lostCard][0]}')
                    player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                    if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                        loseGame()
                    else:
                        IAplayer.CardsInHand[IAplayer.CardsInHand.index(6)] == random.randrange(Total_Cards)
                        os.system('cls')
                        print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                        kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                        if kamikaze == '1':
                            if IAplayer.IAdecision():
                                if 0 in player1.CardsInHand:
                                    os.system('cls')
                                    input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                    WinGame()
                                else:
                                    os.system('cls')
                                    input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                    loseGame()
                            else:
                                os.system('cls')
                                notContestedbyIA()
                                witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                    IAplayer.CardsInHand[1] = -1
                                    CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                    if CardInHand != 0:
                                        input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                        EnemyTurn()
                                    else:
                                        WinGame()
                                elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                    IAplayer.CardsInHand[0] = -1
                                    CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                    if CardInHand != 0:
                                        input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                        EnemyTurn()
                                    else:
                                        WinGame()
                                else:
                                    InvalidEntry()
                        elif kamikaze == '0':
                            EnemyTurn()
                        else:
                            InvalidEntry()
                else:
                    os.system('cls')
                    witchCardKill = input(f'O adversário não tem a condessa, qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                    if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                        IAplayer.CardsInHand[1] = -1
                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                        if CardInHand != 0:
                            input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                            if IAplayer.IAdecision() or 'kamikaze' in Ia_use_this: IaUsesKamikaze()
                            EnemyTurn()
                        else:
                            WinGame()
                    elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                        IAplayer.CardsInHand[0] = -1
                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                        if CardInHand != 0:
                            input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                            if IAplayer.IAdecision() or 'kamikaze' in Ia_use_this: IaUsesKamikaze()
                            EnemyTurn()
                        else:
                            WinGame()
                    else:
                        InvalidEntry()
            elif contested == '0':
                EnemyTurn()
            else:
                InvalidEntry()
        else:
            os.system('cls')
            player1.SilverSerpents += 2
            notContestedbyIA()
            input(f'Você pegou 2 serpente de prata. Agora você tem {player1.SilverSerpents} delas!')
            EnemyTurn() 
    elif actionPlayer1 == '3':
        if player1.SilverSerpents >= id_card[-2][1]:
            witchCardKill = input('Qual carta inimiga gostaria de matar? Esquerda (0), Direita (1)\nSua ação: ')
            if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                player1.SilverSerpents -= 8
                if IAplayer.SilverSerpents >= id_card[1][1] and IAplayer.IAdecision() or 'paladin' in Ia_use_this:
                    if 'paladin' not in Ia_use_this: Ia_use_this.append('paladin'), probabilityReset()
                    IAplayer.SilverSerpents -= id_card[1][1]
                    contested = input(f'O adversário usou a paladina por {id_card[1][1]} serpentes de prata, gostaria de contestar? sim (1), não (0)\n Sua ação: ')
                    if contested == '1':
                        if 1 in IAplayer.CardsInHand:
                            if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                            elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                            else: lostCard = random.choice(player1.CardsInHand)
                            input(f'O adversário tinha a paladina, você perdeu a sua carta: {id_card[lostCard]}')         
                            player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                            if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                                loseGame()
                            else:
                                IAplayer.CardsInHand[IAplayer.CardsInHand.index(1)] == random.randrange(Total_Cards)
                                os.system('cls')
                                print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                                kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                                if kamikaze == '1':
                                    if IAplayer.IAdecision():
                                        if 0 in player1.CardsInHand:
                                            os.system('cls')
                                            input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                            WinGame()
                                        else:
                                            os.system('cls')
                                            input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                            loseGame()
                                    else:
                                        os.system('cls')
                                        notContestedbyIA()
                                        witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                        if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                            IAplayer.CardsInHand[1] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                            IAplayer.CardsInHand[0] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        else:
                                            InvalidEntry()
                                elif kamikaze == '0':
                                    EnemyTurn()
                                else:
                                    InvalidEntry()                                
                        else:
                            os.system('cls')
                            input('O adversário não tinha a paladina... Assim, perdendo mais uma carta e o Eliminando do jogo...')
                            WinGame()
                    elif contested == '0':
                        input ('O adversário impediu o ataque')
                        EnemyTurn()
                    else:
                        InvalidEntry()
                else:
                    IAplayer.CardsInHand[1] = -1
                    CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                    if CardInHand != 0:
                        notContestedbyIA()
                        os.system('cls')
                        input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                        if IAplayer.IAdecision() or 'kamikaze' in Ia_use_this: IaUsesKamikaze()
                        EnemyTurn()
                    else:
                        WinGame()
            elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                player1.SilverSerpents -= 8
                if IAplayer.SilverSerpents >= id_card[1][1] and IAplayer.IAdecision() or 'paladin' in Ia_use_this:
                    if 'paladin' not in Ia_use_this: Ia_use_this.append('paladin'), probabilityReset()
                    IAplayer.SilverSerpents -= id_card[1][1]
                    contested = input(f'O adversário usou a paladina por {id_card[1][1]} serpentes de prata, gostaria de contestar? sim (1), não (0)\n Sua ação: ')
                    if contested == '1':
                        if 1 in IAplayer.CardsInHand:
                            if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                            elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                            else: lostCard = random.choice(player1.CardsInHand)
                            input(f'O adversário tinha a paladina, você perdeu a sua carta: {id_card[lostCard]}')
                            player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                            if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                                loseGame()
                            else:
                                IAplayer.CardsInHand[IAplayer.CardsInHand.index(1)] == random.randrange(Total_Cards)
                                os.system('cls')
                                print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                                kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                                if kamikaze == '1':
                                    if IAplayer.IAdecision():
                                        if 0 in player1.CardsInHand:
                                            os.system('cls')
                                            input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                            WinGame()
                                        else:
                                            os.system('cls')
                                            input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                            loseGame()
                                    else:
                                        os.system('cls')
                                        notContestedbyIA()
                                        witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                        if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                            IAplayer.CardsInHand[1] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                            IAplayer.CardsInHand[0] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        else:
                                            InvalidEntry()
                                elif kamikaze == '0':
                                    EnemyTurn()
                                else:
                                    InvalidEntry()                                
                    elif contested == '0':
                        input ('O adversário impediu o ataque')
                        EnemyTurn()
                    else:
                        InvalidEntry()
                else:
                    IAplayer.CardsInHand[1] = -1
                    CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                    if CardInHand != 0:
                        notContestedbyIA()
                        os.system('cls')
                        input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                        if IAplayer.IAdecision() or 'kamikaze' in Ia_use_this: IaUsesKamikaze()
                        EnemyTurn()
                    else:
                        WinGame()
            else:
                InvalidEntry()
        else:
            NotEnoughtMoney()
    elif actionPlayer1 == '4':
        if player1.SilverSerpents >= id_card[2][1]:
            witchCardKill = input('Qual carta inimiga gostaria de colocar na lista do assassino? Esquerda (0), Direita (1)\n Sua ação: ')
            if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                player1.SilverSerpents -= id_card[2][1]
                if IAplayer.SilverSerpents >= id_card[1][1] and IAplayer.IAdecision() or 'paladin' in Ia_use_this:
                    if 'paladin' not in Ia_use_this: Ia_use_this.append('paladin'), probabilityReset()
                    IAplayer.SilverSerpents -= id_card[1][1]
                    contested = input(f'O adversário usou a paladina por {id_card[1][1]} serpentes de prata, gostaria de contestar? sim (1), não (0)\n Sua ação: ')
                    if contested == '1':
                        if 1 in IAplayer.CardsInHand:
                            if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                            elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                            else: lostCard = random.choice(player1.CardsInHand)
                            input(f'O adversário tinha a paladina, você perdeu a sua carta: {id_card[lostCard]}')
                            player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                            if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                                loseGame()
                            else:
                                IAplayer.CardsInHand[IAplayer.CardsInHand.index(1)] == random.randrange(Total_Cards)
                                os.system('cls')
                                print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                                kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                                if kamikaze == '1':
                                    if IAplayer.IAdecision():
                                        if 0 in player1.CardsInHand:
                                            os.system('cls')
                                            input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                            WinGame()
                                        else:
                                            os.system('cls')
                                            input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                            loseGame()
                                    else:
                                        os.system('cls')
                                        notContestedbyIA()
                                        witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                        if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                            IAplayer.CardsInHand[1] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                            IAplayer.CardsInHand[0] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        else:
                                            InvalidEntry()
                                elif kamikaze == '0':
                                    EnemyTurn()
                                else:
                                    InvalidEntry()                                
                        else:
                            os.system('cls')
                            input('O adversário não tinha a paladina... Fazendo assim ele perder mais uma carta...')
                            WinGame()
                    elif contested == '0':
                        os.system('cls')
                        input ('O adversário impediu o ataque')
                        EnemyTurn()
                    else:
                        InvalidEntry()
                else:
                    if IAplayer.IAdecision():
                        if 2 in player1.CardsInHand:
                                os.system('cls')
                                input('O adversário te contestou e estava enganado... Fazendo assim, ele perder 1 carta para o assassino, e outra para o contestamento errado')
                                WinGame()
                        else:
                            if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                            elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                            else: lostCard = random.choice(player1.CardsInHand)
                            player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                            if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                                loseGame()
                            else:
                                os.system('cls')
                                input(f'O adversário contestou, e estava certo... Você perdeu a sua carta {id_card[lostCard][0]}')
                                os.system('cls')
                                print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                                kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                                if kamikaze == '1':
                                    if IAplayer.IAdecision():
                                        if 0 in player1.CardsInHand:
                                            os.system('cls')
                                            input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                            WinGame()
                                        else:
                                            os.system('cls')
                                            input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                            loseGame()
                                    else:
                                        os.system('cls')
                                        notContestedbyIA()
                                        witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                        if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                            IAplayer.CardsInHand[1] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                            IAplayer.CardsInHand[0] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        else:
                                            InvalidEntry()
                                elif kamikaze == '0':
                                    EnemyTurn()
                                else:
                                    InvalidEntry()                                
                    else:
                        IAplayer.CardsInHand[1] = -1
                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                        if CardInHand != 0:
                            notContestedbyIA()
                            os.system('cls')
                            input(f'Assassino levou a carta da direita de seu oponente, agora ele possui: {CardInHand} carta')
                            EnemyTurn()
                        else:
                            WinGame()
            elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                player1.SilverSerpents -= id_card[2][1]
                if IAplayer.SilverSerpents >= id_card[1][1] and IAplayer.IAdecision() or 'paladin' in Ia_use_this:
                    if 'paladin' not in Ia_use_this: Ia_use_this.append('paladin'), probabilityReset()
                    IAplayer.SilverSerpents -= id_card[1][1]
                    contested = input(f'O adversário usou a paladina por {id_card[1][1]} serpentes de prata, gostaria de contestar? sim (1), não (0)\n Sua ação: ')
                    if contested == '1':
                        if 1 in IAplayer.CardsInHand:
                            if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                            elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                            else: lostCard = random.choice(player1.CardsInHand)
                            input(f'O adversário tinha a paladina, você perdeu a sua carta: {id_card[lostCard]}')
                            player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                            if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                                loseGame()
                            else:
                                IAplayer.CardsInHand[IAplayer.CardsInHand.index(1)] == random.randrange(Total_Cards)
                                os.system('cls')
                                print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                                kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                                if kamikaze == '1':
                                    if IAplayer.IAdecision():
                                        if 0 in player1.CardsInHand:
                                            os.system('cls')
                                            input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                            WinGame()
                                        else:
                                            os.system('cls')
                                            input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                            loseGame()
                                    else:
                                        os.system('cls')
                                        notContestedbyIA()
                                        witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                        if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                            IAplayer.CardsInHand[1] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                            IAplayer.CardsInHand[0] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        else:
                                            InvalidEntry()
                                elif kamikaze == '0':
                                    EnemyTurn()
                                else:
                                    InvalidEntry()                                
                        else:
                            os.system('cls')
                            input('O adversário não tinha a paladina... Fazendo assim ele perder mais uma carta...')
                            WinGame()
                    elif contested == '0':
                        os.system('cls')
                        input ('O adversário impediu o ataque')
                        EnemyTurn()
                    else:
                        InvalidEntry()
                else:
                    notContestedbyIA()
                    if IAplayer.IAdecision() or 'dispute' in Ia_use_this:
                        if 2 in player1.CardsInHand:
                                os.system('cls')
                                input('O adversário te contestou e estava enganado... Fazendo assim, ele perder 1 carta para o assassino, e outra para o contestamento errado')
                                WinGame()
                        else:
                            if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                            elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                            else: lostCard = random.choice(player1.CardsInHand)
                            player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                            os.system('cls')
                            input(f'O adversário contestou, e estava certo... Você perdeu a sua carta {id_card[lostCard][0]}')
                            if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                                loseGame()
                            else:
                                os.system('cls')
                                print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                                kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                                if kamikaze == '1':
                                    if IAplayer.IAdecision():
                                        if 0 in player1.CardsInHand:
                                            os.system('cls')
                                            input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                            WinGame()
                                        else:
                                            os.system('cls')
                                            input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                            loseGame()
                                    else:
                                        os.system('cls')
                                        notContestedbyIA()
                                        witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                        if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                            IAplayer.CardsInHand[1] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                            IAplayer.CardsInHand[0] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        else:
                                            InvalidEntry()
                                elif kamikaze == '0':
                                    EnemyTurn()
                                else:
                                    InvalidEntry()                                
                    else:
                        IAplayer.CardsInHand[1] = -1
                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                        if CardInHand != 0:
                            notContestedbyIA()
                            os.system('cls')
                            input(f'Assassino levou a carta da direita de seu oponente, agora ele possui: {CardInHand} cartas')
                            EnemyTurn()
                        else:
                            WinGame()
            else:
                InvalidEntry()
        else:
            NotEnoughtMoney()
    elif actionPlayer1 == '5':
        if player1.SilverSerpents >= id_card[3][1]:
            if len(player1.CardsInHand) - player1.CardsInHand.count(-1) < 2:
                if IAplayer.IAdecision() or 'dispute' in Ia_use_this:
                    if 'dispute' not in Ia_use_this: Ia_use_this.append('dispute'), probabilityReset()
                    if 3 in player1.CardsInHand:
                        witchCardKill = input('O adversário contestou sua jogada, porém estava enganado. Qual carta adversária gostaria de eliminar? Esquerda (0), Direita (1)\nSua Ação:')
                        if witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                            IAplayer.CardsInHand[0] == -1
                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                            if CardInHand != 0:
                                os.system('cls')
                                print('Você eliminou a carta da esquerda de seu oponente')
                                player1.SilverSerpents -= id_card[3][1]
                                resurrectedCard = random.randrange(Total_Cards)
                                os.system('cls')
                                notContestedbyIA()
                                input(f'Você gastou 6 serpentes de prata para trazer à sua mão a carta: {id_card[resurrectedCard][0]}')
                                EnemyTurn()
                            else:
                                WinGame()
                        elif witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                            IAplayer.CardsInHand[1] == -1
                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                            if CardInHand != 0:
                                os.system('cls')
                                print('Você eliminou a carta da direita de seu oponente')
                                player1.SilverSerpents -= id_card[3][1]
                                resurrectedCard = random.randrange(Total_Cards)
                                os.system('cls')
                                notContestedbyIA()
                                input(f'Você gastou 6 serpentes de prata para trazer à sua mão a carta: {id_card[resurrectedCard][0]}')
                                EnemyTurn()
                            else:
                                WinGame()
                        else:
                            InvalidEntry()
                    else:
                        if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                        elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                        else: lostCard = random.choice(player1.CardsInHand)
                        os.system('cls')
                        input(f'O adversário contestou, e estava certo... Você perdeu a sua carta: {id_card[lostCard][0]}')
                        player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                        if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                            loseGame()
                        else:
                            os.system('cls')
                            print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                            kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                            if kamikaze == '1':
                                if IAplayer.IAdecision():
                                    if 0 in player1.CardsInHand:
                                        os.system('cls')
                                        input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                        WinGame()
                                    else:
                                        os.system('cls')
                                        input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                        loseGame()
                                else:
                                    os.system('cls')
                                    notContestedbyIA()
                                    witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                    if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                        IAplayer.CardsInHand[1] = -1
                                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                        if CardInHand != 0:
                                            input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                            EnemyTurn()
                                        else:
                                            WinGame()
                                    elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                        IAplayer.CardsInHand[0] = -1
                                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                        if CardInHand != 0:
                                            input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                            EnemyTurn()
                                        else:
                                            WinGame()
                                    else:
                                        InvalidEntry()
                            elif kamikaze == '0':
                                EnemyTurn()
                            else:
                                InvalidEntry()                            
                else:
                    player1.SilverSerpents -= id_card[3][1]
                    resurrectedCard = random.randrange(Total_Cards)
                    os.system('cls')
                    notContestedbyIA()
                    input(f'Você gastou 6 serpentes de prata para trazer à sua mão a carta: {id_card[resurrectedCard][0]}')
                    EnemyTurn()
            else:
                os.system('cls')
                input('Você já tem a quantia máxima de cartas na sua mão! Não foi possível trazer mais uma à vida.')
                player1_round()
        else:
            NotEnoughtMoney()
    elif actionPlayer1 == '6':
        if player1.SilverSerpents >= id_card[8][1]:
            if IAplayer.SilverSerpents >= id_card[8][2]:
                if IAplayer.IAdecision() or 'dispute' in Ia_use_this:
                    if 'dispute' not in Ia_use_this: Ia_use_this.append('dispute'), probabilityReset()
                    if 8 in player1.CardsInHand:
                        witchCardKill = input('O adversário contestou sua jogada, porém estava enganado. Qual carta adversária gostaria de eliminar? Esquerda (0), Direita (1)\nSua Ação:')
                        if witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                            IAplayer.CardsInHand[0] == -1
                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                            if CardInHand != 0:
                                os.system('cls')
                                input('Você eliminou a carta da esquerda de seu oponente')
                                os.system('cls')
                                ShuffleCard = random.randrange(Total_Cards)
                                player1.CardsInHand[player1.CardsInHand.index(8)] = ShuffleCard
                                input(f'A carta {id_card[8][0]} que você revelou ter, foi trocada por {ShuffleCard}')
                                os.system('cls')
                                print(f'Você mandou o traira roubar {id_card[8][2]} serpentes de prata.')
                                print(f'Ele dividiu {int(id_card[8][2]/2)} com você.')
                                player1.SilverSerpents += int(id_card[8][2]/2)
                                IAplayer.SilverSerpents -= int(id_card[8][2])
                                input(f'Agora, seu adversário possui {IAplayer.SilverSerpents} serpentes de prata. E você possui {player1.SilverSerpents}!')
                                EnemyTurn()
                            else:
                                WinGame()
                        elif witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                            IAplayer.CardsInHand[1] == -1
                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                            if CardInHand != 0:
                                os.system('cls')
                                input('Você eliminou a carta da direita de seu oponente')
                                os.system('cls')
                                ShuffleCard = random.randrange(Total_Cards)
                                player1.CardsInHand[player1.CardsInHand.index(8)] = ShuffleCard
                                input(f'A carta {id_card[8][0]} que você revelou ter, foi trocada por {ShuffleCard}')
                                os.system('cls')
                                print(f'Você mandou o traira roubar {id_card[8][2]} serpentes de prata.')
                                print(f'Ele dividiu {int(id_card[8][2]/2)} com você.')
                                player1.SilverSerpents += int(id_card[8][2]/2)
                                IAplayer.SilverSerpents -= int(id_card[8][2])
                                input(f'Agora, seu adversário possui {IAplayer.SilverSerpents} serpentes de prata. E você possui {player1.SilverSerpents}!')
                                EnemyTurn()
                            else:
                                WinGame()
                        else:
                            InvalidEntry()
                    else:
                        if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                        elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                        else: lostCard = random.choice(player1.CardsInHand)
                        os.system('cls')
                        input(f'O adversário contestou, e estava certo... Você perdeu a sua carta: {id_card[lostCard][0]}')
                        player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                        if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                            loseGame()
                        else:
                            os.system('cls')
                            print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                            kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                            if kamikaze == '1':
                                if IAplayer.IAdecision():
                                    if 0 in player1.CardsInHand:
                                        os.system('cls')
                                        input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                        WinGame()
                                    else:
                                        os.system('cls')
                                        input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                        loseGame()
                                else:
                                    os.system('cls')
                                    notContestedbyIA()
                                    witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                    if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                        IAplayer.CardsInHand[1] = -1
                                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                        if CardInHand != 0:
                                            input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                            EnemyTurn()
                                        else:
                                            WinGame()
                                    elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                        IAplayer.CardsInHand[0] = -1
                                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                        if CardInHand != 0:
                                            input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                            EnemyTurn()
                                        else:
                                            WinGame()
                                    else:
                                        InvalidEntry()
                            elif kamikaze == '0':
                                EnemyTurn()
                            else:
                                InvalidEntry()                            
                else:
                    notContestedbyIA()
                    if IAplayer.IAdecision() or 'countess' in Ia_use_this:
                        if 'countess' not in Ia_use_this: Ia_use_this.append('countess'), probabilityReset()
                        contested = input('O adversário útilizou a condessa, você não pegou serpentes de prata. Gostaria de contestar? sim (1), não (0)\nSua ação: ')
                        if contested == '1':
                            if 6 in IAplayer.CardsInHand:
                                if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                                elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                                else: lostCard = random.choice(player1.CardsInHand)
                                input(f'O adversário tinha a condessa, você perdeu a seguinte carta: {id_card[lostCard][0]}')
                                player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                                if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                                    loseGame()
                                else:
                                    IAplayer.CardsInHand[IAplayer.CardsInHand.index(6)] == random.randrange(Total_Cards)
                                    EnemyTurn()
                            else:
                                os.system('cls')
                                witchCardKill = input(f'O adversário não tem a condessa, qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                    IAplayer.CardsInHand[1] = -1
                                    CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                    if CardInHand != 0:
                                        input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                        if IAplayer.IAdecision() or 'kamikaze' in Ia_use_this: IaUsesKamikaze()
                                        EnemyTurn()
                                    else:
                                        WinGame()
                                elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                    IAplayer.CardsInHand[0] = -1
                                    CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                    if CardInHand != 0:
                                        input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                        if IAplayer.IAdecision() or 'kamikaze' in Ia_use_this: IaUsesKamikaze()
                                        EnemyTurn()
                                    else:
                                        WinGame()
                                else:
                                    InvalidEntry()
                    else:
                        os.system('cls')
                        notContestedbyIA()
                        print(f'Você mandou o traira roubar {id_card[8][2]} serpentes de prata.')
                        print(f'Ele dividiu {int(id_card[8][2]/2)} com você.')
                        player1.SilverSerpents += int(id_card[8][2]/2)
                        IAplayer.SilverSerpents -= int(id_card[8][2])
                        input(f'Agora, seu adversário possui {IAplayer.SilverSerpents} serpentes de prata. E você possui {player1.SilverSerpents}!')
                        EnemyTurn()
            else:
                if IAplayer.SilverSerpents != 0:
                    if IAplayer.IAdecision() or 'dispute' in Ia_use_this:
                        if 'dispute' not in Ia_use_this: Ia_use_this.append('dispute'), probabilityReset()
                        if 8 in player1.CardsInHand:
                            witchCardKill = input('O adversário contestou sua jogada, porém estava enganado. Qual carta adversária gostaria de eliminar? Esquerda (0), Direita (1)\nSua Ação:')
                            if witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                IAplayer.CardsInHand[0] == -1
                                CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                if CardInHand != 0:
                                    os.system('cls')
                                    input('Você eliminou a carta da esquerda de seu oponente')
                                    os.system('cls')
                                    ShuffleCard = random.randrange(Total_Cards)
                                    player1.CardsInHand[player1.CardsInHand.index(8)] = ShuffleCard
                                    input(f'A carta {id_card[8][0]} que você revelou ter, foi trocada por {ShuffleCard}')
                                    os.system('cls')
                                    print(f'Você mandou o traira roubar {id_card[8][2]} serpentes de prata, porém, ele só encontrou {IAplayer.SilverSerpents}.')
                                    print(f'Ele dividiu {int(IAplayer.SilverSerpents/2)} com você.')
                                    player1.SilverSerpents += int(IAplayer.SilverSerpents/2)
                                    IAplayer.SilverSerpents = 0
                                    input(f'Agora, seu adversário possui {IAplayer.SilverSerpents} serpentes de prata. E você possui {player1.SilverSerpents}!')
                                    EnemyTurn()
                                else:
                                    WinGame()
                            elif witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                IAplayer.CardsInHand[1] == -1
                                CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                if CardInHand != 0:
                                    os.system('cls')
                                    input('Você eliminou a carta da direita de seu oponente')
                                    os.system('cls')
                                    ShuffleCard = random.randrange(Total_Cards)
                                    player1.CardsInHand[player1.CardsInHand.index(8)] = ShuffleCard
                                    input(f'A carta {id_card[8][0]} que você revelou ter, foi trocada por {ShuffleCard}')
                                    os.system('cls')
                                    print(f'Você mandou o traira roubar {id_card[8][2]} serpentes de prata, porém, ele só encontrou {IAplayer.SilverSerpents}.')
                                    print(f'Ele dividiu {int(IAplayer.SilverSerpents/2)} com você.')
                                    player1.SilverSerpents += int(IAplayer.SilverSerpents/2)
                                    IAplayer.SilverSerpents = 0
                                    input(f'Agora, seu adversário possui {IAplayer.SilverSerpents} serpentes de prata. E você possui {player1.SilverSerpents}!')
                                    EnemyTurn()
                                else:
                                    WinGame()
                            else:
                                InvalidEntry()
                        else:
                            if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                            elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                            else: lostCard = random.choice(player1.CardsInHand)
                            os.system('cls')
                            input(f'O adversário contestou, e estava certo... Você perdeu a sua carta: {id_card[lostCard][0]}')
                            player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                            if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                                loseGame()
                            else:
                                os.system('cls')
                                print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                                kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                                if kamikaze == '1':
                                    if IAplayer.IAdecision():
                                        if 0 in player1.CardsInHand:
                                            os.system('cls')
                                            input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                            WinGame()
                                        else:
                                            os.system('cls')
                                            input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                            loseGame()
                                    else:
                                        os.system('cls')
                                        notContestedbyIA()
                                        witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                        if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                            IAplayer.CardsInHand[1] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                            IAplayer.CardsInHand[0] = -1
                                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                            if CardInHand != 0:
                                                input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                                EnemyTurn()
                                            else:
                                                WinGame()
                                        else:
                                            InvalidEntry()
                                elif kamikaze == '0':
                                    EnemyTurn()
                                else:
                                    InvalidEntry()                                
                    else:
                        notContestedbyIA()
                        if IAplayer.IAdecision() or 'countess' in Ia_use_this:
                            if 'countess' not in Ia_use_this: Ia_use_this.append('countess'), probabilityReset()
                            contested = input('O adversário útilizou a condessa, você não pegou serpentes de prata. Gostaria de contestar? sim (1), não (0)\nSua ação: ')
                            if contested == '1':
                                if 6 in IAplayer.CardsInHand:
                                    if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                                    elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                                    else: lostCard = random.choice(player1.CardsInHand)
                                    input(f'O adversário tinha a condessa, você perdeu a seguinte carta: {id_card[lostCard][0]}')
                                    player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                                    if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                                        loseGame()
                                    else:
                                        IAplayer.CardsInHand[IAplayer.CardsInHand.index(6)] == random.randrange(Total_Cards)
                                        os.system('cls')
                                        print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                                        kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                                        if kamikaze == '1':
                                            if IAplayer.IAdecision():
                                                if 0 in player1.CardsInHand:
                                                    os.system('cls')
                                                    input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                                    WinGame()
                                                else:
                                                    os.system('cls')
                                                    input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                                    loseGame()
                                            else:
                                                os.system('cls')
                                                notContestedbyIA()
                                                witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                                if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                                    IAplayer.CardsInHand[1] = -1
                                                    CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                                    if CardInHand != 0:
                                                        input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                                        EnemyTurn()
                                                    else:
                                                        WinGame()
                                                elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                                    IAplayer.CardsInHand[0] = -1
                                                    CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                                    if CardInHand != 0:
                                                        input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                                        EnemyTurn()
                                                    else:
                                                        WinGame()
                                                else:
                                                    InvalidEntry()
                                        elif kamikaze == '0':
                                            EnemyTurn()
                                        else:
                                            InvalidEntry()                                        
                                else:
                                    os.system('cls')
                                    witchCardKill = input(f'O adversário não tem a condessa, qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                    if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                        IAplayer.CardsInHand[1] = -1
                                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                        if CardInHand != 0:
                                            input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                            if IAplayer.IAdecision() or 'kamikaze' in Ia_use_this: IaUsesKamikaze()
                                            EnemyTurn()
                                        else:
                                            WinGame()
                                    elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                        IAplayer.CardsInHand[0] = -1
                                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                        if CardInHand != 0:
                                            input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                            if IAplayer.IAdecision() or 'kamikaze' in Ia_use_this: IaUsesKamikaze()
                                            EnemyTurn()
                                        else:
                                            WinGame()
                                    else:
                                        InvalidEntry()
                            else:
                                if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                                elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                                else: lostCard = random.choice(player1.CardsInHand)
                                os.system('cls')
                                input(f'O adversário contestou, e estava certo... Você perdeu a sua carta: {id_card[lostCard][0]}')
                                player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                                if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                                    loseGame()
                                else:
                                    os.system('cls')
                                    print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                                    kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                                    if kamikaze == '1':
                                        if IAplayer.IAdecision():
                                            if 0 in player1.CardsInHand:
                                                os.system('cls')
                                                input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                                WinGame()
                                            else:
                                                os.system('cls')
                                                input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                                loseGame()
                                        else:
                                            os.system('cls')
                                            notContestedbyIA()
                                            witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                            if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                                IAplayer.CardsInHand[1] = -1
                                                CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                                if CardInHand != 0:
                                                    input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                                    EnemyTurn()
                                                else:
                                                    WinGame()
                                            elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                                IAplayer.CardsInHand[0] = -1
                                                CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                                if CardInHand != 0:
                                                    input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                                    EnemyTurn()
                                                else:
                                                    WinGame()
                                            else:
                                                InvalidEntry()
                                    elif kamikaze == '0':
                                        EnemyTurn()
                                    else:
                                        InvalidEntry()                                    
                        else:
                            os.system('cls')
                            notContestedbyIA()
                            print(f'Você mandou o traira roubar {id_card[8][2]} serpentes de prata, porém, ele só encontrou {IAplayer.SilverSerpents}.')
                            print(f'Ele dividiu {int(IAplayer.SilverSerpents/2)} com você.')
                            player1.SilverSerpents += int(IAplayer.SilverSerpents/2)
                            IAplayer.SilverSerpents = 0
                            input(f'Agora, seu adversário possui {IAplayer.SilverSerpents} serpentes de prata. E você possui {player1.SilverSerpents}!')
                            EnemyTurn()
                else:
                    os.system('cls')
                    input('O adversário não possui moedas para serem roubadas')
                    player1_round()
        else:
            NotEnoughtMoney()
    elif actionPlayer1 == '7':
        if player1.SilverSerpents >= id_card[7][1]:
            if IAplayer.IAdecision() or 'dispute' in Ia_use_this:
                if 'dispute' not in Ia_use_this: Ia_use_this.append('dispute'), probabilityReset()
                if 7 in player1.CardsInHand:
                    witchCardKill = input('O adversário contestou sua jogada, porém estava enganado. Qual carta adversária gostaria de eliminar? Esquerda (0), Direita (1)\nSua Ação:')
                    if witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                        IAplayer.CardsInHand[0] == -1
                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                        if CardInHand != 0:
                            os.system('cls')
                            print('Você eliminou a carta da esquerda de seu oponente')
                            for valor in id_card: id_card[valor][1] += 1
                            print(player1.SilverSerpents)
                            player1.SilverSerpents += id_card[7][2]
                            input(f'Todos os preços foram aumentados em 1. Você recebeu {id_card[7][2]} serpentes de prata, tendo agora: {player1.SilverSerpents} serpentes de prata!')
                            id_card[7][2] += 1
                            EnemyTurn()
                        else:
                            WinGame()
                    elif witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                        IAplayer.CardsInHand[1] == -1
                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                        if CardInHand != 0:
                            os.system('cls')
                            print('Você eliminou a carta da direita de seu oponente')
                            for valor in id_card: id_card[valor][1] += 1
                            player1.SilverSerpents += id_card[7][2]
                            input(f'Todos os preços foram aumentados em 1. Você recebeu {id_card[7][2]} serpentes de prata, tendo agora: {player1.SilverSerpents} serpentes de prata!')
                            id_card[7][2] += 1
                            
                            EnemyTurn()
                        else:
                            WinGame()
                    else:
                        InvalidEntry()
                else:
                    if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                    elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                    else: lostCard = random.choice(player1.CardsInHand)
                    input(f'O adversário contestou corretamente, você perdeu a carta {id_card[lostCard][0]}')
                    player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                    if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                        loseGame()
                    else:
                        os.system('cls')
                        print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                        kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                        if kamikaze == '1':
                            if IAplayer.IAdecision():
                                if 0 in player1.CardsInHand:
                                    os.system('cls')
                                    input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                    WinGame()
                                else:
                                    os.system('cls')
                                    input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                    loseGame()
                            else:
                                os.system('cls')
                                notContestedbyIA()
                                witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                    IAplayer.CardsInHand[1] = -1
                                    CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                    if CardInHand != 0:
                                        input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                        EnemyTurn()
                                    else:
                                        WinGame()
                                elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                    IAplayer.CardsInHand[0] = -1
                                    CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                    if CardInHand != 0:
                                        input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                        EnemyTurn()
                                    else:
                                        WinGame()
                                else:
                                    InvalidEntry()
                        elif kamikaze == '0':
                            EnemyTurn()
                        else:
                            InvalidEntry() 
            else:
                for valor in id_card: id_card[valor][1] += 1
                player1.SilverSerpents += id_card[7][2]
                os.system('cls')
                input(f'Todos os preços foram aumentados em 1. Você recebeu {id_card[7][2]} serpentes de prata, tendo agora: {player1.SilverSerpents} serpentes de prata!')
                id_card[7][2] += 1
                EnemyTurn()
        else:
            NotEnoughtMoney()
    elif actionPlayer1 == '8':
        if player1.SilverSerpents >= id_card[4][1]:
            if IAplayer.IAdecision() or 'dispute' in Ia_use_this:
                if 'dispute' not in Ia_use_this: Ia_use_this.append('dispute'), probabilityReset()
                if 4 in player1.CardsInHand:
                    os.system('cls')
                    input('Seu adversário contestou a jogada, porém estava enganado...\nVocê poderá revelar uma carta inimiga e em seguida, matar uma delas...')
                    reveal = input('Qual carta inimiga gostaria de revelar? Esquerda (0), Direita (1)\nSua ação: ')
                    if reveal == '0' and IAplayer.CardsInHand[0] != -1:
                        os.system('cls')
                        input(f'A carta da esquerda do seu oponente é: {id_card[IAplayer.CardsInHand[0]][0]}\n')
                        witchCardKill = input('Qual carta adversária gostaria de eliminar? Esquerda (0), Direita (1)\nSua Ação:')
                        if witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                            IAplayer.CardsInHand[0] == -1
                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                            if CardInHand != 0:
                                os.system('cls')
                                print('Você eliminou a carta da esquerda de seu oponente')
                                player1.SilverSerpents -= id_card[4][1]
                                EnemyTurn()
                            else:
                                WinGame()
                        elif witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                            IAplayer.CardsInHand[1] == -1
                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                            if CardInHand != 0:
                                os.system('cls')
                                print('Você eliminou a carta da direita de seu oponente')
                                player1.SilverSerpents -= id_card[4][1]
                                EnemyTurn()
                            else:
                                WinGame()
                        else:
                            InvalidEntry()
                    elif reveal == '1' and IAplayer.CardsInHand[1] != -1:
                        os.system('cls')
                        input(f'A carta da direita do seu oponente é: {id_card[IAplayer.CardsInHand[1]][0]}')
                        witchCardKill = input('Qual carta adversária gostaria de eliminar? Esquerda (0), Direita (1)\nSua Ação:')
                        if witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                            IAplayer.CardsInHand[0] == -1
                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                            if CardInHand != 0:
                                os.system('cls')
                                print('Você eliminou a carta da esquerda de seu oponente')
                                player1.SilverSerpents -= id_card[4][1]
                                EnemyTurn()
                            else:
                                WinGame()
                        elif witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                            IAplayer.CardsInHand[1] == -1
                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                            if CardInHand != 0:
                                os.system('cls')
                                print('Você eliminou a carta da direita de seu oponente')
                                player1.SilverSerpents -= id_card[4][1]
                                EnemyTurn()
                            else:
                                WinGame()
                        else:
                            InvalidEntry()
                        EnemyTurn()
                    else:InvalidEntry()
                else:
                    if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                    elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                    else: lostCard = random.choice(player1.CardsInHand)
                    os.system('cls')
                    input(f'O adversário contestou, e estava certo... Você perdeu a sua carta: {id_card[lostCard][0]}')
                    player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                    if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                        loseGame()
                    else:
                        os.system('cls')
                        print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                        kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                        if kamikaze == '1':
                            if IAplayer.IAdecision():
                                if 0 in player1.CardsInHand:
                                    os.system('cls')
                                    input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                    WinGame()
                                else:
                                    os.system('cls')
                                    input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                    loseGame()
                            else:
                                os.system('cls')
                                notContestedbyIA()
                                witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                    IAplayer.CardsInHand[1] = -1
                                    CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                    if CardInHand != 0:
                                        input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                        EnemyTurn()
                                    else:
                                        WinGame()
                                elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                    IAplayer.CardsInHand[0] = -1
                                    CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                    if CardInHand != 0:
                                        input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                        EnemyTurn()
                                    else:
                                        WinGame()
                                else:
                                    InvalidEntry()
                        elif kamikaze == '0':
                            EnemyTurn()
                        else:
                            InvalidEntry()
            else:
                os.system('cls')
                notContestedbyIA()
                reveal = input('Qual carta inimiga gostaria de revelar? Esquerda (0), Direita (1)\nSua ação: ')
                if reveal == '0' and IAplayer.CardsInHand[0] != -1:
                    os.system('cls')
                    input(f'A carta da esquerda do seu oponente é: {id_card[IAplayer.CardsInHand[0]][0]}')
                    EnemyTurn()
                elif reveal == '1' and IAplayer.CardsInHand[1] != -1:
                    os.system('cls')
                    input(f'A carta da direita do seu oponente é: {id_card[IAplayer.CardsInHand[1]][0]}')
                    EnemyTurn()
                else:InvalidEntry()
        else: NotEnoughtMoney() 
    elif actionPlayer1 == '9':
        if len(player1.debt) > 0:
            os.system('cls')
            input(f"Você já tem um divida de {sum(player1.debt)} serpentes de prata com o duque.\nEle não te empresta-rá mais serpentes até que você pague o que deve.")
            player1_round()
        elif player1.angry_duke == True:
            beg = input(f"Você não pagou sua divida com o duque quando fez negócios com ele da última vez.\nEle exige que implore por perdão. Deseja fazer isso? Não (0) Sim (1)\nSua ação: ")
            if beg == '1':
                input('Você implora pelo perdão do duque, jogando sua dignidade fora.\nEle te perdoa, e voltará a fazer negócios com você.')
                player1.angry_duke = False
                EnemyTurn()
            elif beg == '0':
                os.system('cls')
                input('Você se recusou a implorar')
                player1_round()
            else: InvalidEntry()
        else:
            if IAplayer.IAdecision() or 'countess' in Ia_use_this:
                if 'countess' not in Ia_use_this: Ia_use_this.append('countess'), probabilityReset()
                contested = input('O adversário útilizou a condessa, você não pegou serpentes de prata, nem será cobrado pelo duque. Gostaria de contestar? Não (0), Sim (1)\nSua ação: ')
                if contested == '1':
                    if 6 in IAplayer.CardsInHand:
                        if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
                        elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
                        else: lostCard = random.choice(player1.CardsInHand)
                        input(f'O adversário tinha a condessa, você perdeu a seguinte carta: {id_card[lostCard][0]}')
                        player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
                        if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
                            loseGame()
                        else:
                            IAplayer.CardsInHand[IAplayer.CardsInHand.index(6)] == random.randrange(Total_Cards)
                            os.system('cls')
                            print('Você perdeu uma carta... Gostaria de usar o Kamikaze? sim (1), não (0)')
                            kamikaze = input('(SE RESPONDER SIM PARA ESTA AÇÃO, VOCÊ GANHARÁ OU PERDERÁ NESTA RODADA CASO O OPONENTE CONTESTE)\nSua ação: ')
                            if kamikaze == '1':
                                if IAplayer.IAdecision():
                                    if 0 in player1.CardsInHand:
                                        os.system('cls')
                                        input('O adverário te contestou, porém, ele estava enganado, fazendo-o perder mais uma carta...')
                                        WinGame()
                                    else:
                                        os.system('cls')
                                        input('O adverário te contestou, e ele estava certo sobre seu blefe...')
                                        loseGame()
                                else:
                                    os.system('cls')
                                    notContestedbyIA()
                                    witchCardKill = input(f'Qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                                    if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                                        IAplayer.CardsInHand[1] = -1
                                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                        if CardInHand != 0:
                                            input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                            EnemyTurn()
                                        else:
                                            WinGame()
                                    elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                                        IAplayer.CardsInHand[0] = -1
                                        CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                                        if CardInHand != 0:
                                            input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                            EnemyTurn()
                                        else:
                                            WinGame()
                                    else:
                                        InvalidEntry()
                            elif kamikaze == '0':
                                EnemyTurn()
                            else:
                                InvalidEntry()
                    else:
                        os.system('cls')
                        witchCardKill = input(f'O adversário não tem a condessa, qual carta adversária você quer matar? Esquerda (0) Direita (1)\nSua Ação: ')
                        if witchCardKill == '1' and IAplayer.CardsInHand[1] != -1:
                            IAplayer.CardsInHand[1] = -1
                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                            if CardInHand != 0:
                                input(f'Você matou a carta da direita de seu oponente, agora ele possui {CardInHand} carta')
                                if IAplayer.IAdecision() or 'kamikaze' in Ia_use_this: IaUsesKamikaze()
                                EnemyTurn()
                            else:
                                WinGame()
                        elif witchCardKill == '0' and IAplayer.CardsInHand[0] != -1:
                            IAplayer.CardsInHand[0] = -1
                            CardInHand = len(IAplayer.CardsInHand) - IAplayer.CardsInHand.count(-1)
                            if CardInHand != 0:
                                input(f'Você matou a carta da esquerda de seu oponente, agora ele possui {CardInHand} carta')
                                if IAplayer.IAdecision() or 'kamikaze' in Ia_use_this: IaUsesKamikaze()
                                EnemyTurn()
                            else:
                                WinGame()
                        else:
                            InvalidEntry()
                elif contested == '0':
                    EnemyTurn()
                else:
                    InvalidEntry()
            else:
                os.system('cls')
                player1.debt.append(0)
                player1.debt.append((id_card[5][2]+id_card[5][1]) // 2)
                player1.debt.append((id_card[5][2]+id_card[5][1]) // 2 + (id_card[5][2]+id_card[5][1]) % 2)
                if id_card[5][1] > 0:
                    input(f"Você pegou com o duque, {id_card[5][2]} serpentes de prata.\nPelas suas próximas 2 jogadas (a partir dos próximos 2 rounds), terá de pagar este valor à ele de volta.\nComo os impostos foram aumentados recentemente, o juros adicionado à sua divida será de: {id_card[5][1]}\nTotalizando: {sum(player1.debt)} serpentes de prata à serem pagos.\n\nSendo os valores das parcelas:\nDaqui 2 rounds: {player1.debt[1]}\nDaqui 3 rounds: {player1.debt[2]}")
                else:
                    input(f"Você pegou com o duque, {id_card[5][2]} serpentes de prata.\nPelas suas próximas 2 jogadas (a partir dos próximos 2 rounds), terá de pagar este valor à ele de volta.\n\nSendo os valores das parcelas:\nDaqui 2 rounds: {player1.debt[1]}\nDaqui 3 rounds: {player1.debt[2]}")
    #feito acima 
    elif actionPlayer1 == '10':
        ...
    else:
        InvalidEntry()  
   
"""       
    elif actionPlayer1 == '11':
"""

def demand_debt():
    if len(player1.debt) > 0:
        if player1.debt[0] != 0:
            if player1.SilverSerpents < player1.debt[0]:
                print("O duque veio cobrar sua divida.\nPorém, você não possui o dinheiro que você o deve")
                if player1.CardsInHand[0] == -1: dukes_assassin = ['direita', 1]
                elif player1.CardsInHand[1] == -1: dukes_assassin = ['esquerda', 0]
                elif random.choice(range(2)) == 1: dukes_assassin = ['direita', 1]
                else: dukes_assassin = ['esquerda', 0]
                player1.SilverSerpents = 0
                input(f"Ele tomou o pouco de serpentes que lhe restavam, e mandou o assassino atrás da sua carta {id_card[player1.CardsInHand[dukes_assassin[1]]][0]}")
                player1.CardsInHand[dukes_assassin[1]] = -1
                player1.angry_duke = True
                player1.debt.clear()
                if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1: loseGame()
            else:
                input(f"O duque veio cobrar sua divida.\nFoi pago ao duque {player1.debt[0]} serpentes de prata")
                player1.SilverSerpents -= player1.debt[0]
                del player1.debt[0]
        else: del player1.debt[0]

def IaUsesKamikaze():
    if 'kamikaze' not in Ia_use_this: Ia_use_this.append('kamikaze'), probabilityReset()
    os.system('cls')
    contest = input('O adversário usou o Kamikaze, gostaria de contestar? não (0), sim (1)\nSua ação: ')
    if contest == '1':
        if 0 in IAplayer.CardsInHand:
            os.system('cls')
            input('O adversario tinha o Kamikaze...')
            loseGame()
        else:
            os.system('cls')
            input('O adversario não tinha o Kamikaze...')
            WinGame()
    elif contest == '0':
        if player1.CardsInHand[1] == -1: lostCard = player1.CardsInHand[0]
        elif player1.CardsInHand[0] == -1: lostCard = player1.CardsInHand[1] 
        else: lostCard = random.choice(player1.CardsInHand)
        input(f'Você perdeu a carta {id_card[lostCard]}')
        player1.CardsInHand[player1.CardsInHand.index(lostCard)] = -1
        if player1.CardsInHand[0] == -1 and player1.CardsInHand[1] == -1:
            loseGame()
        else:
            EnemyTurn()
    else: InvalidEntry()


def NotEnoughtMoney():
    os.system('cls')
    input(f'Você possui apenas {player1.SilverSerpents}, junte mais serpentes de prata para realizar está ação!')
    player1_round()

def WinGame():
    os.system('cls')
    input('PARAPÉNS, VOCÊ VENCEU')

def notContestedbyIA():
    probability.append(1)
    print('seu adversário não te contestou.')

def probabilityReset():
    #print('Probabilidade resetada')
    probability.clear()
    probability.append(0)
    probability.append(0)
    probability.append(0)
    probability.append(0)
    probability.append(1)

def EnemyTurn():
    Ia_use_this.clear()
    os.system('cls')
    player1_round()
    print('Turno do adversário')

def InvalidEntry():
    os.system('cls')
    input('Ação invalida!')
    player1_round()

def loseGame():
    os.system('cls')
    input('Você Perdeu...')

if True:#random.randrange(2) == 1:
    player1_round()
else:
    EnemyTurn()

