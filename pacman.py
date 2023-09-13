import pygame
import sys
import math
import os

#pathname used for loading objects from folders
pathName = os.path.realpath(os.path.dirname(__file__))
print(f"Current Directory: {pathName}")

#Player
class Pacman():
    #initiate pacman
    def __init__(self):
        #timers
        self.now = pygame.time.get_ticks()
        self.animationTimer = self.now
        self.spriteUpdateCooldown = 50
        #pos
        self.x = 227
        self.y = 405
        self.pastX = self.y
        self.pastY = self.y
        self.pacPos = [self.x,self.y]
        #sprite
        self.pacBox = [34*scale,1*scale,13*scale,13*scale]
        self.pacmanSpriteSheetXPos = 18
        self.pacmanSpriteSheetYPos = 1
        self.spriteCount = 3
        #hitbox
        self.hitbox = pygame.Rect(self.x-3,self.y-3,16*scale,16*scale)
        self.dotHitbox = pygame.Rect(1000,1000,1,1)
        self.keyPressed = pygame.key.get_pressed()
        self.direction = 0
        self.nextDirection = -1
        self.speed = 2
    #draw pacman
    def draw(self):
        window.blit(spriteSheet, self.pacPos, self.pacBox)
        #draw hitboxes around pacman
        if showHitboxes:
            #pacman hitbox
            pygame.draw.rect(window,(160,32,240),self.hitbox,width = 1)
            #pacdots kill range
            pygame.draw.rect(window,(160,32,240),self.dotHitbox,width = 1)
            #orange ghost flee range
            pygame.draw.circle(window, (160,32,240), (self.pastX+10,self.pastY+10), 100, 1)
            
    #update pacman
    def move(self):
        #update hitbox position and current pressed key as well as if colliding with a wall
        self.keyPressed = pygame.key.get_pressed()
        self.pacPos = [self.x,self.y]
        self.hitbox = pygame.Rect(self.x-3,self.y-3,16*scale,16*scale)
        self.collidedWithWall = False
        self.now = pygame.time.get_ticks()
        
        #depending on which key is pressed, set the next direction of the player
        if self.keyPressed[pygame.K_LEFT]:
            self.nextDirection = 0
        if self.keyPressed[pygame.K_RIGHT]:
            self.nextDirection = 1
        if self.keyPressed[pygame.K_UP]:
            self.nextDirection = 2
        if self.keyPressed[pygame.K_DOWN]:
            self.nextDirection = 3

        
        #check if can change current direction
        #if moving left causes a wall collision, do not turn left, otherwise turn left
        if self.nextDirection == 0: #LEFT
            #simulate a temp movement to the left
            self.x -= self.speed
            self.hitbox = pygame.Rect(self.x-3,self.y-3,16*scale,16*scale)
            #if this temp movement collides with a wall, undo movement and do not change direction
            for i in range(len(wallHitBox)):
                if pygame.Rect.colliderect(self.hitbox, wallHitBox[i]):
                    self.collidedWithWall = True
            if self.collidedWithWall == True:
                self.x += self.speed
                self.collidedWithWall = False
            #if it doesnt collide, change the direction and undo the temp movement
            else:
                self.x += self.speed
                self.collidedWithWall = False
                self.direction = self.nextDirection
        
        #if moving right causes a wall collision, do not turn right, otherwise turn right
        elif self.nextDirection == 1: #RIGHT
            self.x += self.speed
            self.hitbox = pygame.Rect(self.x-3,self.y-3,16*scale,16*scale)
            for i in range(len(wallHitBox)):
                if pygame.Rect.colliderect(self.hitbox, wallHitBox[i]):
                    self.collidedWithWall = True
            if self.collidedWithWall == True:
                self.x -= self.speed
                self.collidedWithWall = False
            else:
                self.x -= self.speed
                self.collidedWithWall = False
                self.direction = self.nextDirection
        
        #if moving up causes a wall collision, do not turn up, otherwise turn up
        elif self.nextDirection == 2: #UP
            self.y -= self.speed
            self.hitbox = pygame.Rect(self.x-3,self.y-3,16*scale,16*scale)
            for i in range(len(wallHitBox)):
                if pygame.Rect.colliderect(self.hitbox, wallHitBox[i]):
                    self.collidedWithWall = True
            if self.collidedWithWall == True:
                self.y += self.speed
                self.collidedWithWall = False
            else:
                self.y += self.speed
                self.collidedWithWall = False
                self.direction = self.nextDirection
        
        #if moving down causes a wall collision, do not turn down, otherwise turn down
        elif self.nextDirection == 3: #DOWN
            self.y += self.speed
            self.hitbox = pygame.Rect(self.x-3,self.y-3,16*scale,16*scale)
            for i in range(len(wallHitBox)):
                if pygame.Rect.colliderect(self.hitbox, wallHitBox[i]):
                    self.collidedWithWall = True
            if self.collidedWithWall == True:
                self.y -= self.speed
                self.collidedWithWall = False
            else:
                self.y -= self.speed
                self.collidedWithWall = False
                self.direction = self.nextDirection
        
        #reset hitbox
        self.hitbox = pygame.Rect(self.x-3,self.y-3,16*scale,16*scale)


        #check if player is colliding with a wall
        for i in range(len(wallHitBox)):
            if pygame.Rect.colliderect(self.hitbox, wallHitBox[i]):
                self.collidedWithWall = True
                break


        #update current sprite seletec
        if self.now - self.animationTimer > self.spriteUpdateCooldown:
            self.spriteCount += 1
            if self.spriteCount == 5:
                self.spriteCount = 1
        
        #update what the location of the sprite we want to draw on screen is depending on the cooldown of the sprite updating
        if self.spriteCount != 4:
            if self.spriteCount == 1 and (self.now - self.animationTimer > self.spriteUpdateCooldown):
                self.animationTimer = self.now
                self.pacmanSpriteSheetXPos = 18
            elif self.spriteCount == 2 and (self.now - self.animationTimer > self.spriteUpdateCooldown):
                self.animationTimer = self.now
                self.pacmanSpriteSheetXPos = 2
            elif self.spriteCount == 3 and (self.now - self.animationTimer > self.spriteUpdateCooldown):
                self.animationTimer = self.now
                self.pacmanSpriteSheetXPos = 18

            if self.direction == 0:
                self.pacmanSpriteSheetYPos = 17
            elif self.direction == 1:
                self.pacmanSpriteSheetYPos = 1
            elif self.direction == 2:
                self.pacmanSpriteSheetYPos = 33
            elif self.direction == 3:
                self.pacmanSpriteSheetYPos = 49
        elif self.now - self.animationTimer > self.spriteUpdateCooldown:
            self.animationTimer = self.now
            self.pacmanSpriteSheetYPos = 1
            self.pacmanSpriteSheetXPos = 34
        

        #if not colliding with a wall
        if not self.collidedWithWall:
            #stop animation if hit a wall
            if self.pastY == self.y and self.pastX == self.x:
                if self.direction == 0:
                    self.pacmanSpriteSheetYPos = 17
                elif self.direction == 1:
                    self.pacmanSpriteSheetYPos = 1
                elif self.direction == 2:
                    self.pacmanSpriteSheetYPos = 33
                elif self.direction == 3:
                    self.pacmanSpriteSheetYPos = 49
                self.pacmanSpriteSheetXPos = 18

            #player can move so we update captured x pos
            if self.pastX != self.x:
                self.pastX = self.x 

            if self.pastY != self.y:
                self.pastY = self.y

            

                
            #move players actual x pos
            if self.direction == 0:
                self.x -= self.speed
            if self.direction == 1 :
                self.x += self.speed
            if self.direction == 2:
                self.y -= self.speed
            if self.direction == 3:
                self.y += self.speed
        else:
            #stop animation if hit wall
            if self.direction == 0:
                self.pacmanSpriteSheetYPos = 17
            elif self.direction == 1:
                self.pacmanSpriteSheetYPos = 1
            elif self.direction == 2:
                self.pacmanSpriteSheetYPos = 33
            elif self.direction == 3:
                self.pacmanSpriteSheetYPos = 49
                
            self.pacmanSpriteSheetXPos = 18

            #if colliding with wall:
            #fix wall collision by going to last captured pos that way is no longer colliding with wall
            self.x = self.pastX
            self.y = self.pastY
            self.pacPos = [self.x,self.y]
            self.hitbox = pygame.Rect(self.x-3,self.y-3,16*scale,16*scale)
            self.collidedWithWall = False
            
        #teleport player if leaves map
        if self.x > width:
            self.x = 0-30
        if self.x < -39:
            self.x = width



        #fix dot hitbox
        self.dotHitbox = pygame.Rect(self.pastX+6,self.pastY+6,14,14)
        #fix where pacman sprite is found
        self.pacBox = [self.pacmanSpriteSheetXPos*scale,self.pacmanSpriteSheetYPos*scale,13*scale,13*scale]


            
