import pygame, random, math

pygame.init()

# Mirror Image Function
def mirror(spriteArray):
    mirrorArray = []
    for i in range(len(spriteArray)):
         mirrorArray.append(pygame.transform.flip(spriteArray[i], True, False))
    return mirrorArray

# Visuals Setup
bg = pygame.transform.scale(pygame.image.load('sprites/BGZombie.png'), (1400, 800))
icon = pygame.image.load('sprites/icon.png')
font = pygame.font.SysFont('Helvetica', 40, True, False)
mediumFont = pygame.font.SysFont('Helvetica', 30, True, False)
smallFont = pygame.font.SysFont('Helvetica', 20, True, False)
walkRight = [pygame.image.load('sprites/wRunR0.png'), pygame.image.load('sprites/wRunR1.png'), pygame.image.load('sprites/wRunR2.png'), pygame.image.load('sprites/wRunR3.png')]
walkLeft = mirror(walkRight)
fireball = pygame.transform.scale(pygame.image.load('sprites/bullet.png'), (15,15))
demonRight = [pygame.image.load('sprites/demonRun0.png'), pygame.image.load('sprites/demonRun1.png'), pygame.image.load('sprites/demonRun2.png'), pygame.image.load('sprites/demonRun3.png')]
demonLeft = mirror(demonRight)
chortRight = [pygame.image.load('sprites/chortRun0.png'), pygame.image.load('sprites/chortRun1.png'), pygame.image.load('sprites/chortRun2.png'), pygame.image.load('sprites/chortRun3.png')]
chortLeft = mirror(chortRight)
bloodImages = [pygame.image.load('sprites/1_0.png'), pygame.image.load('sprites/1_1.png'), pygame.image.load('sprites/1_2.png'), pygame.image.load('sprites/1_3.png'), pygame.image.load('sprites/1_4.png'), pygame.image.load('sprites/1_5.png'), pygame.image.load('sprites/1_6.png'), pygame.image.load('sprites/1_7.png'), pygame.image.load('sprites/1_8.png'), pygame.image.load('sprites/1_9.png'), pygame.image.load('sprites/1_10.png'), pygame.image.load('sprites/1_11.png'), pygame.image.load('sprites/1_12.png'), pygame.image.load('sprites/1_13.png'), pygame.image.load('sprites/1_14.png'), pygame.image.load('sprites/1_15.png'), pygame.image.load('sprites/1_16.png'), pygame.image.load('sprites/1_17.png'), pygame.image.load('sprites/1_18.png'), pygame.image.load('sprites/1_19.png'), pygame.image.load('sprites/1_20.png'), pygame.image.load('sprites/1_21.png'), pygame.image.load('sprites/1_22.png'), pygame.image.load('sprites/1_23.png'), pygame.image.load('sprites/1_24.png'), pygame.image.load('sprites/1_25.png'), pygame.image.load('sprites/1_26.png'), pygame.image.load('sprites/1_27.png'), pygame.image.load('sprites/1_28.png')]
heartEmpty = pygame.image.load('sprites/HeartEmpty.png')
heartFull = pygame.image.load('sprites/HeartFull.png')
manaPotion = pygame.image.load('sprites/manaPotionIcon.png')
healthPotion = pygame.image.load('sprites/healthPotionIcon.png')
goldCoin = pygame.image.load('sprites/goldCoin.png')
silverCoin = pygame.image.load('sprites/silverCoin.png')

# Sounds Setup
fireballSound = pygame.mixer.Sound("sounds/fireballSound.mp3")
fireballSound.set_volume(10)
killSound = pygame.mixer.Sound('sounds/killSound.wav')
killSound.set_volume(0.1)
drinkSound = pygame.mixer.Sound('sounds/drinkSound.wav')
drinkSound.set_volume(0.3)
coinSounds = [pygame.mixer.Sound("sounds/Bag-of-Coins-A-www.fesliyanstudios.com.mp3"),pygame.mixer.Sound("sounds/Bag-of-Coins-B-www.fesliyanstudios.com.mp3"),pygame.mixer.Sound("sounds/Bag-of-Coins-D-www.fesliyanstudios.com.mp3")]

# General Setup
win = pygame.display.set_mode((1400,800))
pygame.display.set_icon(icon)
pygame.display.set_caption("Dungeon Wizard")
clock = pygame.time.Clock()

