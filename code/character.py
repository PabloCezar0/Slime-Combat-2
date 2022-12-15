import pygame
import time
import random
from settings import *

screen = pygame.display.set_mode((WIDHT, HEIGHT))

class Character:
    def __init__(self, x, y, scale, name, max_hp, max_mp, strenght, agility, magic, defense, magic_defense, hp_potions, mp_potions, level, frames, weakness):  
        self.name = name #atributos
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.start_def = defense
        self.start_scale = scale
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.magic = 0
        self.max_hp_potion = hp_potions
        self.max_mp_potion = mp_potions
        self.strenght = strenght
        self.start_str = strenght
        self.agility = agility
        self.start_agi = agility
        self.magic = magic
        self.defense = defense
        self.magic_defense = magic_defense
        self.hp_potions = hp_potions
        self.mp_potions = mp_potions
        self.weakness = weakness #0 None - 1 Physical  - 2  Magic -  3 Fire - 4 Ice - 5 Lightning
        self.alive = True
        self.animation_list = [] #animando os frame
        self.update_time = pygame.time.get_ticks() #conta os milisegundos desde que o pygame.init foi utilizado na main
        self.frame_index = 0 #inica a aniamcao no primeiro frame
        self.action = 0 # cada numero signifca a animacao referente a uma acao, infelizmente nao existe sprite de magia para a maiorai dos persnagens 0 Iddle, 1 Attack, 2 Magic, 3 Hurt, 4 Dead
        #iddle animation
        temp_list = []
        for i in range(frames): #pega quantos frames cada personagem tem e anima
            img = pygame.image.load(f'graphics/Characters/{self.name}/Idle/{i}.png').convert_alpha() #utiliza uma funcao de pygame para carregar a imagem em uma variavel
            img = pygame.transform.scale(img, (img.get_width()*scale, img.get_height() * scale)) #utiliza uma funcao do pygame para alterar a escala da imagem, util para nao precisar manualmente alterar os sprites
            temp_list.append(img) #da append das imagens em uma lista temporaria
        self.animation_list.append(temp_list) #da append da lista temporaria na lista de animacao utilizada
        #attack animation
        temp_list = []
        for i in range(frames): #pega quantos frames cada personagem tem e anima
            img = pygame.image.load(f'graphics/Characters/{self.name}/Attack/{i}.png').convert_alpha() 
            img = pygame.transform.scale(img, (img.get_width()*scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #magic animation
        temp_list = []
        for i in range(frames): #pega quantos frames cada personagem tem e anima
            img = pygame.image.load(f'graphics/Characters/{self.name}/Magic/{i}.png').convert_alpha() 
            img = pygame.transform.scale(img, (img.get_width()*scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #hurt animation
        temp_list = []
        for i in range(frames): #pega quantos frames cada personagem tem e anima
            img = pygame.image.load(f'graphics/Characters/{self.name}/Hurt/{i}.png').convert_alpha() 
            img = pygame.transform.scale(img, (img.get_width()*scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #dead animation
        temp_list = []
        for i in range(frames): #pega quantos frames cada personagem tem e anima
            img = pygame.image.load(f'graphics/Characters/{self.name}/Dead/{i}.png').convert_alpha() 
            img = pygame.transform.scale(img, (img.get_width()*scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)  
        self.image = self.animation_list[self.action][self.frame_index] #altera o sprite atual para o sprite da lista na acao e frame correnspodente
        self.rect = self.image.get_rect() #cria um retangulo para colisao
        self.rect.center = (x,y) #centraliza o retangulo no x,y
        self.level = level 

    def update(self): #atualiza animacao
        animation_cd = 50
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cd:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1 #trava o frame no ultimo da animacao de morte se o personagem morreu
                self.rect.center = (self.x,self.y)
            else:
                self.idle()
   
    def reset(self): #funcao para resetar o personagem apos uma morte ou restart
        self.alive = True
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.defense = self.start_def
        self.agility = self.start_agi
        self.strenght = self.start_str
        self.hp_potions = self.max_hp_potion
        self.mp_potions = self.max_mp_potion 
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.x = self.start_x 
        self.y = self.start_y
        self.scale = self.start_scale
  


    def idle(self):
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



    def draw(self): #exibe o personagem na tela com o frame e o retangulo
        screen.blit(self.image, self.rect)

    def hurt(self):
            self.action = 3
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def dead(self):
            self.action = 4
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def attack(self,target):
        rand = random.randint(0,50) #numero aleatrio para critico
        if rand >= 40:
            damage = self.strenght * 2
        else:
             damage = self.strenght
        if target.weakness == 1:
            damage = damage*3
        if damage - target.defense > 0:
            target.hp -= damage - target.defense 
        target.hurt() #ativa a animacao hurt do alvo
        target.action = 3
        if target.hp < 1:#checa se ta morto ou nao
            target.hp = 0
            target.alive = False #se estiver morto altera o status do alvo pra morto
            target.dead() #se o alvo morrer ativar animacao de morte

        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
    #a logica do attack se aplica a todos os outros, muda somente o que aumenta o dano da skill
    def fire(self,target):
        self.mp -= 15
        rand = random.randint(0,50)
        if rand >= 40:
            damage = self.magic * 5
        else:
             damage = self.magic * 2
        if target.weakness == 2 or target.weakness == 3:
            damage = damage*3
        if damage - target.magic_defense > 0:
            target.hp -= damage - target.magic_defense
        target.hurt()
        target.action = 3
        if target.hp < 1:#checa se ta morto ou nao
            target.hp = 0
            target.alive = False
            target.dead()

        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
    def ice(self,target):
        self.mp -= 15
        rand = random.randint(0,50)
        if rand >= 40:
            damage = self.magic * 3
        else: 
             damage = self.magic * 2
        if target.weakness == 2 or target.weakness == 4:
            damage = damage*2
            target.agility -= 2
        if damage - target.magic_defense > 0:
            target.hp -= damage - target.magic_defense 
        target.hurt()
        target.action = 3
        if target.hp < 1:#checa se ta morto ou nao
            target.hp = 0
            target.alive = False
            target.dead()

        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def lightning(self,target):
        self.mp -= 15
        rand = random.randint(0,50)
        if rand >= 40:
            damage = self.magic * 3
        else: 
             damage = self.magic * 2
        if target.weakness == 2 or target.weakness == 5:
            damage = damage*2
            target.strenght -= 2
        if damage - target.magic_defense > 0:
            target.hp -= damage - target.magic_defense 
        target.hurt()
        target.action = 3
        if target.hp < 1:#checa se ta morto ou nao
            target.hp = 0
            target.alive = False
            target.dead()
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def death_magic(self,target):

        self.mp -= 30
        rand = random.randint(0,50)
        if rand >= 40:
            damage = self.magic * 3
        else: 
            damage = self.magic * 2
        if target.weakness == 2 or target.weakness == 5:
            damage = damage*2
            target.magic_defense -= 2
            target.defense -= 2
        if damage - target.magic_defense > 0:
            target.hp -= damage - target.magic_defense 
        target.hurt()
        target.action = 3
        if target.hp < 1:#checa se ta morto ou nao
            target.hp = 0
            target.alive = False
            target.dead()

        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()