class Ghost():
    def __init__(self, types):
        
        #pos and sprite
        #sprite
        self.types = types
        self.animationframe = 0
        self.moveAnimation = 16
        self.spriteDirection = 32
        self.now = pygame.time.get_ticks()
        self.animationTime = self.now
        self.lastChecked = self.now
        self.introwait = self.now
        self.mode = "Intro"
        self.direction = 0
        self.freezeTimer = 0
        #depending on type go to different pos and have a different target corner for when pacman is powered up as well as dif sprite
        if self.types == 1:
            #do corner movement phase
            self.mode = "JustRun"
            self.x = 222
            self.y = 220
            self.color = (255,0,0)
            self.ghostBox = [0*scale,63*scale,16*scale,16*scale]
            self.yfix = 0
            self.cornerx = 0000
            self.cornery = 40000000
        if self.types == 2:
            self.direction = 3
            self.x = 190
            self.y = 265
            self.color = (0,255,255)
            self.ghostBox = [0*scale,97*scale,16*scale,14*scale]
            self.yfix = 4
            self.cornerx = 0000
            self.cornery = 40000000
        elif self.types == 3:
            self.direction = 2
            self.x = 222
            self.y = 265
            self.color = (255,192,203)
            self.ghostBox = [0*scale,81*scale,16*scale,14*scale]
            self.yfix = 4
            self.cornerx = 0000
            self.cornery = 40000000
        elif self.types == 4:
            self.direction = 3
            self.x = 256
            self.y = 265
            self.color = (255,165,0) 
            self.ghostBox = [0*scale,113*scale,16*scale,14*scale]
            self.yfix = 4
            self.cornerx = 24
            self.cornery = 500
        self.pastX = self.x
        self.pastY = self.y
        self.origonalX = self.x
        self.origonalY = self.y
        self.ghostPos = [self.x,self.y]
        self.hitbox = pygame.Rect(self.x+2,self.y+2,16*scale,16*scale)
        self.frames = 0
        
        #collision
        self.nextDirection = self.direction
        self.keyPressed = pygame.key.get_pressed()
        self.speed = 1.8
        self.correctHitbox = 2-self.speed #(annoying hitbox fix for ghosts cause they have dif speed)

        #movement
        self.cangoleft = True
        self.cangoright = True
        self.cangoup = True
        self.cangodown = True

        #power
        self.powerupcooldown = self.now

        #pacman information
        self.pacstorex = 0
        self.pacstorey = 0
        self.storedX = self.pastX
        self.storedY = self.pastY
        self.pacDistX = self.x-self.pacstorex
        self.pacDistY = self.y-self.pacstorey

    #draw ghosts
    def draw(self):
        self.now = pygame.time.get_ticks()
        window.blit(spriteSheet, (self.ghostPos[0],self.ghostPos[1]+self.yfix), self.ghostBox)
        if showHitboxes:
            pygame.draw.rect(window,(160,32,240),self.hitbox,width = 1)
    
    #update ghosts
    def move(self):
        self.keyPressed = pygame.key.get_pressed()
        self.ghostPos = [self.x,self.y]
        self.hitbox = pygame.Rect(self.x+2,self.y+2,16*scale,16*scale)
        self.collidedWithWall = False
        
        #fix some stuttering with the x and y dist trackers
        if not self.mode == "Run4Life" or self.mode == "JustRun":
            if self.now - self.animationTime > 100:
                if self.animationframe == 0:
                    self.animationframe += 1
                else:
                    self.animationframe = 0
                self.animationTime = self.now
        
        #if not being ressed or start of game mode
        if not self.mode == "Intro" and self.mode != "Res":
            if self.frames == 0:
                #fix sprite y pos for ghosts
                if self.mode == "Chase":
                    if self.types != 1:
                        self.yfix = 4
                    else:
                        self.yfix = 0
                    #define where pacman is on screen
                    self.pacstorex = pacmans[0].x - 4.2
                    self.pacstorey = pacmans[0].y - 5.0
                elif self.mode == "Run4Life" or self.mode == "JustRun" or self.mode == "Coward":
                    #pretend that pacman is in a corner and force ghosts to chase a fakse pacman to menuver them into their repsective corners
                    if self.types == 1:
                        self.pacstorex = 350
                        self.pacstorey = -1000
                    if self.types == 3:
                        self.pacstorex = 100
                        self.pacstorey = -1000
                    if self.types == 4:
                        self.pacstorex = 400
                        self.pacstorey = 1000
                self.frames = 1
            else:
                self.frames = 0
                

            #what to start sprite x pos on depending on direction
            if self.direction == 0:
                self.spriteDirection = 32
            elif self.direction == 1:
                self.spriteDirection = 0
            if self.direction == 2:
                self.spriteDirection = 64
            elif self.direction == 3:
                self.spriteDirection = 96


            #if pacman is too close to orange ghosts, make him flee
            if self.types == 4:
                self.pacFullDist = round(math.sqrt((self.pastX-self.pacstorex)**2 + (self.pastY-self.pacstorey)**2),1)
                if self.pacFullDist < 100 and self.mode != "Run4Life" and self.mode != "Eaten" and self.mode != "Res":
                    self.mode = "Coward"
                elif self.pacFullDist > 100 and self.mode != "Run4Life" and self.mode != "Eaten" and self.mode != "Res":
                    self.mode = "Chase"

            #movement predictions
            if self.mode == 'Chase' or self.mode == "JustRun" or self.mode == "Run4Life":
                #red or orange
                if self.types == 1 or self.types == 4:
                    #update where they are trying to get to
                    self.pacDistX = self.pastX-self.pacstorex
                    self.pacDistY = self.pastY-self.pacstorey
                    if showHitboxes == True:
                        pygame.draw.line(window,self.color, (self.pastX+17,self.pastY+17),(self.pacstorex+17, self.pacstorey+17),2)
                    
                    #change sprite type depending on character
                    if self.types == 1:
                        if self.animationframe == 0:
                            self.ghostBox = [(0+self.spriteDirection+self.moveAnimation)*scale,63*scale,16*scale,16*scale]
                        elif self.animationframe == 1:
                            self.ghostBox = [(0+self.spriteDirection)*scale,63*scale,16*scale,16*scale]
                    elif self.types == 4:
                        if self.animationframe == 0:
                            self.ghostBox = [(0+self.spriteDirection+self.moveAnimation)*scale,113*scale,16*scale,14*scale]
                        elif self.animationframe == 1:
                            self.ghostBox = [(0+self.spriteDirection)*scale,113*scale,16*scale,14*scale]
                            
                #blue ghost
                elif self.types == 2:
                    #update blues target
                    self.pacDistX = inkytargetx
                    self.pacDistY = inkytargety
                    
                    if showHitboxes == True:
                        pygame.draw.line(window,self.color, (self.pastX+17,self.pastY+17),(self.pacDistX, self.pacDistY),2)
                    #update blue sprite
                    if self.animationframe == 0:
                        self.ghostBox = [(0+self.spriteDirection+self.moveAnimation)*scale,97*scale,16*scale,14*scale]
                    elif self.animationframe == 1:
                        self.ghostBox = [(0+self.spriteDirection)*scale,97*scale,16*scale,14*scale]
                #pink ghost
                elif self.types == 3:
                    #depending on direction, chase the space a bit infront of pacman
                    if pacmans[0].direction == 0:
                        self.pacDistX = self.pastX-self.pacstorex-70
                        self.pacDistY = self.pastY-self.pacstorey+20
                        if showHitboxes == True:
                            pygame.draw.line(window,self.color, (self.pastX+17,self.pastY+17),(self.pacstorex-70, self.pacstorey+20),2)
                    if pacmans[0].direction == 1:
                        self.pacDistX = self.pastX-self.pacstorex+90
                        self.pacDistY = self.pastY-self.pacstorey+20
                        if showHitboxes == True:
                            pygame.draw.line(window,self.color, (self.pastX+17,self.pastY+17),(self.pacstorex+90, self.pacstorey+20),2)
                    if pacmans[0].direction == 2:
                        self.pacDistX = self.pastX-self.pacstorex+20
                        self.pacDistY = self.pastY-self.pacstorey-70
                        if showHitboxes == True:
                            pygame.draw.line(window,self.color, (self.pastX+17,self.pastY+17),(self.pacstorex+20, self.pacstorey-70),2)
                    if pacmans[0].direction == 3:
                        self.pacDistX = self.pastX-self.pacstorex+20
                        self.pacDistY = self.pastY-self.pacstorey+90
                        if showHitboxes == True:
                            pygame.draw.line(window,self.color, (self.pastX+17,self.pastY+17),(self.pacstorex+20, self.pacstorey+90),2)
                    #pink sprite
                    if self.animationframe == 0:
                        self.ghostBox = [(0+self.spriteDirection+self.moveAnimation)*scale,81*scale,16*scale,14*scale]
                    elif self.animationframe == 1:
                        self.ghostBox = [(0+self.spriteDirection)*scale,81*scale,16*scale,14*scale]
            #if orange ghosts is too close to pacman
            else:
                if self.types == 4 and self.mode == "Coward":
                    #update their target and sprite
                    self.pacDistX = self.pastX-self.cornerx
                    self.pacDistY = self.pastY-self.cornery
                    if self.animationframe == 0:
                        self.ghostBox = [(0+self.spriteDirection+self.moveAnimation)*scale,113*scale,16*scale,14*scale]
                    elif self.animationframe == 1:
                        self.ghostBox = [(0+self.spriteDirection)*scale,113*scale,16*scale,14*scale]

                    if showHitboxes == True:
                        pygame.draw.line(window,(255,255,0), (self.pastX+17,self.pastY+17),(self.cornerx, self.cornery),2)

                
            #if the ghost is eaten by pacman
            if self.mode == "Eaten":
                #update target pos and sprite
                self.yfix = 0
                self.pacDistX = self.pastX-234
                self.pacDistY = self.pastY-283

                #if the ghost is above the respawn chamber update its mode
                if self.x > 220 and self.x < 222 and self.y >= 209 and self.y < 285 :
                    self.x = 222
                    self.y = 220
                    self.mode = "Res"
                if showHitboxes == True:
                    pygame.draw.line(window,(255,255,0), (self.pastX+17,self.pastY+17),(235, 283),2)
                #update sprite based on direction
                if self.direction == 0:
                    self.spriteDirection = 16
                elif self.direction == 1:
                    self.spriteDirection = 0
                elif self.direction == 2:
                    self.spriteDirection = 32
                elif self.direction == 3:
                    self.spriteDirection = 48
                    
                self.ghostBox = [(129+self.spriteDirection)*scale,79*scale,16*scale,16*scale]

            #based on the x and y distence the ghosts are from their target, make a distence for them to detect how close/far they are
            self.pacFullDist = round(math.sqrt(((self.pacDistX)**2 + self.pacDistY**2)),1)
            
            

            


            #direction handeling
            #check if can go left
            #simulate a left movement, if they collide with a wall they cant go left, otherwise they can. This is the same for each direction
            self.x -= self.speed + self.correctHitbox
            self.hitbox = pygame.Rect(self.x+2,self.y+2,16*scale,16*scale)
            for i in range(len(wallHitBox)):
                if pygame.Rect.colliderect(self.hitbox, wallHitBox[i]):
                    self.collidedWithWall = True
                    break
            if self.collidedWithWall == True:
                self.x += self.speed + self.correctHitbox
                self.collidedWithWall = False
                self.cangoleft = False
            else:
                self.x += self.speed + self.correctHitbox
                self.collidedWithWall = False
                self.cangoleft = True

            #check if can go right
            self.x += self.speed + self.correctHitbox
            self.hitbox = pygame.Rect(self.x+2,self.y+2,16*scale,16*scale)
            for i in range(len(wallHitBox)):
                if pygame.Rect.colliderect(self.hitbox, wallHitBox[i]):
                    self.collidedWithWall = True
            if self.collidedWithWall == True:
                self.x -= self.speed + self.correctHitbox
                self.collidedWithWall = False
                self.cangoright = False
            else:
                self.x -= self.speed + self.correctHitbox
                self.collidedWithWall = False
                self.cangoright = True
            
            #check if can go up
            self.y -= self.speed + self.correctHitbox
            self.hitbox = pygame.Rect(self.x+2,self.y+2,16*scale,16*scale)
            for i in range(len(wallHitBox)):
                if pygame.Rect.colliderect(self.hitbox, wallHitBox[i]):
                    self.collidedWithWall = True
                    break
            if self.collidedWithWall == True:
                self.y += self.speed + self.correctHitbox
                self.collidedWithWall = False
                self.cangoup = False
                    
            else:
                self.y += self.speed + self.correctHitbox
                self.collidedWithWall = False
                self.cangoup = True
            
            #check if can go down
            self.y += self.speed + self.correctHitbox
            self.hitbox = pygame.Rect(self.x+2,self.y+2,16*scale,16*scale)
            for i in range(len(wallHitBox)):
                if pygame.Rect.colliderect(self.hitbox, wallHitBox[i]):
                    self.collidedWithWall = True
                    break
            if self.collidedWithWall == True:
                self.y -= self.speed + self.correctHitbox
                self.collidedWithWall = False
                self.cangodown = False
                    
            else:
                self.y -= self.speed + self.correctHitbox
                self.collidedWithWall = False
                self.cangodown = True
            

            #cant go backwards to catch pacman
            if self.direction == 0:
                self.cangoright = False
            if self.direction == 1:
                self.cangoleft = False
            if self.direction == 2:
                self.cangodown = False
            if self.direction == 3:
                self.cangoup = False



           
            #store current x and y pos to check if stuck every 150 seconds
            if self.now - self.lastChecked > 150:
                self.storedX = self.pastX
                self.storedY = self.pastY
                self.lastChecked = self.now

            #help

            #basicallt it checks which direction its best go to based on which way is faster to get to their target and which way they can and cant go, as well as making sure they are not stuck
            if not (self.storedX == self.pastX and self.storedY == self.pastY):
                #better to go left?
                if self.cangoleft and round(math.sqrt(((self.pacDistX-self.speed)**2 + (self.pacDistY)**2)),1) < round(math.sqrt(((self.pacDistX + self.speed)**2 + (self.pacDistY)**2)),1) and (self.cangoup and round(math.sqrt(((self.pacDistX-self.speed)**2 + (self.pacDistY)**2)),1) < round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY-self.speed)**2)),1)):
                    self.direction = 0
                elif self.cangoleft and round(math.sqrt(((self.pacDistX-self.speed)**2 + self.pacDistY**2)),1) < round(math.sqrt(((self.pacDistX + self.speed)**2 + self.pacDistY**2)),1) and not self.cangoup:
                    self.direction = 0
                elif self.cangoleft and round(math.sqrt(((self.pacDistX-self.speed)**2 + self.pacDistY**2)),1) < round(math.sqrt(((self.pacDistX + self.speed)**2 + self.pacDistY**2)),1) and (self.cangodown and round(math.sqrt(((self.pacDistX-self.speed)**2 + (self.pacDistY)**2)),1) < round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY+self.speed)**2)),1)):
                    self.direction = 0
                elif self.cangoleft and round(math.sqrt(((self.pacDistX-self.speed)**2 + self.pacDistY**2)),1) < round(math.sqrt(((self.pacDistX + self.speed)**2 + self.pacDistY**2)),1) and not self.cangodown:
                    self.direction = 0

                #better to go right?
                elif self.cangoright and round(math.sqrt(((self.pacDistX+self.speed)**2 + self.pacDistY**2)),1) < round(math.sqrt(((self.pacDistX - self.speed)**2 + self.pacDistY**2)),1) and (self.cangoup and round(math.sqrt(((self.pacDistX+self.speed)**2 + (self.pacDistY)**2)),1) < round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY-self.speed)**2)),1)):
                    self.direction = 1
                elif self.cangoright and round(math.sqrt(((self.pacDistX+self.speed)**2 + self.pacDistY**2)),1) < round(math.sqrt(((self.pacDistX - self.speed)**2 + self.pacDistY**2)),1) and not self.cangoup:
                    self.direction = 1
                elif self.cangoright and round(math.sqrt(((self.pacDistX+self.speed)**2 + self.pacDistY**2)),1) < round(math.sqrt(((self.pacDistX - self.speed)**2 + self.pacDistY**2)),1) and (self.cangodown and round(math.sqrt(((self.pacDistX+self.speed)**2 + (self.pacDistY)**2)),1) < round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY+self.speed)**2)),1)):
                    self.direction = 1
                elif self.cangoright and round(math.sqrt(((self.pacDistX+self.speed)**2 + self.pacDistY**2)),1) < round(math.sqrt(((self.pacDistX - self.speed)**2 + self.pacDistY**2)),1) and not self.cangodown:
                    self.direction = 1

                #better to go up?
                elif self.cangoup and round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY-self.speed)**2)),1) < round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY + self.speed)**2)),1) and (self.cangoleft and round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY-self.speed)**2)),1) < round(math.sqrt(((self.pacDistX-self.speed)**2 + (self.pacDistY)**2)),1)):
                    self.direction = 2
                elif self.cangoup and round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY-self.speed)**2)),1) < round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY + self.speed)**2)),1) and not self.cangoleft:
                    self.direction = 2
                elif self.cangoup and round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY-self.speed)**2)),1) < round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY + self.speed)**2)),1) and (self.cangoright and round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY-self.speed)**2)),1) < round(math.sqrt(((self.pacDistX+self.speed)**2 + (self.pacDistY)**2)),1)):
                    self.direction = 2
                elif self.cangoup and round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY-self.speed)**2)),1) < round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY + self.speed)**2)),1) and not self.cangoright:
                    self.direction = 2

                #better to go down?
                elif self.cangodown and round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY+self.speed)**2)),1) < round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY - self.speed)**2)),1) and (self.cangoleft and round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY+self.speed)**2)),1) < round(math.sqrt(((self.pacDistX-self.speed)**2 + (self.pacDistY)**2)),1)):
                    self.direction = 3
                elif self.cangodown and round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY+self.speed)**2)),1) < round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY - self.speed)**2)),1) and not self.cangoleft:
                    self.direction = 3
                elif self.cangodown and round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY+self.speed)**2)),1) < round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY - self.speed)**2)),1) and (self.cangoright and round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY+self.speed)**2)),1) < round(math.sqrt(((self.pacDistX+self.speed)**2 + (self.pacDistY)**2)),1)):
                    self.direction = 3
                elif self.cangodown and round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY+self.speed)**2)),1) < round(math.sqrt(((self.pacDistX)**2 + (self.pacDistY - self.speed)**2)),1) and not self.cangoright:
                    self.direction = 3
            #if they are stuck go a way they can go
            else:
                if self.cangoleft:
                    self.direction = 0
                if self.cangoright:
                    self.direction = 1 
                elif self.cangoup:
                    self.direction = 2 
                elif self.cangodown:    
                    self.direction = 3 
                        
        
            #fix hitbox
            self.hitbox = pygame.Rect(self.x+2,self.y+2,16*scale,16*scale)
            #check if in a wall
            for i in range(len(wallHitBox)):
                if pygame.Rect.colliderect(self.hitbox, wallHitBox[i]):
                    self.collidedWithWall = True
            
            #if not in a wall, go in the direction facing
            if not self.collidedWithWall:
                if self.pastX != self.x:
                    self.pastX = self.x 
                if self.pastY != self.y:
                    self.pastY = self.y
                    
                if self.direction == 0:
                    self.x -= self.speed
                if self.direction == 1 :
                    self.x += self.speed
                if self.direction == 2:
                    self.y -= self.speed
                if self.direction == 3:
                    self.y += self.speed
            #if in a wall, get out of the wall and update hitbox and collision
            else:
                self.x = self.pastX
                self.y = self.pastY
                self.ghostPos = [self.x,self.y]
                self.hitbox = pygame.Rect(self.x+2,self.y+2,16*scale,16*scale)
                self.collidedWithWall = False

            #can wrap around the map if they leave
            if self.x > width:
                self.x = 0-30
            if self.x < -39:
                self.x = width
            
            #if pacman has a berry or the red ghost has just spawned in, wait 10 seconds before setting mode to chacing pacman again
            if self.mode == 'Run4Life' or self.mode == "JustRun":
                if self.now - self.powerupcooldown > 5000:
                    s = 48
                    if self.now - self.powerupcooldown > 10000:
                        # if self.types == 1 and self.mode == "Run4Life":
                        #     ghostSiren.stop()
                        #     ghostSiren.play(-1)
                        self.mode = 'Chase'
                        
                else:
                    s = 16
                
                #if pacman has eaten a berry update the animation
                if self.mode == 'Run4Life':
                    if self.now - self.animationTime > 100:
                        if self.animationframe != s:
                            self.animationframe += 16
                        else:
                            self.animationframe = 0
                        self.animationTime = self.now
                    if self.types == 1:
                        self.yfix = 2
                    self.ghostBox = [(129+self.animationframe)*scale,65*scale,16*scale,16*scale]
            else:
                #fix y pos for sprite
                if self.mode == "Res" or self.mode == "Eaten":
                    self.yfix = 1
        else:
            #if the ghost has made it to res chamber, use y fix as a placeholder to move down until hitting a certain y pos, then change the y fix placeholder to now move upwards
            if self.mode == "Res":
                if self.yfix == 1:
                    
                    if self.y != 265:
                        self.y += 1
                    else:
                        self.yfix = 0
                if self.yfix == 0:
                    if self.y != 220:
                        self.y -= 1
                    #once at correct y pos, go back to chasing pacman
                    else:
                        self.mode = "Chase"
                        checkIfMusic()
            #if in intro phase
            else:
                if self.direction == 2:
                    self.spriteDirection = 64
                elif self.direction == 3:
                    self.spriteDirection = 96

                #for each ghost wait a bit then move to the center of the res chamber, float out of it and begin chasing pacman
                if self.types == 3:
                    if self.animationframe == 0:
                        self.ghostBox = [(0+self.spriteDirection+self.moveAnimation)*scale,81*scale,16*scale,14*scale]
                    elif self.animationframe == 1:
                        self.ghostBox = [(0+self.spriteDirection)*scale,81*scale,16*scale,14*scale]
                    if self.now - self.introwait - self.freezeTimer > 8000:
                        if self.y != 220:
                            self.direction = 2
                            self.y -= 1
                            self.pastY = self.y
                        if self.now - self.introwait - self.freezeTimer > 8900:
                            self.mode = "Chase"
                    else:
                        if self.direction == 2:
                            self.y -= 1
                            if self.y < 260:
                                self.direction = 3
                        elif self.direction == 3:
                            self.y += 1
                            if self.y > 270:
                                self.direction = 2
                if self.types == 2:
                    if self.animationframe == 0:
                        self.ghostBox = [(0+self.spriteDirection+self.moveAnimation)*scale,97*scale,16*scale,14*scale]
                    elif self.animationframe == 1:
                        self.ghostBox = [(0+self.spriteDirection)*scale,97*scale,16*scale,14*scale]
                    if self.now - self.introwait - self.freezeTimer > 16500:
                        if not self.x == 222:
                            self.x += 2
                            self.pastX = self.x
                        else:
                            if self.y != 220:
                                self.direction = 2
                                self.y -= 1
                                self.pastY = self.y
                            if self.now - self.introwait - self.freezeTimer > 17800:
                                self.mode = "Chase"
                    else:
                        if self.direction == 2:
                            self.y -= 1
                            if self.y < 260:
                                self.direction = 3
                        elif self.direction == 3:
                            self.y += 1
                            if self.y > 270:
                                self.direction = 2
                if self.types == 4:
                    if self.animationframe == 0:
                        self.ghostBox = [(0+self.spriteDirection+self.moveAnimation)*scale,113*scale,16*scale,14*scale]
                    elif self.animationframe == 1:
                        self.ghostBox = [(0+self.spriteDirection)*scale,113*scale,16*scale,14*scale]
                    if self.now - self.introwait - self.freezeTimer > 26500:
                        if not self.x == 222:
                            self.x -= 2
                            self.pastX = self.x
                        else:
                            if self.y != 220:
                                self.direction = 2
                                self.y -= 1
                                self.pastY = self.y
                            if self.now - self.introwait - self.freezeTimer > 27800:
                                self.mode = "Chase"
                    else:
                        if self.direction == 2:
                            self.y -= 1
                            if self.y < 260:
                                self.direction = 3
                        elif self.direction == 3:
                            self.y += 1
                            if self.y > 270:
                                self.direction = 2

