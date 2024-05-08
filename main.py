from pygame import *
from random import randint
from time import time as timer

init()

W = 700
H = 700

window = display.set_mode((W, H))
display.set_caption("Shooter")
display.set_icon(image.load('images/asteroid.png'))

bg = transform.scale(image.load('images/galaxy.jpg'), (W, H))
clock = time.Clock()

mixer.init()
mixer.music.load('sounds/space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()

fire_snd = mixer.Sound('sounds/fire.ogg')

font.init()
font1 = font.Font('fonts/Konstancia.ttf', 35)
font2 = font.Font('fonts/Konstancia.ttf', 50)
font3 = font.SysFont('fonts/Konstancia.ttf', 100, bold = True)



#базовий клас для всіх спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу з властивостями
    def __init__(self, img, x, y, width, height, speed):
        super().__init__()
        self.width = width
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    #метод для малювання спрайту
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#клас для гравця
class Player(GameSprite):
    def update(self):
        '''метод для  управління гравцем'''
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < W - self.width:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('images/bullet.png', self.rect.centerx, self.rect.top, 15, 40, 10)
        bullets.add(bullet)

class Asteroid(GameSprite):
    def update(self):
        global lost, count, speed_x
        self.rect.y += self.speed
        self.rect.x += speed_x
        count += 1
        if count == 100:
            count = 0
            speed_x *= -1
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(0, W - self.width)
     
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(0, W - self.width)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
 
player = Player('images/rocket.png', 0, H-100, 80, 100, 8)
asteroids = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
for i in range (5):
    enemy = Enemy('images/ufo.png', randint(0, W-50), 0, 80, 50, randint(1, 2))
    monsters.add(enemy)

for i in range(3):
    asteroid = Asteroid('images/asteroid.png', randint(0, 50), 0, 80, 50, randint(2, 5))                
    asteroids.add(asteroid) 

num_fire = 0
rel_time = False   
speed_x = 3
count = 0
lost = 0
killed = 0
life = 3
life_color = (0, 255, 0)
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 7 and rel_time is False:
                    player.fire()
                    fire_snd.play()
                    num_fire += 1
                if num_fire > 7 and rel_time is False:
                    rel_time = True
                    start_time = timer()
        

    if finish is not True:
        window.blit(bg, (0, 0))

        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()

        if rel_time:
            end_time = timer()
            if end_time - start_time >= 2:
                rel_time = False
                num_fire = 0 
            else:
                reload_txt = font1.render('Перезарядка...', True, (255, 0, 0))
                window.blit(reload_txt, (300, 500))

        if sprite.spritecollide(player, monsters, True):
            life -= 1
            enemy = Enemy('images/ufo.png', randint(0, W-50), 0, 80, 50, randint(1, 2))
            monsters.add(enemy)
            
        if sprite.spritecollide(player, asteroids, True):
            life -= 1
            asteroid = Asteroid('images/asteroid.png', randint(0, 50), 0, 80, 50, randint(2, 5))                
            asteroids.add(asteroid) 
        monsters_collide = sprite.groupcollide(monsters, bullets, True, True)
        for monster in monsters_collide:
            enemy = Enemy('images/ufo.png', randint(0, W-50), 0, 80, 50, randint(1, 2))
            monsters.add(enemy)
            killed += 1



        if life == 0 or lost > 5:
            finish = True
            mixer.music.pause()
            lose_txt = font3.render('Ти програв!', True, (255, 0, 0))
            window.blit(lose_txt, (150, 300))

        if killed > 10:
            finish = True
            mixer.music.pause()
            win_txt = font3.render('Ти виграв !', True, (0, 255, 0))
            window.blit(win_txt, (150, 300))

        if life == 3:
            life_color = (0, 255, 0)
        if life == 2:
            life_color = (235, 245, 47)
        if life == 1:
            life_color = (255, 0, 0)
            
            


        lost_txt = font2.render('Пропущено:' + str(lost), True, (0, 255, 0))
        window.blit(lost_txt, (15, 15))

        killed_txt = font2.render('Збито:' + str(killed), True, (0, 255, 0))
        window.blit(killed_txt, (15, 50))

        life_txt = font2.render(str(life), True, (life_color))
        window.blit(life_txt, (640, 15))
    else:
        keys_pressed = key.get_pressed()
        if keys_pressed[K_ESCAPE]:
            life = 10
            killed = 0
            lost = 0
            for m in monsters:
               m.kill()
            for b in bullets:
               b.kill()
            for i in range (5):
                enemy = Enemy('images/ufo.png', randint(0, W-50), 0, 80, 50, randint(1, 2))
                monsters.add(enemy)
            mixer.music.play()
            finish = False   

        
    


    display.update()
    clock.tick(100)