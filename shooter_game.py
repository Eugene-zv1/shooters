#Создай собственный Шутер!
from pygame import *
from random import randint, random
mixer.init()
font.init()
font2 = font.Font(None, 36)
font1 = font.Font(None, 56)
mixer.music.load('space.ogg')
mixer.music.play()
window = display.set_mode((700,500))
space = transform.scale(image.load('galaxy.jpg'),(700,500))
space1 = transform.scale(image.load('photo.png'),(700,500))
display.set_caption('space')
        

    
            




class GameSprite(sprite.Sprite):
    def __init__(self,filename,w,h,speed,x,y):
            super().__init__()
            self.image = transform.scale(image.load(filename),(w,h))
            self.speed = speed
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x , self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0 :
            self.rect.y -= 10
        if keys_pressed[K_s] and self.rect.y < 450 :
            self.rect.y += 10
        if keys_pressed[K_a] and self.rect.x > 0 :
            self.rect.x -= 10
        if keys_pressed[K_d] and self.rect.x < 650:
         self.rect.x += 10
    def fire(self):
        x = self.rect.centerx
        y = self.rect.top
        bullet = Bullet('bullet.png',10,10,6,x,y) 
        bullets.add(bullet)
    def apply_buff(self, buff):
        if buff.type == "speed":
            self.speed += buff.value
        elif buff.type == "health":
            self.health += buff.value
    def remove_buff(self, buff):
        if buff.type == "speed":
            self.speed -= buff.value
        elif buff.type == "health":
            self.health -= buff.value



class Enemy(GameSprite):
    def __init__(self,filename,w,h,speed,x,y):
        super().__init__(filename,w,h,speed,x,y)
        self.last_shot_time = time.get_ticks()
        self.shoot_interval = 5000

    def update(self):
        global lost
    
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = -100 
            self.rect.x = randint(1,700)
            self.speed = randint(3,7)
            lost += 1
     
    def shoot(self):
        current_time = time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_interval:
            self.last_shot_time = current_time
            x = self.rect.centerx
            y = self.rect.top
            bullet = Monster_Bullet('bullet.png',10,10,6,x,y)
            monsters_bullet.add(bullet)




        

class Bullet(GameSprite):
    def update(self):
        

        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
class Monster_Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 499:
            self.kill()
class Buff(GameSprite):
    def __init__(self, filename,w,h,speed,x,y,duration):
        super().__init__(filename,w,h,speed,x,y)
        self.duration = duration
        self.start_time = time.get_ticks()
        self.active = True

    def update(self):
        if time.get_ticks() - self.start_time > self.duration :
            self.active = False
            self.kill()




buffs = sprite.Group()
monsters_bullet = sprite.Group()
bullets = sprite.Group()
menu = True
finish = False
button = GameSprite('button.png',120,120,0,300,120)
rocket = Player('rocket.png',65,65,10,50,400)
monsters1 = Enemy('ufo.png',65,39,randint(3,7,),randint(0,600),-60)
monsters2 = Enemy('ufo.png',65,39,randint(3,7,),randint(0,600),-60)
monsters3= Enemy('ufo.png',65,39,randint(3,7,),randint(0,600),-60)
monsters4 = Enemy('ufo.png',65,39,randint(3,7,),randint(0,600),-60)
monsters5 = Enemy('ufo.png',65,39,randint(3,7,),randint(0,600),-60)
win_f = font1.render(' Ты победил!!! ',1,(0,255,0))
lose_f = font1.render(' Ты проиграл ',1,(255,0,0))
monsters = sprite.Group()
monsters.add(monsters1,monsters2,monsters3,monsters4,monsters5)
levels=[{'enemy_count': 5},{'enemy_count': 10},{'enemy_count': 15}]
current_level_index = 0
def load_level(level_index):
    global monsters
    monsters.empty()
    level_data = levels[level_index]
    for i in range(level_data['enemy_count']):
        monsters.add(Enemy('ufo.png',65,39,randint(3,7,),randint(0,600),-60))
def check_level_complete(level_index):
    level_data = levels[level_index]
    return kills == level_data['enemy_count']
load_level(current_level_index)

run = True
clock = time.Clock()
FPS = 60
lost = 0
kills = 0
while run:

    if menu:
        window.blit(space,(0,0))
        button.reset()
        for e in event.get():
            if e.type == QUIT:
                    run = False
            if e.type == MOUSEBUTTONDOWN:
                x,y = e.pos
                if button.rect.collidepoint(x, y):
                    menu = False
    if finish != True and menu == False:
        window.blit(space,(0,0))
        if random() < 0.01:  
            buffs.add(Buff('ppp.png',20,20,6,x,y,(randint(0, 780), randint(0, 580), 5000)))

        for monster in monsters:
            monster.shoot()
        text_lose = font2.render('Пропущено: '+str(lost),1,(255,255,255))
        text_win = font2.render('Счет: '+str(kills),1,(255,255,255))
        window.blit(text_lose,(50,50))
        window.blit(text_win,(50,90))
        monsters_bullet.draw(window)
        monsters_bullet.update()
        buffs.update()
        buffs.draw(window)
        rocket.reset()
        rocket.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        sprites_list = sprite.groupcollide(monsters,bullets,True,True)
        for i in sprites_list:
            kills += 1
            monsters1 = Enemy('ufo.png',65,39,randint(3,7,),randint(0,600),-60)
            monsters.add(monsters1)
        if check_level_complete(current_level_index):
            current_level_index += 1
            if current_level_index < len(levels):
                load_level(current_level_index)
            else:
                finish = True
        # if kills >= 10:
        #     finish = True
        #     window.blit(win_f,(260,280))
        sprites_list = sprite.spritecollide(rocket,monsters,True)
        if lost >= 7 or len(sprites_list) >= 1:
            finish = True
            window.blit(lose_f,(260,280))

            
    
    for e in event.get():
            if e.type == QUIT:
                    run = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    rocket.fire()

        
    display.update()
    clock.tick(FPS)
