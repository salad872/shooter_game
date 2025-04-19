import pygame as pg 
from random import randint
import time
pg.init()

GREEN = (0, 255, 0)
RED = (255,0,0)
class Base_sprite(pg.sprite.Sprite):
    def __init__(self, filename, x, y, w, h, speed_x=0, speed_y=0):
      super().__init__()
      self.rect = pg.Rect(x, y, w, h)
      self.image = pg.transform.scale(pg.image.load(filename), (w, h))
      self.speed_x = speed_x
      self.speed_y = speed_y

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
          self.rect.x += self.speed_x
          self.rect.y += self.speed_y
      
class Health_bag(Base_sprite):
      def update(self):
            super().update()
            if self.rect.y > win_size[y]:
                  self.kill()
            if killed_ufos == 15:
                  time.sleep(5)

class Enemy(Base_sprite):
      def __init__(self, filename, x, y, w, h, speed_x=0, speed_y=0, 
                        y1=0, y2=0):
            super().__init__(filename, x, y, w, h, speed_x, speed_y)
            self.y1 = y1
            self.y2 = y2

class Star(Base_sprite):
      def update(self):
            super().update()
            if self.rect.y > win_size[y]:
                  self.kill()

class Ufo(Base_sprite):
      def update(self):
            super().update()
            global missed_ufos
            if self.rect.y > win_size[y]-50:
                  self.kill()
                  missed_ufos += 1
            if killed_ufos == 15:
                  self.kill() 

class Ufo2(Base_sprite):
      ufo_health = 2
      def update(self):
            super().update()
            if self.rect.y > win_size[y]-50:
                  self.kill()
                  missed_ufos += 1
            if killed_ufos == 15:
                  self.kill()

class Boss_ufo(Base_sprite):
      boss_health = 15
      def update(self):
            super().update()

class Hero(Base_sprite):
      energy = 0

      health = 100

      def fire(self):
            w = 56
            h = 70
            bullet = Bullet('laser.png',
                              self.rect.x + self.rect.width/2 - w/2,
                              self.rect.y - h, w, h,
                              speed_x = 0, speed_y = -10)
            bullets.add(bullet)
            all_sprite.add(bullet)
      
      def update(self):
            super().update()
            self.energy += 5
            self.draw_health()

      def draw_health(self):
            rect1 = pg.Rect(self.rect.x, self.rect.bottom, self.rect.width / 100 * self.health, 8)
            rect2 = pg.Rect(self.rect.x, self.rect.bottom, self.rect.width, 8)
            
            g = int(255/100*self.health)
            if g < 0 :
                  g = 0
            r = int(255 - g)
            b = 50
            pg.draw.rect(mw, (255,0,0), rect2)
            pg.draw.rect(mw, (r,g,b), rect1)
            

class Bullet(Base_sprite):
      def update(self):
            super().update()
            if self.rect.y > win_size[y]+ 50:
                  self.kill()

class Boom(pg.sprite.Sprite):
    def __init__(self, ufo_center, boom_sprites, booms) -> None:
        super().__init__() 
        #global booms, boom_sprites              
        self.frames = boom_sprites        
        self.frame_rate = 1   
        self.frame_num = 0
        self.image = boom_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = ufo_center
        self.add(booms)
        self.add(all_sprite)
    
    def next_frame(self):
        self.image = self.frames[self.frame_num]
        self.frame_num += 1
        if self.frame_num > len(self.frames)-1:
            self.frame_num = 0
        
    
    def update(self):
        self.next_frame()
        if self.frame_num == len(self.frames)-1:
            self.kill()

class Meteorite(pg.sprite.Sprite):
    def __init__(self, meteorite_sprites, meteors, x) -> None:
        super().__init__() 
        #global booms, boom_sprites              
        self.frames = meteorite_sprites 
        self.x = x  
        self.frame_rate = 1   
        self.frame_num = 0
        self.speed_x = randint(1, 3)
        self.speed_y = randint(1, 3)
        self.image = meteorite_sprites[0]
        self.rect = self.image.get_rect()
        self.add(meteors)
        self.add(all_sprite)
    
    def next_frame(self):
        self.image = self.frames[self.frame_num]
        self.frame_num += 1
        if self.frame_num > len(self.frames)-1:
            self.frame_num = 0
        
    
    def update(self):
        self.next_frame()
        if self.frame_num == len(self.frames)-1:
            self.kill()

def sprites_load(folder, file_name, size, colorkey=(0,0,0)):    
    sprites = []
    load = True
    num = 1
    while load:
        try:
            spr = pg.image.load(f'{folder}\\{file_name}{num}.png')
            spr = pg.transform.scale(spr,size)
            if colorkey: spr.set_colorkey(colorkey)
            sprites.append(spr)
            num += 1
        except:
            load = False
    return sprites

def set_text(text, x, y, color = (255, 255, 200)):
      mw.blit(
            font1.render(text, True, color),(x,y)
      )

def spawn_bag():
      x2 = randint(0, 1850)
      bag = Health_bag('pngtree-heal.png',x2 , 0, 70, 70, 0, 8)
      health_bags.add(bag)
      all_sprite.add(bag)                  

