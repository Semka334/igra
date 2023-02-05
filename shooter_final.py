#Створи власний Шутер!

#Версія з касетою

from pygame import *
from random import randint

font.init()
font2 = font.SysFont('Arial', 32)
font_cd = font.SysFont('Arial', 14)

class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_width, player_height, player_image, player_x, player_y, player_speed):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.width = player_width
        self.height = player_height
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    sheels = 3
    max_sheels = 5
    kaset_cd = 70
    cd = 0
    cd_image = font_cd.render("Куля:100%", 1, (255, 255, 255))

    def update(self):
        if self.cd > 0:
            self.cd -= 1
            cd = str(100 - rocket.cd * 2)
            self.cd_image = font_cd.render("Куля:"+ cd +"%", 1, (255, 255, 255))

        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

        if keys[K_SPACE] and self.sheels > 0 and self.cd == 0:
            
            self.cd = 50
            self.cd_image = font_cd.render("Куля:0%", 1, (255, 255, 255))
            self.sheels -= 1

            x = rocket.rect.x + rocket.width / 2 - 10
            bullets_p.append(Bullet(20, 25, bullet_image, x , rocket.rect.y, -5))
        if self.sheels < self.max_sheels :
            if self.kaset_cd == 0:
                self.sheels += 1
                self.kaset_cd = 70
            if self.kaset_cd > 0:
                self.kaset_cd -= 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed


asteroid_image = "images/asteroid.png" 
bullet_image = "images/bullet.png"
galaxy_image = "images/galaxy.jpg"
rocket_image = "images/rocket.png"
ufo_image =    "images/ufo.png"

space_music = "music/space.ogg"

fire_sound = "sounds/fire.ogg"

bullets_p = []
monsters = []



win_width = 700
win_height = 500

rocket = Player(65, 80, rocket_image, win_width / 2, win_height - 100, 3)

window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load(galaxy_image), (win_width, win_height))
shell_image = transform.scale(image.load(bullet_image), (20, 25))


# музика
mixer.init()
mixer.music.load(space_music)
mixer.music.set_volume(0.05)
mixer.music.play()

fire = mixer.Sound(fire_sound)

Time = 0
text_time = font2.render("Час:"+str(Time), 1, (255, 255, 255))

lost = 0
text_lose = font2.render("Пропущено:"+str(lost), 1, (255, 255, 255))

score = 0
score_image = font2.render("Рахунок:"+str(score), 1, (255, 255, 255))

game = True

FPS = 60
clock = time.Clock()

monster_spawn_timer = 0

while game:
    window.blit(background, (0, 0))

    window.blit(text_time, (10, 70))
    window.blit(text_lose, (10, 10))
    window.blit(score_image, (10, 40))


    rocket.update()
    rocket.reset()

    window.blit(rocket.cd_image, (rocket.rect.x, rocket.rect.y + rocket.rect.height))
    a = rocket.sheels
    while a > 0:
        x = rocket.rect.x + rocket.rect.width + a * 5
        y = rocket.rect.y + rocket.rect.height
        window.blit(shell_image, ( x, y))
        a -= 1

    if monster_spawn_timer > 0:
        monster_spawn_timer -= 1
    elif monster_spawn_timer == 0 and len(monsters) < 5:
        monster_spawn_timer = randint(60 , 300)

        speed = randint(1, 3)
        x = randint(30, win_width - 100)
        
        monsters.append(Enemy(70, 50, ufo_image, x , -50, speed))

    for monster in monsters:
        monster.update()
        monster.reset()
        if monster.rect.y > win_height:
            lost += 1
            text_lose = font2.render("Пропущено:"+str(lost), 1, (255, 255, 255))
            monsters.remove(monster)


    for bullet in bullets_p:
        bullet.update()
        bullet.reset()

        delete_bullet = False
        for monster in monsters:
            
            if sprite.collide_rect(bullet, monster):
                score += monster.speed
                score_image = font2.render("Рахунок:"+str(score), 1, (255, 255, 255))
                monsters.remove(monster)
                delete_bullet = True
                break
        if delete_bullet:
            bullets_p.remove(bullet)
            continue

        while Time != FPS:
            Time += 1
            text_time = font2.render("Час:"+str(Time), 1, (255, 255, 255))

    


        '''
        for aster in asteroids:
            if sprite.collide_rect(bullet, aster):
                score += 2
                score_image = font2.render("Рахунок:"+str(score), 1, (255, 255, 255))
                asteroids.remove(aster)
                delete_bullet = True
                break
        if delete_bullet:
            bullets_p.remove(bullet)
            continue'''


    #keys = key.get_pressed()

    for e in event.get():
        if e.type == QUIT:
            game = False
    
    display.update()
    clock.tick(FPS)