class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = pygame.Rect(self.x + 5, self.y + 35, self.width - 10, self.height - 35)
        self.health = 250
        self.healthPotion = 0
        self.manaPotion = 0
        self.shootCoolDown = 50
        self.coins = 0

    def draw(self, win):
        if self.walkCount >= 12:
            self.walkCount = 0

        if not(self.standing):
            if self.right:
                charRight = pygame.transform.scale(walkRight[self.walkCount//3], (wiz.width, wiz.height))
                win.blit(charRight, (self.x,self.y))
                self.walkCount += 1
            elif self.left:
                charLeft = pygame.transform.scale(walkLeft[self.walkCount//3], (wiz.width, wiz.height))
                win.blit(charLeft, (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                idleRight = pygame.transform.scale(walkRight[0], (wiz.width, wiz.height))
                win.blit(idleRight, (self.x, self.y))
            else:
                idleLeft = pygame.transform.scale(walkLeft[0], (wiz.width, wiz.height))
                win.blit(idleLeft, (self.x, self.y))
        
        self.hitbox = (self.x + 5, self.y + 35, self.width - 10, self.height - 35)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        pass

class mob():
    def __init__(self, coord, width, height, vel, mobType, leftRun, rightRun):
        self.x = coord[0]
        self.y = coord[1]
        self.width = width
        self.height = height
        self.walkCount = 0
        self.vel = vel
        self.mobType = mobType
        self.leftRun = leftRun
        self.rightRun = rightRun
        self.spawnTime = 0
        self.center = (self.x + self.width/2, self.y + self.height/2)
        self.damaged = False

        if mobType == 'demon':
            self.hitbox = pygame.Rect(self.x + 20, self.y + 20, self.width - 30, self.height - 30)
            self.health = random.randint(2,3)
            self.healthBarDivider = self.health
        
        elif mobType == 'chort':
            self.hitbox = pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 10)
            if random.randint(0,4) == 0:
                self.health = 2
                self.healthBarDivider = self.health
            else:
                self.health = 1
                self.healthBarDivider = self.health

    def draw(self, win):
        if self.walkCount >= 12:
            self.walkCount = 0

        if wiz.x > self.x: #FACE RIGHT
            charRight = pygame.transform.scale(self.rightRun[self.walkCount//3], (self.width, self.height))
            win.blit(charRight, (self.x,self.y))
            self.walkCount += 1
        elif wiz.x < self.x:
            charLeft = pygame.transform.scale(self.leftRun[self.walkCount//3], (self.width, self.height))
            win.blit(charLeft, (self.x,self.y))
            self.walkCount += 1

        if self.damaged == True and self.mobType == 'demon':
            pygame.draw.rect(win, (150, 33, 33), pygame.Rect(self.x + 10, self.y + 110, 80, 7), 0, 2)
            pygame.draw.rect(win, (40, 173, 47), pygame.Rect(self.x + 10, self.y + 110, self.health*80/self.healthBarDivider, 7), 0, 2)
            pygame.draw.rect(win, (0, 0, 0), pygame.Rect(self.x + 10, self.y + 110, 80, 7), 1, 2)
        
        elif self.damaged == True and self.mobType == 'chort':
            pygame.draw.rect(win, (150, 33, 33), pygame.Rect(self.x + 5, self.y + 60, 30, 7), 0, 2)
            pygame.draw.rect(win, (40, 173, 47), pygame.Rect(self.x + 5, self.y + 60, self.health*30/self.healthBarDivider, 7), 0, 2)
            pygame.draw.rect(win, (0, 0, 0), pygame.Rect(self.x + 5, self.y + 60, 30, 7), 1, 2)
            
        if self.mobType == 'demon':
            self.hitbox = pygame.Rect(self.x + 20, self.y + 30, self.width - 40, self.height - 40)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

        elif self.mobType == 'chort':
            self.hitbox = pygame.Rect(self.x + 10, self.y + 20, self.width - 20, self.height - 30)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.health -= 1
        self.damaged = True
        if self.health == 0:
            randomCoinType = random.randint(0,4)
            if randomCoinType == 0:
                drops.append(coin(demon.x + demon.width/2, demon.y + demon.height/2, 'gold'))
            if randomCoinType == 1 or randomCoinType == 2:
                drops.append(coin(demon.x + demon.width/2, demon.y + demon.height/2, 'silver'))
            demons.pop(demons.index(self))

class projectile():
    def __init__(self, x, y, mousepos, vel):
        self.x = x
        self.y = y
        self.xMouse = mousepos[0]
        self.yMouse = mousepos[1]
        self.vel = vel
        radians = math.atan2(mousepos[1] - y, mousepos[0] - x)
        self.dx = math.cos(radians)
        self.dy = math.sin(radians)

    def draw(self, win):
        win.blit(fireball, (self.x, self.y))

class death():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0

    def draw(self, win):
        if self.frame <= 14:
            bloodFrame = pygame.transform.scale(bloodImages[self.frame * 2], (150, 150))
            win.blit(bloodFrame, (self.x, self.y))
            self.frame += 1

class coin():
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.hitbox = pygame.Rect(self.x + 2, self.y + 2, 15, 15)

    def draw(self, win):
            if self.type == 'gold':
                coin = pygame.transform.scale(goldCoin, (200, 200))
            else:
                coin = pygame.transform.scale(silverCoin, (200, 200))
            win.blit(coin, (self.x, self.y))
            self.hitbox = pygame.Rect(self.x + 2, self.y + 2, 15, 15)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
            pass
        
# Drawing
def redrawGameWindow():
    win.blit(bg, (0,0))
    
    # MANA BAR
    pygame.draw.rect(win, (0,0,0), pygame.Rect(wiz.x - 5, wiz.y + 87, 60, 7.5), 0, 2)
    if shootTimer == 0: # FULL BLUE
        pygame.draw.rect(win, (52, 137, 247), pygame.Rect(wiz.x - 3, wiz.y + 88, 56, 5), 0, 2)
    pygame.draw.rect(win, (72, 72, 74), pygame.Rect(wiz.x - 3, wiz.y + 88, shootTimer*55/(wiz.shootCoolDown - wiz.manaPotion*10), 5), 0, 2) # GRAY PROGESS

    # HEALTH
    pygame.draw.rect(win, (150, 33, 33), pygame.Rect(58, 757, wiz.health, 30), 0, 4) # HEALTH BAR
    pygame.draw.rect(win, (143, 103, 43), pygame.Rect(58, 757, 500, 30), 3, 4) # HEALTH BORDER
    win.blit(pygame.transform.scale(heartFull, (40, 40)), (10, 750))

    # POTIONS
    win.blit(font.render('Q', 1, (255, 255, 255)), (35, 575))
    win.blit(font.render('E', 1, (255, 255, 255)), (135,575))
    win.blit(pygame.transform.scale(healthPotion, (225, 225)), (10, 640))
    win.blit(pygame.transform.scale(manaPotion, (225, 225)), (105, 640))
    numHealth = smallFont.render('x'+str(wiz.healthPotion), 1, (255, 255, 255))
    win.blit(numHealth, (80, 715))
    numMana = smallFont.render('x'+str(wiz.manaPotion), 1, (255, 255, 255))
    win.blit(numMana, (175, 715))
    price25 = smallFont.render('25', 1, (255, 255, 255))
    win.blit(price25, (30, 620))
    price50 = smallFont.render('50', 1, (255, 255, 255))
    win.blit(price50, (125, 620))
    win.blit(pygame.transform.scale(goldCoin, (200, 200)), (52, 622))
    win.blit(pygame.transform.scale(goldCoin, (200, 200)), (147, 622))

    # SCORE
    text = mediumFont.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (5, 490))

    # COINS
    numOfCoins = mediumFont.render('Coins: ' + str(wiz.coins), 1, (255, 255, 255))
    win.blit(numOfCoins, (5, 525))
    for drop in drops:
        drop.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    wiz.draw(win)

    for demon in demons:
        demon.draw(win)
    
    for kill in blood:
        kill.draw(win)

    pygame.display.update()

# Main Loop
score = 0
wiz = player(670, 330, 48, 84) #OG width 16, height 28
bullets = []
chortSpawnpoints = [(245, 306), (672, 141), (1059, 150), (1100, 305), (668, 575)]
demonSpawnpoints = [(242, 256), (655, 131), (1039, 139), (1065, 275), (653, 530)]
demons = []
blood = []
drops = []
shootTimer = 0
spawnCoolDown = 0
buttonTimer = 0
buttonDelay = 15
difficulty = score

run = True
while run:
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # SPAWNING MOBS
    mobType = random.randint(0,4)
    if difficulty < 80:
        difficulty = score
    if spawnCoolDown == 100 - difficulty:
        if mobType == 0 or mobType == 1:
            demons.append(mob(chortSpawnpoints[random.randint(0, 4)], 42, 58, random.random()*2 + 3, 'chort', chortLeft, chortRight))
        if mobType == 2:
            demons.append(mob(demonSpawnpoints[random.randint(0, 4)], 96, 108, random.random()*2 + 1, 'demon',demonLeft, demonRight))
        if mobType == 3:
            demons.append(mob(demonSpawnpoints[random.randint(0, 4)], 96, 108, random.random()*2 + 1, 'demon',demonLeft, demonRight))
            demons.append(mob(chortSpawnpoints[random.randint(0, 4)], 42, 58, random.random()*2 + 3, 'chort', chortLeft, chortRight))
        
        spawnCoolDown = 0
    else:
        spawnCoolDown += 1

    # BUG FIX OF Spawn Cool Down Surpassing SpawnTime
    if spawnCoolDown > 200:
        spawnCoolDown = 0
 
    for bullet in bullets: # CHECK IF BULLETS HIT DEMON OR OFF SCREEN
        for demon in demons:
            try:
                if bullet.y - 7.5 < demon.hitbox[1] + demon.hitbox[3] and bullet.y + 7.5 > demon.hitbox[1]:
                    if bullet.x + 7.5 > demon.hitbox[0] and bullet.x - 7.5 < demon.hitbox[0] + demon.hitbox[2]:
                        score += 1
                        demon.hit()
                        blood.append(death(bullet.x - 50, bullet.y - 50))
                        bullets.pop(bullets.index(bullet))
                        killSound.play() 
            except:
                pass

        if bullet.x < 1120 and bullet.x > 250 and bullet.y < 600 and bullet.y > 110:
            bullet.x += bullet.dx * bullet.vel
            bullet.y += bullet.dy * bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
        
    for demon in demons: # MAKE DEMON FOLLOW WIZ
        if demon.spawnTime > 25:
            radians = math.atan2(wiz.y - demon.y, wiz.x - demon.x)
            demon.x += math.cos(radians) * demon.vel
            demon.y += math.sin(radians) * demon.vel
        else:
            demon.spawnTime += 1

    for demon in demons: # WIZ TAKES DAMAGE IF HIT
        if demon.hitbox.colliderect(wiz.hitbox):
            wiz.health -= (1 + score/20)
  
    # CHECK IF WIZ PICKS UP DROP
    for drop in drops:
        if drop.hitbox.colliderect(wiz.hitbox) and drop.type == 'gold':
            drops.pop(drops.index(drop))
            coinSounds[random.randint(0,2)].play()
            wiz.coins += 10
        elif drop.hitbox.colliderect(wiz.hitbox) and drop.type == 'silver':
            drops.pop(drops.index(drop))
            coinSounds[random.randint(0,2)].play()
            wiz.coins += 5

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    if shootTimer > 0:
        shootTimer += 1
    if shootTimer > wiz.shootCoolDown - (wiz.manaPotion*10):
        shootTimer = 0
    if mouse[0] and shootTimer == 0: # SHOOT
        fireballSound.play()
        bullets.append(projectile(round(wiz.x + wiz.width//2 - 15), round(wiz.y + wiz.width//2 + 40), pygame.mouse.get_pos(), 6))
        shootTimer = 1

    if keys[pygame.K_w] and wiz.y > 110: # UP
        wiz.y -= wiz.vel*1
        wiz.standing = False
        if keys[pygame.K_a] and wiz.x > 250: # UPLEFT 
            wiz.x -= wiz.vel
            wiz.left= True
            wiz.right= False
        if keys[pygame.K_d] and wiz.x < 1090: # UPRIGHT
            wiz.x += wiz.vel
            wiz.right= True
            wiz.left= False
    elif keys[pygame.K_s] and wiz.y < 535: # DOWN
        wiz.y += wiz.vel
        wiz.standing = False
        if keys[pygame.K_a] and wiz.x > 250: # DOWNLEFT
            wiz.x -= wiz.vel
            wiz.left= True
            wiz.right= False
        if keys[pygame.K_d] and wiz.x < 1090: # DOWNRIGHT
            wiz.x += wiz.vel
            wiz.right= True
            wiz.left= False
    elif keys[pygame.K_a] and wiz.x > 250: # LEFT
        wiz.x -= wiz.vel*1.3
        wiz.left= True
        wiz.right= False
        wiz.standing = False
    elif keys[pygame.K_d] and wiz.x < 1090: # RIGHT
        wiz.x += wiz.vel*1.3
        wiz.right= True
        wiz.left= False
        wiz.standing = False
    else: # NOT MOVING
        wiz.standing = True
        walkCount = 0

    if buttonTimer > 0:
        buttonTimer += 1
    if buttonTimer > buttonDelay:
        buttonTimer = 0
    if keys[pygame.K_q] and wiz.coins >= 25 and wiz.health < 500 and buttonTimer == 0: # BUY HEALTH
        buttonTimer = 1
        drinkSound.play()
        if wiz.health + 50 <= 500:
            wiz.health += 50
        else:
            wiz.health = 500
        wiz.healthPotion += 1
        wiz.coins -= 25
    if keys[pygame.K_e] and wiz.coins >= 50 and wiz.manaPotion < 4 and buttonTimer == 0: # BUY MANA
        drinkSound.play()
        buttonTimer = 1
        wiz.manaPotion += 1
        wiz.coins -= 50

    if wiz.health > 0:
        redrawGameWindow()

    else:
        pygame.draw.rect(win, (45, 45, 45), pygame.Rect(530, 250, 345, 200), 0, 4) # HEALTH BAR
        gameOver = font.render('GAME OVER', 1, (255, 77, 46))
        scoreText = font.render(str(score), 1, (255, 255, 255))

        if score < 10:
            win.blit(scoreText, (695, 350))
        elif score < 100:
            win.blit(scoreText, (685, 350))
        else:
            win.blit(scoreText, (675, 350))
        win.blit(gameOver, (600, 300))
        pygame.display.update()

pygame.quit()