def spawn_star():
      size = randint(15, 30)
      star = Star('star.png', randint(0, win_size[x]), -10, size, size, 0, randint(2, 9))
      stars.add(star)
      all_sprite.add(star)

def spawn_ufo():
      ufo = Ufo('art.ufo.png', randint(0, win_size[x]-100), -100, 100, 100, 0, randint(1, 5))
      ufos.add(ufo)
      all_sprite.add(ufo)

def spawn_ufo2():
      ufo2 = Ufo2('cat-alien.png', randint(0, win_size[x]-100), -100, 100, 100, 0, randint(1, 6))
      ufos2.add(ufo2)
      all_sprite.add(ufo2)

def spawn_meteorite():
      size = randint (15, 40)
      meteor = Meteorite(meteorite_sprites, meteors, randint(0, win_size[x]))
      meteors.add(meteor)
      all_sprite.add(meteor)

def spawn_boss():
      size = (300, 200)
      boss = Boss_ufo('boss.png', 600, 0, size[0], size[1], 0, 1)
      all_sprite.add(boss)


win_size = (1920, 1080)
x, y =0, 1

mw = pg.display.set_mode(win_size, pg.FULLSCREEN)
caption = pg.display.set_caption('Лабиринт')

clock = pg.time.Clock()

background = pg.image.load('1140964.png')
background = pg.transform.scale(background, win_size)
lose_bg = pg.image.load('photo.jpg')
lose_bg = pg.transform.scale(lose_bg, win_size)

pg.mixer.music.load('space.ogg')
#pg.mixer.music.play()
kick = pg.mixer.Sound('fire.ogg')

#stars = []
#ufos = []
#bullets = []

boom_sprites = sprites_load('boom4', 'boom', (80, 80))
meteorite_sprites = sprites_load('meteor1', 'meteor', (40, 40))

stars = pg.sprite.Group()
ufos = pg.sprite.Group()
bullets = pg.sprite.Group()
booms = pg.sprite.Group()
meteors = pg.sprite.Group()
all_sprite = pg.sprite.Group()
ufos2 = pg.sprite.Group()
health_bags = pg.sprite.Group()
killed_ufos = 0
ufo_health = 2

font1 = pg.font.Font(None , 40)
hero = Hero('ship.png', 1000, 900, 120, 120)
all_sprite.add(hero)

play = True
win = False
game = True
ticks = 1
missed_ufos = 0
while play:
      for event in pg.event.get():
            if event.type == pg.QUIT:
                  play = False
            if event.type == pg.KEYDOWN:
                  if event.key == pg.K_LEFT:
                        hero.speed_x = -20
                  if event.key == pg.K_RIGHT:
                        hero.speed_x = 20
                  if event.key == pg.K_SPACE:
                        hero.fire()
                  if event.key == pg.K_UP:
                        play = False
            if event.type == pg.KEYUP:
                  if event.key == pg.K_LEFT:
                        hero.speed_x = 0
                  if event.key == pg.K_RIGHT:
                        hero.speed_x = 0

      

      if game:

            if ticks % 10 == 0:
                  spawn_star()

            if ticks % 80  == 0:
                  spawn_ufo()
                  if killed_ufos >=10:
                        if ticks % 120 == 0:
                              spawn_ufo2()
            if ticks % 480 == 0:
                  spawn_bag()      

            if ticks % 240 == 0:
                  spawn_meteorite()
            #if ticks % 60 == 0:
                  #spawn_meteorite()
                  
            if killed_ufos == 1:
                  spawn_boss()
                  

            mw.blit(background, (0, 0))

            # star in stars:
                  #star.update()
                  #star.draw()


            #for ufo in ufos:
             #     ufo.update()
              #    ufo.draw()
            all_sprite.update()
            all_sprite.draw(mw)

            if hero.rect.x >= win_size[x]-120 or hero.rect.x == win_size[x]-1920:
                  hero.speed_x = 0

            collides = pg.sprite.groupcollide(bullets, ufos, True, True)
            for bullet , ufo in collides.items():
                  Boom(ufo[0].rect.center, boom_sprites, booms)
                  killed_ufos += 1

            collides2 = pg.sprite.groupcollide(bullets, ufos2, True, False)
            for bullet , ufo2 in collides2.items():
                  ufo2[0].ufo_health -= 1
                  if ufo2[0].ufo_health == 0:   
                        Boom(ufo2[0].rect.center, boom_sprites, booms)
                        ufo2[0].kill()
                        killed_ufos += 1


            if pg.sprite.spritecollide(hero, ufos, False):
                  hero.health -= 0.5
                  if hero.health <= 0:
                        game = False
                        mw.blit(lose_bg, (0, 0))


            if pg.sprite.spritecollide(hero, health_bags, True):
                  hero.health = 100
                  if hero.health <= 0:
                        game = False
                        mw.blit(lose_bg, (0, 0))

            set_text(f'Пропущено: {missed_ufos}', 0, 0)
            set_text(f'Здоровье: {hero.health}', 220, 0)
            set_text(f'Убитых врагов: {killed_ufos}', 440, 0)
            #if missed_ufos > 100:
                  #game = False
                  #mw.blit(lose_bg, (0, 0))



            
      pg.display.update()
      clock.tick(120)
      ticks += 1