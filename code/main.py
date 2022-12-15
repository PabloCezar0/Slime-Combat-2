import pygame
from settings import *
from debug import debug
import time
import character
import buttons
from fila import Queue
from heap import MinHeap
import random
from credits import Credits


#teste5

pygame.init()

clock = pygame.time.Clock() #variavel para controlar o FPS, usada no começo do loop de combate


screen = pygame.display.set_mode((WIDHT, HEIGHT)) #inicia a janela baseado nos parametros em Settings

pygame.display.set_caption('Slime Combat II') #Muda o nome da janela do jogo


run = True #necssario para o pygame

background_img = pygame.image.load('graphics/Background/background.png').convert_alpha() #coloca um background

slime_panel_img = pygame.image.load('graphics/Icons/SlimeStatusBar.png').convert_alpha() #barrinha embaixo do background, onde fica a vida e mana para o protagonista

enemy_panel_img = pygame.image.load('graphics/Icons/EnemyStatusBar.png').convert_alpha() #barrinha embaixo do background, onde fica a vida e mana para inimigos

win_screen = pygame.image.load('graphics/Background/Win.png').convert_alpha()#tela de vitoria com os scores


#icones nomes explicam para que cada um serve
attack_icon = pygame.image.load('graphics/Icons/Sword.png').convert_alpha()
active_attack_icon = pygame.image.load('graphics/Icons/S_Active.png').convert_alpha()
potion_icon = pygame.image.load('graphics/Icons/Potion.png').convert_alpha()
mp_potion_icon = pygame.image.load('graphics/Icons/MpPotion.png').convert_alpha()
fireball_icon = pygame.image.load('graphics/Spells/Fireball.png').convert_alpha()
ice_icon = pygame.image.load('graphics/Spells/Ice.png').convert_alpha()
lightning_icon = pygame.image.load('graphics/Spells/Lightning.png').convert_alpha()
active_fireball_icon = pygame.image.load('graphics/Spells/Fireball_A.png').convert_alpha()
active_ice_icon = pygame.image.load('graphics/Spells/Ice_A.png').convert_alpha()
active_lightning_icon = pygame.image.load('graphics/Spells/Lightning_A.png').convert_alpha()
victory_icon = pygame.image.load('graphics/Icons/Victory.png').convert_alpha()
defeat_icon = pygame.image.load('graphics/Icons/Defeat.png').convert_alpha()
restart_icon = pygame.image.load('graphics/Icons/Restart.png').convert_alpha()
left_icon = pygame.image.load('graphics/Icons/Left.png').convert_alpha()
right_icon = pygame.image.load('graphics/Icons/Right.png').convert_alpha()


#variaveis para controlar os turnos e o combate
current_fighter = 1 #lutador 1 protagonista

level_over = 0 #1 acaba o level e manda para o proximo no
game_win = 0 # 1 o jogo vence -1 game over
action_cd = 0
wait_time = 1200
action_wait = wait_time
clicked = False
heal = 0
heal_mp = 0
next_turn = 0
turns = 1
turn_end = 0
pontuationTurn = 0
level_pontuation = []
next_level = 0

font = pygame.font.SysFont('Times New Roman', 18)#fonte
end_font = pygame.font.SysFont('Times New Roman', 30)#fonte
win_font = pygame.font.SysFont('Times New Roman', 60)#fonte

#RGG
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
wine = (255,50,50)

#background
def draw_bg():
   screen.blit(background_img, (0,0))

def draw_win():
   screen.blit(win_screen, (0,0))

