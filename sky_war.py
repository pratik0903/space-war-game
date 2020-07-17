import pygame
import random
import sys
random_vel_increase=[0,1,2,3]
win=pygame.display.set_mode((500,500))
pygame.display.set_caption('sky wars')
pygame.init()
class war_ship:
    def __init__(self,x,y,width,height,color):
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.color=color
        self.vel=10
    def draw(self):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
        pygame.display.update()

class projectile:
    bullet_count_total=3
    def __init__(self,x,y,radius):
        self.x=x
        self.y=y
        self.vel=10
        self.radius=radius
    @classmethod
    def bullet_addup(cls):
        if(bullet_count_total<7):
            cls.bullet_count_total+=1
    @classmethod
    def return_bullet_count(cls):
        return cls.bullet_count_total
    def draw(self,win):
        pygame.draw.circle(win,(255,255,255),(self.x,self.y),self.radius)

class enemy:
    def __init__(self,x,y,width,height,vel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=8+vel
        self.health=100
        self.visible=True

    def move(self,win):
        if(self.y!=500):
            if(self.x+self.width+self.vel>500):
                # print('touched boundry')
                self.x=0
                self.y+=self.height
            self.x=self.x+self.vel
            #print(self.x,self.y,self.visible)
            pygame.draw.rect(win,(0,255,0),(self.x,self.y,self.width,self.height))

    def hit(self):
        if(self.health>0):
            self.health-=10
        else:
            self.visible=False
#level class and lvl variable for doing alien list size manipulation
class level:
    def __init__(self):
        self.lev=1
    def increment(self):
        self.lev+=1

def redraw_win():
    win.fill((0,0,0))
    text=font.render("Score : "+str(score),1,(255,255,255))
    win.blit(text,(350,10))
    ship.draw()

    for alien in alien_list:
        if(alien.visible):
            alien.move(win)
        else:
            alien_list.pop(alien_list.index(alien))
            lvl.increment()
            projectile.bullet_addup()
            print(projectile.return_bullet_count())
            # print('length',len(alien_list),"level",lvl.lev)

    for bullet in bullets:
        bullet.draw(win)

#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
run=True
score=0
lvl=level()
ship=war_ship(0,450,50,50,(255,0,0))
alien=enemy(0,0,50,50,lvl.lev)
alien_list=[]
bullets=[]
len_alien_list=0
 #initial count
bullet_count_total=5
while run:
    pygame.time.delay(100)
    # alien.move(win)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    keys=pygame.key.get_pressed()

    while(len(alien_list)<lvl.lev):
        alien_list.append(enemy(0,0,50,50,(lvl.lev+random.choice(random_vel_increase)) ))
        # for alien in alien_list:
            # print(alien.x,alien.y,alien.width,alien.height,alien.vel)

    for alien in alien_list:
        for bullet in bullets:
            if(bullet.y>alien.y and bullet.y<alien.y+alien.height):
                if(bullet.x>alien.x and bullet.x<alien.x+alien.width):
                    #print("bullet hit alien ship")
                    alien.hit()
                    score+=10
                    print(alien.health,alien.visible)
                    bullets.pop(bullets.index(bullet))
            if(bullet.y>0):
                bullet.y-=bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

    if(keys[pygame.K_RIGHT]):
        if(ship.x+ship.width+ship.vel<500):
            ship.x+=ship.vel
        else:
            ship.x=500-ship.width

    if(keys[pygame.K_LEFT]):
        if(ship.x-ship.vel>0):
            ship.x-=ship.vel
        else:
            ship.x=0
    if(keys[pygame.K_UP]):
        if(ship.y-ship.vel>0):
            ship.y-=ship.vel
        else:
            ship.y=0
    if(keys[pygame.K_DOWN]):
        if(ship.y+ship.height+ship.vel<500):
            ship.y+=ship.vel
        else:
            ship.y=500-ship.height
    if(keys[pygame.K_SPACE]):
        if(len(bullets)<projectile.return_bullet_count()):
            bullets.append(projectile(round(ship.x+round(ship.width/2)),round(ship.y),3))

    redraw_win()

    pygame.display.update()
    for alien in alien_list:
        if(alien.visible):
            if(round(ship.y+(ship.height/2))>alien.y and round(ship.y+(ship.height/2)) < alien.y+alien.height):
                if(round(ship.x+(ship.width/2))>alien.x and round(ship.x+(ship.width/2)) < alien.x+alien.width):
                    score-=50
                    print('hit',alien.x,alien.y)
            if(alien.x+alien.width==500 and alien.y+alien.width==500):
                run=False
                print("you lose")
                print('Your final score is :',score)
pygame.quit()