#pacdots
class pacDot():
    def __init__(self,x,y,width,height):
        #pos
        self.x = x
        self.y = y
        #sprite
        self.width = width
        self.height = height
        #technical
        self.kill = False
        self.hitBox = pygame.Rect(self.x,self.y,self.width,self.height)
        self.killzone = [(pygame.Rect(130,220,220,140)), (pygame.Rect(0,270,100,20)), (pygame.Rect(380,270,100,20))]
        #if touching anything not supposed to, "kill" it so as to now create errors
        for i in range(len(wallHitBox)):
            if pygame.Rect.colliderect(wallHitBox[i],self.hitBox):
                self.kill = True
        for i in range(len(self.killzone)):
            if pygame.Rect.colliderect(self.hitBox, self.killzone[i]):
                self.kill = True
        for i in range(len(powers)):
            if pygame.Rect.colliderect(self.hitBox, powers[i].hitbox):
                self.kill = True
    def draw(self):
        #draw unkilled dots
        if not self.kill:
            pygame.draw.rect(window,(250,185,176), (self.x,self.y,self.width,self.height))
        for i in range(len(self.killzone)):
            if showHitboxes:
                pygame.draw.rect(window,(255,32,0),self.killzone[i],1)

#powerups
class Power():
    def __init__(self,types):
        #which powerup
        self.types = types
        #pos
        #change pos for each powerup
        if types == 0:
            self.x = 25
            self.y = 133
        elif types == 1:
            self.x = 456
            self.y = 133
        elif types == 2:
            self.x = 25
            self.y = 415
        elif types == 3:
            self.x = 456
            self.y = 415
        self.width = 10
        self.hitbox = pygame.Rect(self.x-self.width,self.y-self.width,self.width*2,self.width*2)
        #timers
        self.now = pygame.time.get_ticks()
        self.last = self.now


    #draw
    def draw(self):
        self.now = pygame.time.get_ticks()
        #flash based on current ticks passed
        if self.now - self.last > 0 and self.now - self.last < 150:
            pygame.draw.circle(window, (250,185,176), (self.x,self.y), self.width)
        elif self.now - self.last > 300:
            self.last = self.now
        
        if showHitboxes:
            pygame.draw.rect(window,(160,32,240),self.hitbox,1)
        

