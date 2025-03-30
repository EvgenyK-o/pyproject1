#Создай собственный космический Шутер!
#Create your own space Shooter!
from pygame import *
from random import randint
from time import time as timer
w=display.set_mode((700,500))
background=transform.scale(image.load('galaxy.jpg'),(700,500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
game=True
finish=False
class GameSprite(sprite.Sprite):
    def __init__(self,p_image,x,y,size_x,size_y,speed):
        sprite.Sprite.__init__(self)
        self.image=transform.scale(image.load(p_image),(size_x,size_y))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.speed=speed
    def reset(self):
        w.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x < 695:
            self.rect.x+=self.speed
    def fire(self):
        bullet=Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,-25)
        bullets.add(bullet)
score=0
skiped=0   
lives=3
color1=(0,255,0)
class Enemy(GameSprite):
    def flying(self):
        global skiped        
        self.rect.y+=self.speed
        if self.rect.y>500:
            self.rect.y=0
            self.rect.x=randint(50,650)
            skiped+=1
class Astro(GameSprite):
    def flying(self):        
        self.rect.y+=self.speed
        if self.rect.y>500:
            self.rect.y=0
            self.rect.x=randint(50,650)
class Bullet(GameSprite):
    def shooting(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
shoot=mixer.Sound('fire.ogg')
bullets=sprite.Group()
font.init()
font1=font.SysFont('Arial',33)
font2=font.SysFont('Arial',90)
font3=font.SysFont('Arial',90)
font4=font.SysFont('Arial',40)
player=Player('rocket.png',5,400,80,100,15)
monsters=sprite.Group()
for i in range(1,6):
    enemy=Enemy('ufo.png',randint(50,620),-80,80,50,randint(1,5))
    monsters.add(enemy)
asteroids=sprite.Group()
for i in range(1,4):
    asteroid=Astro('asteroid.png',randint(50,620),-80,50,40,randint(3,8))
    asteroids.add(asteroid)
bullet_count=0
rel_time=False
while game:
    for e in event.get():
        if e.type==QUIT:
            game=False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE: 
                if bullet_count<5 and rel_time==False:
                    player.fire()
                    shoot.play()
                    bullet_count+=1
                if bullet_count>=5 and rel_time==False:
                    start_time=timer()
                    rel_time=True
    if not finish:
        w.blit(background,(0,0))        
        player.update()
        for enemy in monsters:
            enemy.flying()      
        monsters.draw(w)
        for asteroid in asteroids:
            asteroid.flying()       
        asteroids.draw(w)
        bullets.draw(w)
        for bullet in bullets:
            bullet.shooting()
        score_text=font1.render('Счёт:'+str(score),True,(255,255,255))
        skiped_text=font1.render('Пропущено:'+str(skiped),True,(255,255,255))
        live_text=font3.render(str(lives),True,color1)
        w.blit(score_text,(5,20))
        w.blit(skiped_text,(5,55))
        w.blit(live_text,(650,20))
        player.reset()
        sprites_list=sprite.groupcollide(monsters,bullets,True,True)
        sprites_list2=sprite.spritecollide(player,monsters,False)
        sprites_list3=sprite.spritecollide(player,asteroids,False)
        if rel_time==True:
            end_time=timer()
            if end_time-start_time<3:
                charge=font4.render('Wait, reload...',1,(255,0,0))
                w.blit(charge,(250,460))
            else:
                rel_time=False
                bullet_count=0
        for i in sprites_list:
            score+=1
            enemy=Enemy('ufo.png',randint(50,620),-80,80,50,randint(1,5))
            monsters.add(enemy)
        if  len(sprites_list3)>=1:
            sprite.spritecollide(player,asteroids,True)
            lives-=1
            asteroid=Astro('asteroid.png',randint(50,620),-80,50,40,randint(3,8))
            asteroids.add(asteroid)
        elif len(sprites_list2)>=1:
            sprite.spritecollide(player,monsters,True)
            lives-=1
            enemy=Enemy('ufo.png',randint(50,620),-80,80,50,randint(1,5))
            monsters.add(enemy)
        if score>=10:
            win=font2.render('You win!',True,(0,200,0))
            w.blit(win,(220,220))
            finish=True
        if lives<=0 or skiped >= 3:
            losed=font2.render('You lose',True,(255,0,0))
            w.blit(losed,(220,220))
            finish=True
        if lives==3:
            color1=(0,255,0)
        if lives==2:
            color1=(255,255,65)
        if lives==1:
            color1=(255,0,0)
        display.update()
    else:
        finish=False
        score=0
        skiped=0
        lives=3
        bullet_count=0
        color1=(0,255,0)
        for monster in monsters:
            monster.kill()
        for bullet in bullets:
            bullet.kill()
        for asteroid in asteroids:
            asteroid.kill()
        time.delay(3000)
        for i in range(1,6):
            enemy=Enemy('ufo.png',randint(50,620),-80,80,50,randint(1,5))
            monsters.add(enemy)
        for i in range(1,4):
            asteroid=Astro('asteroid.png',randint(50,620),-80,50,40,randint(3,8))
            asteroids.add(asteroid)
    time.delay(50)