#imprimir texto
def drawn_text(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#paineis para se colocara vida e pocoes
def draw_panelSlime():
        screen.blit(slime_panel_img, (0,450))
        drawn_text(f'{Slime.name} HP: {Slime.hp}', font, red, 100, 230)
        drawn_text(f'{Slime.name} MP: {Slime.mp}', font, blue, 100, 250)
        drawn_text(f'{Slime.hp_potions}', font, red, 40, 580)
        drawn_text(f'{Slime.mp_potions}', font, blue, 80, 580)

#painel com vida e mana dos inimigos
def draw_panelEnemy(aux):
    if aux.head.data.name != 'Slime':
        screen.blit(enemy_panel_img, (450,450))
        drawn_text(f'{aux.head.data.name} Level: {aux.head.data.level}', font, black, 550 , 375 + 80 )
        drawn_text(f'{aux.head.data.name} HP: {aux.head.data.hp}', font, red, 550 , 400 + 80 )
        drawn_text(f'{aux.head.data.name} MP: {aux.head.data.mp}', font, blue, 550, 430 + 80 )
    if aux.tail.data.name != 'Slime':
        screen.blit(enemy_panel_img, (450,450))
        drawn_text(f'{aux.tail.data.name} Level: {aux.tail.data.level}', font, black, 550 , 375 + 80 )
        drawn_text(f'{aux.tail.data.name} HP: {aux.tail.data.hp}', font, red, 550 , 400 + 80 )
        drawn_text(f'{aux.tail.data.name} MP: {aux.tail.data.mp}', font, blue, 550, 430 + 80 )


#criar botoes para pressionar
sword_button = buttons.Button(screen, 25,460, attack_icon, 50, 50)
potion_button = buttons.Button(screen, 30,540, potion_icon, 30, 30)
mp_button = buttons.Button(screen, 70,540, mp_potion_icon, 30, 30)
fireball_button = buttons.Button(screen, 100,455, fireball_icon, 40, 50)
ice_button = buttons.Button(screen, 160,455, ice_icon, 45, 45)
lightning_button = buttons.Button(screen, 230,455, lightning_icon, 45, 45)
restart_button = buttons.Button(screen, 300,100, restart_icon, 120, 28)
left_button = buttons.Button(screen, 200,100, left_icon, 80, 28)
right_button = buttons.Button(screen, 500,100, right_icon, 80, 28)

#criar inimigos              x  y scale name hp mp str mgc agi def mdef hpP mpP level frame weak
Slime = character.Character(140,370,1,'Slime',100,100,10,100,10,10,10,2,2,1,8,0)
enemyList = [0]*4
enemyList[0] = character.Character(700,385,5 ,'Zombie',50,0,10,0,3,0,1,0,0,1,7,1)
enemyList[1] = character.Character(500,385,5 ,'Zombie',60,0,10,0,4,2,1,0,0,2,7,1)
enemyList[2] = character.Character(700,360,5 ,'Skelleton',50,0,10,0,3,0,1,0,0,1,18,1)
enemyList[3] = character.Character(500,360,5 ,'Skelleton',60,0,5,0,3,50,1,0,0,2,18,1)

#Bosses
bossList = [0]*4
bossList[0] = character.Character(500,130,4 ,'Demon of Fire',80,50,1000,0,3,50,1,0,0,5,22,1)
bossList[1] = character.Character(500,130,4 ,'Demon of Fire',95,50,1000,0,3,50,1,0,0,6,22,1)
bossList[2] = character.Character(600,200,6 ,'Lich',80,100,10,0,3,50,1,0,0,5,18,1)
bossList[3] = character.Character(600,200,6 ,'Lich',95,100,10,0,3,50,1,0,0,6,18,1)

# Cria a árvore min-Heap
gameHeap = MinHeap(15)

for i in range(0,7):
    gameHeap.insert(random.choice(enemyList))

for i in range(0,8):
    gameHeap.insert(random.choice(bossList))

print(gameHeap)


pontuationHeap = MinHeap(4)


#Função que percorre a Heap

def runHeap(heap, level, side, next):
    print(level)
    if side == 'left' and next == 1:
        next = 0
        level = heap.leftChildIndex(level)   
        print(level)
        return level
    if side == 'right' and next == 1:
        next = 0
        level = heap.rightChildIndex(level)
        print(level)
        return level

# Função que percorre os leveis da Heap    
def turnLevel(Heap, Slime, Queue, level):
    Queue.dequeue()
    Queue.dequeue()
    Queue.enqueue(Slime)
    Queue.enqueue(Heap.storage[level])

#Função que cria o turno da fase
def turnQueue(Queue, turns):
    aux = Queue.dequeue()
    Queue.enqueue(aux)

def pontuation(hp, turns, level):
    points = (hp+level)
    return points
 
# Função que aciona os ataques
def turnAtack(person, turns):
    global wait_time
    global action_cd
    global action_wait
    global next_turn
    attack = False
    magic = random.randint(0,5)
    potion = False
    fire_magic = False
    ice_magic = False
    lightning_magic = False


    if person.head.data.name == 'Slime':
        if sword_button.clicked == True:
            if fireball_button.clicked == True or lightning_button.clicked == True or ice_button.clicked == True:
                sword_button.clicked = False
            fireball_button.clicked = False
            ice_button.clicked = False
            lightning_button.clicked = False
            sword_button.image = active_attack_icon
            if person.tail.data.rect.collidepoint(pos):
                pygame.mouse.set_visible(False)
                screen.blit(active_attack_icon, pos)
                if clicked == True:
                    attack = True
                    target = person.tail.data

        if fireball_button.clicked == True:
            if ice_button.clicked == True or lightning_button.clicked == True:
                fireball_button.clicked = False
            ice_button.clicked = False
            lightning_button.clicked = False
            sword_button.clicked = False
            fireball_button.image = active_fireball_icon
            if person.tail.data.rect.collidepoint(pos):
                pygame.mouse.set_visible(False)
                screen.blit(active_fireball_icon, pos)
                if clicked == True:
                    fire_magic = True
                    target = person.tail.data

        if ice_button.clicked == True:
            if lightning_button.clicked == True:
                ice_button.clicked = False
            sword_button.clicked = False
            fireball_button.clicked = False
            lightning_button.clicked = False
            ice_button.image = active_ice_icon
            if person.tail.data.rect.collidepoint(pos):
                pygame.mouse.set_visible(False)
                screen.blit(active_ice_icon, pos)
                if clicked == True:
                    ice_magic = True
                    target = person.tail.data

        if lightning_button.clicked == True:
            sword_button.clicked = False
            fireball_button.clicked = False
            ice_button.clicked = False
            lightning_button.image = active_lightning_icon
            if person.tail.data.rect.collidepoint(pos):
                pygame.mouse.set_visible(False)
                screen.blit(active_lightning_icon, pos)
                if clicked == True:
                    lightning_magic = True
                    target = person.tail.data

        if potion_button.clicked == True and potion == False and Slime.hp_potions > 0: #controla as pocoes, impede o usuario de usar pocao com hp maximo e impede o hp com a cura passar do hp maximo

                if person.head.data.hp == person.head.data.max_hp and potion == False:
                    drawn_text('Health Full', font, red, 240, 230)
                    
                if person.head.data.hp > 50 and person.head.data.hp != person.head.data.max_hp and potion == False:
                    person.head.data.hp += person.head.data.max_hp - person.head.data.hp
                    potion = True
                    person.head.data.hp_potions -= 1
                    potion_button.clicked = False


                if person.head.data.hp <= 50 and potion == False and person.head.data.hp != 100:
                    drawn_text('+50', font, red, 240, 250)    
                    person.head.data.hp += 50
                    potion = True
                    person.head.data.hp_potions -= 1
                    potion_button.clicked = False

        if mp_button.clicked == True and potion == False and Slime.mp_potions > 0 :#controla as pocoes, impede o usuario de usar pocao com mp maximo e impede o hp com a cura passar do mp maximo

            if person.head.data.mp == person.head.data.max_mp and potion == False:
                drawn_text('Mana Full', font, blue, 240, 250)
                    
            if person.head.data.mp > 50 and person.head.data.mp != 100 and potion == False:
                person.head.data.mp += person.head.data.max_mp - person.head.data.mp
                potion = True
                person.head.data.mp_potions -= 1
                mp_button.clicked = False
    
            
            if person.head.data.mp <= 50 and potion == False and person.head.data.mp != 100:  
                drawn_text('+50', font, blue, 240, 250)  
                person.head.data.mp += 50
                potion = True            
                person.head.data.mp_potions -= 1
                mp_button.clicked = False
     
                    
        
            #acao do jogador se o slime tiver vivo ele comeca fighter 1 eh slime 2 eh o inimigo 1 e o 3 inimigo 2
 

        if attack == True: #controla o ataque de fogo
            #attack
            if target != None:                       
                person.head.data.attack(target)
                sword_button.clicked = False
                potion = False
                potion_button.clicked = False
                mp_button.clicked = False
                if person.tail.data.hp == 0:
                    person.tail.data.alive = False
                else:
                    turns += 1
                    turnQueue(person, turns)



        if fire_magic == True: #controla o ataque de fogo
            if person.head.data.mp >= 15: #so executa o ataque se mana for maior que 15
                #attack
                if target != None:                        
                    person.head.data.fire(target)
                    fireball_button.clicked = False
                    potion = False
                    potion_button.clicked = False
                    mp_button.clicked = False
                    fire_magic = False
                    if person.tail.data.hp == 0:
                        person.tail.data.alive = False
                    else:
                        turns += 1
                        turnQueue(person, turns)


            else:
                drawn_text('No mana', font, blue, 240, 250) 

        if ice_magic == True: #controla o ataque de gelo
            if person.head.data.mp >= 15: #so executa o ataque se mana for maior que 15
                #attack
                if target != None:                        
                    person.head.data.ice(target)
                    ice_button.clicked = False
                    potion = False
                    potion_button.clicked = False
                    mp_button.clicked = False
                    ice_magic = False
                    if person.tail.data.hp == 0:
                        person.tail.data.alive = False
                    else:
                        turns += 1
                        turnQueue(person, turns)


            else:
                drawn_text('No mana', font, blue, 240, 250) 


        if lightning_magic == True: #controla o ataque de raio
            if person.head.data.mp >= 15: #so executa o ataque se mana for maior que 15
                #attack
                if  target != None:                        
                    person.head.data.lightning(target)
                    lightning_button.clicked = False
                    potion = False
                    potion_button.clicked = False
                    mp_button.clicked = False
                    lightning_magic = False
                    if person.tail.data.hp == 0:
                        person.tail.data.alive = False
                    else:
                        turns += 1
                        turnQueue(person, turns)
                    

 
            else:
                drawn_text('No mana', font, blue, 240, 250)  
        action_cd = 0
        

        

    if person.head.data.name != 'Slime':
        
        
        action_cd += 1
        if action_cd >= action_wait:


            if person.head.data.name == 'Lich' and person.head.data.mp < 30  or person.head.data.name == 'Demon' and person.head.data.mp < 15 or magic == 5:

            
                if person.head.data.name == 'Lich' and person.head.data.mp >= 30 and magic == 5:
                    #attack
                    person.head.data.death_magic(person.tail.data)
                    time.sleep(0.08)
                    

                if person.head.data.name == 'Demon' and person.head.data.mp >= 15 and magic == 5:
                    #attack
                    person.head.data.fire(person.tail.data)
                    time.sleep(0.08)
                    
                else:
                    person.head.data.attack(person.tail.data)
                    time.sleep (0.08)
                    

            else:
                person.head.data.attack(person.tail.data)
                time.sleep (0.08)
                
            turnQueue(person, turns)
 
            
        



#coloca os inimigos em uma lista 
character_list = Queue()
enemy_alive = 0
level = 0
turnLevel(gameHeap, Slime, character_list, level)
enemy_alive += 1

while run == True:
    clock.tick(FPS) #limita o fps para o colocado em settings
    
    next_level = 0
    while game_win == 0 and run == True:
        draw_bg() #mostra background na tela
        draw_panelSlime() #mostra o painel do pc
        #Gerar personagens
        Slime.update()
        Slime.draw()
        sword_button.draw()
        potion_button.draw()
        fireball_button.draw()
        ice_button.draw()
        mp_button.draw()
        lightning_button.draw()

        if character_list.head.data.name != Slime:
            character_list.head.data.draw()
            character_list.head.data.update()
        if character_list.tail.data.name != Slime:
            character_list.tail.data.draw()
            character_list.tail.data.update()
        

        draw_panelEnemy(character_list)

        #controlar o ataque
        
        pygame.mouse.set_visible(True)#mostra o mouse normal apos ataque

        pos = pygame.mouse.get_pos()#pega a posicao do mosue e coloca em pos

            
    # todos fazem a mesma coisa, ao clicar em algum botao de ataque e colocar o mouse em cima do inimigo o cursos muda para o do icone de ataque ativo selecionado

        if level_over == 0: # se o jogo nao tiver ganho roda o codigo abaixo
  

            turnAtack(character_list, turns)

            if  character_list.tail.data.name == 'Slime' and character_list.tail.data.hp <= 0:
                level_over = -1
            
            if character_list.head.data.name == 'Slime' and character_list.head.data.hp <= 0:
                level_over = -1          

            if character_list.head.data.name != 'Slime' and character_list.head.data.hp <= 0:
                action_cd = 0
                next_level = 1
                level_over = 1 
                turn_end = 1
                

            if character_list.tail.data.name != 'Slime' and character_list.tail.data.hp <= 0:
                action_cd = 0
                next_level = 1
                level_over = 1     
                turn_end = 1 

            

        #faz as imagens serem as padroes apos ataque
        if sword_button.clicked == False:
            sword_button.image = attack_icon
        if fireball_button.clicked == False:
            fireball_button.image = fireball_icon
        if ice_button.clicked == False:
            ice_button.image = ice_icon
        if lightning_button.clicked == False:
            lightning_button.image = lightning_icon

#check para vitoria 
        if level_over == 1:
            

            screen.blit(victory_icon, (250,0))
            left_button.clicked = False
            right_button.clicked = False
            if character_list.tail.data.name != 'Demon of Fire' and character_list.tail.data.name != 'Lich' :
                if left_button.draw():
                    left_button.clicked = False
                    Slime.reset()
                    character_list.tail.data.reset()
                    level_over = 0
                    level = runHeap(gameHeap, level, 'left', next_level)
                    turnLevel(gameHeap, Slime, character_list, level)
                    
                if right_button.draw():
                    right_button.clicked = False
                    Slime.reset()
                    character_list.tail.data.reset()
                    level_over = 0
                    level = runHeap(gameHeap, level, 'right', next_level)    
                    turnLevel(gameHeap, Slime, character_list, level)

            if (turn_end == 1):
                turn_end = 0
                pontuationTurn = pontuation(character_list.head.data.hp, turns, character_list.tail.data.level)
                auxPoint = Credits(character_list.tail, pontuationTurn)
                pontuationHeap.insert(auxPoint)

            if character_list.tail.data.name == 'Demon of Fire' or character_list.tail.data.name == 'Lich' :
                if action_cd >= 7000: 
                    game_win = 1 
                action_cd += 1
                while pontuationHeap.size != 0:           
                    level_pontuation.append(pontuationHeap.remove())
    


            if character_list.tail.data.name == 'Demon of Fire' or character_list.tail.data.name == 'Lich' :
                if action_cd >= 7000: 
                    game_win = 1 
                action_cd += 1
                while pontuationHeap.size != 0:           
                    level_pontuation.append(pontuationHeap.remove())

            sword_button.clicked = False
            fireball_button.clicked = False
            ice_button.clicked = False
            lightning_button.clicked = False
            action_cd += 1
            
 
        
#derrota
        if level_over == -1:
            restart_button.clicked = False
            screen.blit(defeat_icon, (250,0))
            if restart_button.draw():
                character_list.head.data.reset()
                character_list.tail.data.reset()
                current_fighter = 1
                level_over = 0
            sword_button.clicked = False
            fireball_button.clicked = False
            ice_button.clicked = False
            lightning_button.clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
        pygame.display.update()  

    while game_win == 1:
        draw_win()
        drawn_text('Scores', win_font, wine, 250, 130)
        for i, point in enumerate(level_pontuation):
            drawn_text(f'{point.enemyName}, Level: {point.level}  Score: {point.pontuation}', end_font, black, 250 , 200+(i*80)) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit() 
                pygame.quit()
                exit()
        pygame.display.update() 

pygame.quit()