#load sounds
def sounds(Folder, SoundName):
    '''
    Calculates the correct file path to get to a specific sound in a folder and return the sound file path

    Parameters
    ----------
    Folder : string
    The folder the sound is in
    SoundName : string
    The name of the sound in said folder

    Returns
    -------
    string
    The full file path of the sound file
    '''
    soundPath = str(sys.path[0]+f"\\sounds\\{Folder}\\{SoundName}.wav")
    print(f"Sound '{SoundName}.wav' Loaded")
    return(soundPath)

#play sounds
def playSounds(sound, loop):
    '''
    Plays a sound a certain number of times after stopping all other sound

    Parameters
    ----------
    sound : sound
    The name of a loaded sound
    loop : string
    The amount of times to loop the sound

    Returns
    -------
    sound
    Only one sound playing the number of looped times
    '''
    pygame.mixer.stop()
    sound.play(loop)

#Load Images
def imageLoad(FolderType, Name):
    '''
    Calculates the correct file path to get to a specific image in a folder and return the image file path

    Parameters
    ----------
    FolderType : string
    The folder the image is in
    Name : string
    The name of the sound in said folder

    Returns
    -------
    string
    The full file path of the image file
    '''
    ImagePath = str(sys.path[0]+f"\\sprites\\{FolderType}\\{Name}.png")
    print("loaded: " + ImagePath)
    return(ImagePath)

