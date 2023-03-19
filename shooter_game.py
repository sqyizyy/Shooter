from pygame import *
from time import time as timer
from random import randint
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
galaxy = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
window.blit(galaxy,(0,0))

 

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

score1 = 0
lost = 0
font.init()
font2 = font.SysFont('Arial', 30)
font1 = font.SysFont('Arial', 70)
win = font1.render('WIN', True, (255,215,0))
lose = font1.render('YOU LOSE', True, (255,0,0))

class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -=self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x +=self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 10, -10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0



rocket = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 4):
    asteroid  = Asteroid("asteroid.png", randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)


fired = 0
bullets = sprite.Group()  
life = 3
game = True
finish = False 
reload_time = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if fired < 5 and reload_time == False:
                    fire_sound.play()
                    fired = fired + 1
                    rocket.fire()
                if fired >= 5 and reload_time == False:
                    last_time = timer()
                    reload_time = True
    if finish != True:
        window.blit(galaxy,(0,0))
        rocket.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        rocket.reset()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)
        rocket.reset()
        score = font2.render('Счет:'+ str(score1),1,(255,255,255))
        window.blit(score,(10,20))
        miss = font2.render('Пропущено:' + str(lost),1,(255,255,255))
        window.blit(miss,(10,50))
        if reload_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("Wait, reload...", 1, (150,0,0))
                window.blit(reload, (260, 460))
            else:
                fired = 0
                reload_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score1 = score1 + 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 75, 75,randint(1, 5))
            monsters.add(monster)
        if score1 >= 10:
            finish = True
            window.blit(win, (200,200))
        if sprite.spritecollide(rocket, monsters, False) or sprite.spritecollide(rocket, asteroids, False):
            sprite.spritecollide(rocket, monsters, True)
            sprite.spritecollide(rocket, asteroids, True)
            life = life -1
        if life == 3:
            life_color = (0,255,0)
        if life== 2:
            life_color = (255,255,0)
        if life == 1:
            life_color = (255,0,0)
        lifes = font1.render(str(life),1, life_color)
        window.blit(lifes, (650, 10))

        if life == 0 or lost >= 3:
            finish = True
            window.blit(lose, (200,200))







    display.update()
    clock.tick(FPS)
