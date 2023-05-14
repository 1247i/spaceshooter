#Создай собственный Шутер!

from pygame import *
from random import randint
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound=mixer.Sound('fire.ogg')
win_w=1000
win_h=600
img_back='epic.jpg'
img_hero='rocket.png'
font.init()
font2=font.Font(None,36)
score=0

lost=0

display.set_caption('Shooter')
window=display.set_mode((win_w,win_h))
background=transform.scale(image.load(img_back),(win_w,win_h))



class GameSprite(sprite.Sprite):
    def __init__(self,iimage,x,y,speed):
        super().__init__()
        self.image = transform.scale(image.load(iimage),(65,65))
        self.speed=speed
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys [K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet=Bullet('bullet.png',self.rect.centerx,self.rect.top,-15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        global lost
        if self.rect.y > win_h:
            self.rect.x=randint(80,win_w-80)
            self.rect.y=0
            lost += 1 
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()

player= Player(img_hero ,5, win_h-100,10)

monsters=sprite.Group()
for i in range(5):
    monster=Enemy('ufo.png',randint(80,win_w-80),50,randint(1,5))
    monster.add(monsters)
bullets = sprite.Group()

finish=False

run = True
restart=font2.render('RESTART-key R',True,(255,255,255))
shoot=font2.render('shoot -space',True,(255,255,255))
win =font2.render('you win',True,(255,255,255))
lose=font2.render('you lose',True,(255,255,255))
while run:
    for e in event.get():
        if e.type ==QUIT:
            run=False
        if e.type ==KEYDOWN:
            if e.key ==K_SPACE: 
                fire_sound.play()
                player.fire()
            if e.key ==K_r:
                finish=False
                score=0
                lost=0
                for b in bullets:
                    b.kill()
                for m in monsters:
                    m.kill()
                for i in range(5):        
                    monster=Enemy('ufo.png',randint(80,win_w-80),50,randint(1,4))
                    monster.add(monsters)
    if not finish:     
        window.blit(background,(0,0))

       
    
        
       
        player.update()
        monsters.update()
        bullets.update()
        player.reset() 
        monsters.draw(window)
        bullets.draw(window)
        window.blit(shoot,(10,70))
        collides=sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score +=1
            monster=Enemy('ufo.png',randint(80,win_w-80),50,randint(1,4))
            monsters.add(monster)
            
        if sprite.spritecollide(player,monsters,False) or lost >=3:
            finish=True
            window.blit(lose,(200,200))
            window.blit(restart,(500,300))
        if score >=70:
            finish=True
            window.blit(win,(200,200)) 
            window.blit(restart,(500,300))       
        text_Q =font2.render(f'Сбито:{score}',1,(255,255,255)) 
        window.blit(text_Q,(10,50))
        text_lost = font2.render(f'Пропущено:{lost}',1,(255,255,255))
        window.blit(text_lost,(10,20))
        display.update() 
    time.delay(60)      

    