#load fonts
def fontLoad(Name):
    '''
    Calculates the correct file path to get to a specific font in a folder and return the font file path

    Parameters
    ----------
    Name : string
    The name of the font

    Returns
    -------
    string
    The full file path of the font file
    '''
    fontPath = str(sys.path[0]+f"\\fonts\\{Name}.ttf")
    return(fontPath)      


#detect if ghosts are respawning or if powerup timer is active
def checkIfMusic():
    '''
    Calculates the correct music to play based on if a ghost is running/respawning

    Parameters
    ----------
    None

    Returns
    -------
    sound
    plays a proper sound file
    '''
    global ghostRunning
    global eaten
    x = 0
    #if any ghosts are still eaten, dont run script
    for i in range(len(ghosts)):
        if ghosts[i].mode == "Res" or ghosts[i].mode == "Eaten":
            x = 1
    #if no ghosts are eaten
    if x == 0:
        #if powerup active, play power up sound, else play siren
        ghostRunning = False
        if eaten:
            playSounds(powerup, -1)
        else:
            playSounds(ghostSiren,-1)
        

#get highscore from text file
def getHighScore():
    '''
    Grabs the highscore from a text file

    Parameters
    ----------
    None

    Returns
    -------
    string
    Returns the grabbed value from the text file
    '''
    while True:
        try:
            file = open(f"{pathName}\save.txt", "r").readlines()
            x = file[0].strip()
            if not x.isnumeric():
                print("RESETTING HIGHSCORE")
                edit = open(f"{pathName}\save.txt", "w")
                file[0] = "0\n"
                edit.writelines(file)
                x = "0"
                edit.close
            return x
        except:
            print("RESETTING SYSTEM")
            edit = open(f"{pathName}\save.txt", "w")
            file = "\n\n\n"
            edit.writelines(file)
            edit.close

#change score in text file
def highScoreUpdate(editText):
    '''
    Updates the value in a text file

    Parameters
    ----------
    editText : string
    The text replacing the old text in the file

    Returns
    -------
    string
    The new updated line from the file
    '''
    editText = str(editText) + "\n"
    lines = open(f"{pathName}\save.txt", "r").readlines()
    lines[0] = editText
    editText = open(f"{pathName}\save.txt", "w")
    editText.writelines(lines)
    editText.close()
    return lines[0].strip()



#Game Vars
pygame.init()
pygame.mouse.set_visible(False)
rate = pygame.time.Clock()
frames = 60
width = 479
height = 600
windowSize = (width,height)  
window = pygame.display.set_mode((windowSize))
pygame.display.set_caption('PacMan!')
gameState = "menu"
currentTicks = pygame.time.get_ticks()


#sounds
eat = [pygame.mixer.Sound(sounds("pacman","eat1")), pygame.mixer.Sound(sounds("pacman","eat2"))]
eat[0].set_volume(0.5)
eat[1].set_volume(0.5)
ghostdies = pygame.mixer.Sound(sounds("pacman","eatGhost"))
pacdies = pygame.mixer.Sound(sounds("pacman","pacdies"))
flee = pygame.mixer.Sound(sounds("ghosts","fleaingGhost"))
powerup = pygame.mixer.Sound(sounds("pacman","powerup"))
ghostSiren = pygame.mixer.Sound(sounds("ghosts","ambientghost"))
intro = pygame.mixer.Sound(sounds("pacman","intro"))
playintrotheme = True
#sprites
bg = pygame.image.load(imageLoad("backgrounds","mainbg"))
bg = pygame.transform.scale(bg, (479,479))  
menu = pygame.image.load(imageLoad("backgrounds","menu"))
spriteSheet = pygame.image.load(imageLoad("","spritesheet1"))
scale = 2
spriteSheet = pygame.transform.scale(spriteSheet, (scale*spriteSheet.get_width(),scale*spriteSheet.get_height()))
#fonts
font = pygame.font.Font(fontLoad('pacman'), 18)

#wall hitboxes
wallHitBox = [(pygame.Rect(0,65,479,8)),(pygame.Rect(472,65,100,202)),(pygame.Rect(386,106,53,25)),(pygame.Rect(386,164,53,12)),
(pygame.Rect(386,209,100,58)),(pygame.Rect(-500,65,510,202)),(pygame.Rect(10,209,85,58)),(pygame.Rect(230,65,22,66)),
(pygame.Rect(285,106,68,25)),(pygame.Rect(335,164,18,103)),(pygame.Rect(283,209,62,13)),(pygame.Rect(136,209,61,13)),
(pygame.Rect(128,164,17,103)),(pygame.Rect(43,106,52,25)),(pygame.Rect(43,164,52,12)),(pygame.Rect(128,106,69,25)),
(pygame.Rect(178,164,124,12)),(pygame.Rect(230,164,20,58)),(pygame.Rect(178,344,124,12)),(pygame.Rect(230,344,20,57)),
(pygame.Rect(178,434,124,12)),(pygame.Rect(230,434,20,56)),(pygame.Rect(178,255,45,8)),(pygame.Rect(256,255,46,8)),
(pygame.Rect(178,304,124,8)),(pygame.Rect(178,255,12,50)),(pygame.Rect(290,255,12,50)),(pygame.Rect(0,523,600,12)),
(pygame.Rect(128,300,17,56)),(pygame.Rect(335,300,18,56)),(pygame.Rect(283,389,70,12)),(pygame.Rect(128,389,69,12)),
(pygame.Rect(386,300,100,56)),(pygame.Rect(-25,300,120,56)),(pygame.Rect(-500,340,510,203)),(pygame.Rect(470,340,510,203)),
(pygame.Rect(386,389,17,57)),(pygame.Rect(76,389,19,57)),(pygame.Rect(43,389,51,12)),(pygame.Rect(386,389,51,12)),
(pygame.Rect(436,434,50,12)),(pygame.Rect(-7,434,50,12)),(pygame.Rect(335,434,18,50)),(pygame.Rect(128,434,17,50)),
(pygame.Rect(43,479,154,11)),(pygame.Rect(283,479,154,11)), (pygame.Rect(200,255,100,7))] #I Hate Hitboxes

#technical vars
score = 0
numGhostsEaten = 0
highscore = int(getHighScore())
lives = 3
inkytargetx = 0
inkytargety = 0
eatSoundType = 0
eaten = False
ghostRunning = False
showHitboxes = False #editable
invinc = False #editable

#timers
introTimer = currentTicks
flash = currentTicks
freeze = currentTicks
powerupTimer = currentTicks
waitingTimeStart = 4200

#lists/classes
pacmans = []
ghosts = []
dots = []
powers = []
for i in range(0,4,1):
    powers.append(Power(i))
pacmans.append(Pacman())

for i in range(1,5,1):
    ghosts.append(Ghost(i))

x = 23
y = 87
for i in range(0,20,1): #20
    for i in range(0,26,1):
        dots.append(pacDot(x,y,5,5))
        x += 17.2
        if x > width:
            break
    x = 23.1
    y += 21.7

#game inputes
keyInput = pygame.key.get_pressed()
mousePos = pygame.mouse.get_pos()


print(f"Current Highscore: {highscore}0")

#game loop
while True:
    #update vars
    mousePos = pygame.mouse.get_pos()
    keyInput = pygame.key.get_pressed()
    currentTicks = pygame.time.get_ticks()
    event = pygame.event.poll()
    font = pygame.font.Font(fontLoad('pacman'), 18)
    keyPresses = pygame.key.get_pressed()
    #close game when quit
    if event.type == pygame.QUIT or keyInput[pygame.K_ESCAPE]:
            break

    #if starting the game
    if gameState == "start":
        #show background stuff and flash objects
        window.fill(0)
        window.blit(bg,(0,50))
        if currentTicks - flash > 0 and currentTicks - flash < 300:
            text = font.render("1up", True, (255,255,255))
            window.blit(text, (32,5))
        elif currentTicks - flash > 600:
            flash = currentTicks
        text = font.render(f"{score:10d}0", True, (255,255,255))
        window.blit(text, (-80,30))
        text = font.render("high score", True, (255,255,255))
        window.blit(text, (150,5))
        text = font.render(f"{highscore:10d}0", True, (255,255,255))
        window.blit(text, (98,30))
        text = font.render("READY!", True, (255,255,7))
        window.blit(text, (190,315))
        
        #draw sprites
        for i in range(len(ghosts)):
            ghosts[i].draw()
        for i in range(len(powers)):
            powers[i].draw()
        for i in range(len(dots)):
            dots[i].draw()
        pacmans[0].draw()
        #after a bit, start game
        if currentTicks - introTimer > waitingTimeStart:
            gameState = 'game'
            waitingTimeStart = 2000
            playSounds(ghostSiren,-1)
    #if game started
    elif gameState == "game":
        #draw sprites
        window.fill(0)
        window.blit(bg,(0,50))

        #if score is better then highscore, update the highscore
        if score > highscore:
            highScoreUpdate(score)
            highscore = score
        
        #count how many dots are left, and if there are 0, win the game
        dotLeft = 0
        for i in range(len(dots)):
            if dots[i].kill == False:
                dotLeft += 1
        if dotLeft == 0 and len(powers) == 0:
            gameState = "win"
            xy = []
            for i in range(len(ghosts)):
                xy.append((ghosts[i].pastX,ghosts[i].pastY))
            ghosts = []
            for i in range(1,5,1):
                ghosts.append(Ghost(i))
                
            for i in range(len(ghosts)):
                ghosts[i].x = xy[i][0]
                ghosts[i].y = xy[i][1]
                ghosts[i].pastX = ghosts[i].x
                ghosts[i].pastY = ghosts[i].y
                ghosts[i].mode = "Chase"
                ghosts[i].move()
                ghosts[i].draw()

        #fix blue ghosts target based on mode
        if ghosts[1].mode == "Chase":
            inkytargetx = 2*abs((ghosts[0].pacDistX - ghosts[2].pacDistX))
            inkytargety = 2*abs((ghosts[0].pacDistY - ghosts[2].pacDistY))
        if ghosts[1].mode == 'Run4Life':
            inkytargetx = ghosts[1].pastX+350
            inkytargety = ghosts[1].pastY-1000
        
        

        
        

        #text
        if currentTicks - flash > 0 and currentTicks - flash < 300:
            text = font.render("1up", True, (255,255,255))
            window.blit(text, (32,5))
        elif currentTicks - flash > 600:
            flash = currentTicks
        text = font.render(f"{score:10d}0", True, (255,255,255))
        window.blit(text, (-80,30))
        text = font.render("high score", True, (255,255,255))
        window.blit(text, (150,5))
        text = font.render(f"{highscore:10d}0", True, (255,255,255))
        window.blit(text, (98,30))
        


        if showHitboxes:
            for i in range(len(wallHitBox)):
                pygame.draw.rect(window,(160,32,240),wallHitBox[i],width = 1)
            pygame.draw.rect(window,(255,255,255),pygame.Rect(inkytargetx,inkytargety,10,1))
        
        #draw and update powers
        for i in range(len(powers)):
            powers[i].draw()
        #if pacman ate a berry, inscrease score and scare ghosts not already eaten
        for i in range(len(powers)):
            if pygame.Rect.colliderect(powers[i].hitbox,pacmans[0].dotHitbox):
                eaten = True
                powerupTimer = currentTicks
                powers.remove(powers[i])
                score += 5
                if ghostRunning == False:
                    playSounds(powerup,-1)
                for i in range(len(ghosts)):
                    if ghosts[i].mode != "Intro" and ghosts[i].mode != "Eaten" and ghosts[i].mode != "Res":
                        ghosts[i].mode = "Run4Life"
                        ghosts[i].animationframe = 0
                        ghosts[i].now = pygame.time.get_ticks()
                        ghosts[i].powerupcooldown = ghosts[i].now
                        
                break
        #draw and update dots
        for i in range(len(dots)):
            dots[i].draw()
        for i in range(len(dots)):
            #kill the dots and play sounds 
            if pygame.Rect.colliderect(dots[i].hitBox,pacmans[0].dotHitbox):
                if not dots[i].kill:
                    eat[eatSoundType].play()
                    if eatSoundType == 0:
                        eatSoundType = 1
                    else:
                        eatSoundType = 0
                    score += 1
                dots[i].kill = True
                dots.remove(dots[i])
                break
        
        #update ghosts
        for i in range(len(ghosts)):
            ghosts[i].draw()
            ghosts[i].move()
            #if touching pacman
            if pygame.Rect.colliderect(pacmans[0].hitbox,ghosts[i].hitbox):
                #if pacman has powerup active and has not already respawned, get eaten and increase score amount
                if ghosts[i].mode == "Run4Life":
                    ghosts[i].mode = "Eaten"
                    #num of ghosts can never exceed 4
                    if numGhostsEaten != 4:
                        numGhostsEaten += 1
                    ghostRunning = True
                    gameState = "GhostEaten"
                    playSounds(ghostdies, 0)
                    freeze = currentTicks
                #otherwise if just a regular ghost, kill pacman
                elif (ghosts[i].mode == "Chase" or ghosts[i].mode == "Coward" or ghosts[i].mode == "JustRun" or ghosts[i].mode == "Intro") and invinc == False:
                    gameState = "PacDead"
                    pygame.mixer.stop()
                    freeze = currentTicks

        #update pacman
        for i in range(len(pacmans)):
            pacmans[i].draw()
            pacmans[i].move()

        
        
        #if powerup is eaten, after 10 seconds turn on ghost siren if there are no ghosts running and reset how many ghosts have been eaten this run
        if eaten:
            if currentTicks - powerupTimer > 10000:
                if ghostRunning == False:
                    playSounds(ghostSiren,-1)
                eaten = False
                numGhostsEaten = 0
        #debug testing for what hitboxes are what for the walls
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(wallHitBox)):
                if pygame.Rect.colliderect(pygame.Rect(mousePos[0],mousePos[1],1,1), wallHitBox[i]):
                    print(wallHitBox[i])
                    print(i)
            print(mousePos)
    #if a ghost is eaten, pause the game for a bit then keep going
    elif gameState == "GhostEaten":
        window.fill(0)
        window.blit(bg,(0,50))
        if currentTicks - flash > 0 and currentTicks - flash < 300:
            text = font.render("1up", True, (255,255,255))
            window.blit(text, (32,5))
        elif currentTicks - flash > 600:
            flash = currentTicks
        text = font.render(f"{score:10d}0", True, (255,255,255))
        window.blit(text, (-80,30))
        text = font.render("high score", True, (255,255,255))
        window.blit(text, (150,5))
        text = font.render(f"{highscore:10d}0", True, (255,255,255))
        window.blit(text, (98,30))

        for i in range(len(dots)):
            dots[i].draw()
        for i in range(len(powers)):
            powers[i].draw()
        tempscore = (2 ** numGhostsEaten)*10


        font = pygame.font.Font(fontLoad('pacman'), 12)
        text = font.render(f"{tempscore*10}", True, (0,255,255))
        window.blit(text, (pacmans[0].x,pacmans[0].y))
        if currentTicks - freeze > 1000:
            score += tempscore
            for i in range(len(ghosts)):
                ghosts[i].freezeTimer += 1000
            gameState = "game"
            playSounds(flee,-1)
    #if pacman is hit, do an animation
    elif gameState == "PacDead":
        window.fill(0)
        window.blit(bg,(0,50))
        if currentTicks - flash > 0 and currentTicks - flash < 300:
            text = font.render("1up", True, (255,255,255))
            window.blit(text, (32,5))
        elif currentTicks - flash > 600:
            flash = currentTicks
        text = font.render(f"{score:10d}0", True, (255,255,255))
        window.blit(text, (-80,30))
        text = font.render("high score", True, (255,255,255))
        window.blit(text, (150,5))
        text = font.render(f"{highscore:10d}0", True, (255,255,255))
        window.blit(text, (98,30))
        for i in range(len(dots)):
            dots[i].draw()
        for i in range(len(powers)):
            powers[i].draw()
        #after waiting one sec, update pacmans sprite and sound then reset part of the game to  continue playing
        if currentTicks - freeze < 1000:
            pacsprite = 34
            playdeathsound = True
            pacdeathana = currentTicks
            for i in range(4):
                ghosts[i].draw()
            pacmans[0].draw()
        else:
            if playdeathsound:
                playSounds(pacdies,0)
                playdeathsound = False
            if currentTicks - pacdeathana > 100:
                pacsprite += 16
                pacdeathana = currentTicks
            if pacsprite == 482:
                playintrotheme = False
                gameState = "Reset"
            else:
                if pacsprite < 1000:
                    pacBox = [pacsprite*scale,1*scale,15*scale,15*scale]
                    window.blit(spriteSheet, (pacmans[0].x,pacmans[0].y), pacBox)
    #if the game needs to be reset
    elif gameState == "Reset":
        #reset all values
        #play theme on first itteration and no others
        if playintrotheme:
            playSounds(intro,-1)
            playintrotheme = False
        inkytargetx = 0
        inkytargety = 0
        eatSoundType = 0
        eaten = False
        ghostRunning = False
        introTimer = currentTicks
        flash = currentTicks
        freeze = currentTicks
        powerupTimer = currentTicks
        pacmans = []
        ghosts = []
        lives -= 1
        print(lives)
        #fully reset game if game over
        if lives == 0 or lives == 1000:
            
            if lives == 0:
                gameState = "gameOver"
            lives = 4
            waitingTimeStart = 4200
            playintrotheme = True
            score = 0
            dots = []
            powers = []
            #reset powerups
            for i in range(0,4,1):
                powers.append(Power(i))
            #reset pacdots
            x = 23
            y = 87
            for i in range(0,20,1):
                for i in range(0,26,1): #(set to 5)
                    dots.append(pacDot(x,y,5,5))
                    x += 17.2
                    if x > width:
                        break
                x = 23.1
                y += 21.7
           
        #ignore some resets on a non game over
        else:
            gameState = "start"

        #reset pacman
        pacmans.append(Pacman())
        #reset ghosts
        for i in range(1,5,1): #(set to 5)
            ghosts.append(Ghost(i))
    #if no more lives, show game over text and wait for enter key
    elif gameState == "gameOver":
        font = pygame.font.Font(fontLoad('pacman'), 12)
        text = font.render(f"game over", True, (255,0,0))
        window.blit(text, (186,320))
        
        if keyPresses[pygame.K_RETURN] or keyPresses[pygame.K_SPACE]:
            gameState = "menu"
            freeze = currentTicks
    #if win, show win text and wait for enter key
    elif gameState == "win":
        pygame.mixer.stop()
        
        font = pygame.font.Font(fontLoad('pacman'), 12)
        text = font.render(f"you  win", True, (0,255,0))
        window.blit(text, (186,320))
        font = pygame.font.Font(fontLoad('pacman'), 20)
        for i in range(len(ghosts)):
            text = font.render(f"!", True, (255,0,0))
            
            window.blit(text, (ghosts[i].pastX+8,ghosts[i].pastY-25))
        if keyPresses[pygame.K_RETURN] or keyPresses[pygame.K_SPACE]:
            gameState = "menu"
            
            freeze = currentTicks
    #if on menu, wait for enter key and show menu sprite
    elif gameState == "menu":
        window.fill(0)
        window.blit(menu,(0,0))
        if highscore != 0:
            text = font.render(f"{highscore:10d}0", True, (222,223,255))
            window.blit(text, (98,30))
        if currentTicks - freeze > 100:
            if keyPresses[pygame.K_RETURN] or keyPresses[pygame.K_SPACE]:
                introTimer = currentTicks
                flash = currentTicks
                freeze = currentTicks
                powerupTimer = currentTicks
                waitingTimeStart = 4200
                lives = 1001
                gameState = "Reset"

                
        
    
    #for how many lives are left, show mini pacmen in the bottom of the screen to show lives
    if gameState != "menu" and lives != 0 and lives != 1001:
        x = -20
        for i in range(lives-1):
            x += 24
            livesBox = [132*scale,17*scale,10*scale,30*scale]
            window.blit(spriteSheet, (x, 530), livesBox)

    #update screen
    pygame.display.flip()
    #update ticks
    rate.tick(frames)
#quit game
pygame.quit()