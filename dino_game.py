import pygame
import random

pygame.init()
cactus_image = [pygame.image.load("bigcactus.png"), pygame.image.load("smallcactus.png"),
                pygame.image.load("manycactus.png"), pygame.image.load("manycactus2.png"),
                pygame.image.load("manycactus3.png"), pygame.image.load("smallcactus2.png")]
dino_walk_image = [pygame.image.load("dinorun1.png"), pygame.image.load("dinorun2.png")]
dino_duck_image = [pygame.image.load("dinoduck1.png"), pygame.image.load("dinoduck2.png")]
dino_jump_image = pygame.image.load("dinojump.png")
bird_image = [pygame.image.load("bird1.png"), pygame.image.load("bird2.png")]
ground_image1 = pygame.image.load("ground.png")
ground_image2 = pygame.image.load("ground.png")
win = pygame.display.set_mode((1200, 400))

clock = pygame.time.Clock()
sfont = pygame.font.SysFont("comicsans", 50, True)


class Ground:
    def __init__(self, x):
        self.x = x
        self.x2 = 1786

    def move(self, frame_vel):
        self.x -= frame_vel
        self.x2 -= frame_vel
        if self.x < -1786:
            self.x = self.x + 2 * 1786
        if self.x2 < -1786:
            self.x2 = self.x2 + 2 * 1786


class Bird:
    def __init__(self):
        self.x = 1200
        self.y = random.choices([190, 238, 310])[0]
        self.image = bird_image[0]
        self.count = 0
    def move(self, frame_vel):
        self.x -= frame_vel
        self.count += 1
        if self.count > 11:
            self.count = 0
        self.image = bird_image[self.count // 6]

    def draw(self):
        win.blit(self.image, (self.x, self.y))

    def collide(self, dino):
        if self.y==238:
            if self.x+self.image.get_width()>dino.x+dino.image.get_width()>self.x and self.y+self.image.get_height()>dino.y>self.y:
                return True
            else:
                return False

        else:
            dino_mask = dino.get_mask()
            bird_mask = pygame.mask.from_surface(self.image)
            offset = (self.x - dino.x, self.y - dino.y)
            bpoint = dino_mask.overlap(bird_mask, offset)
            if bpoint:
                return True

            else:
                return False


class Dino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 8
        self.ctime = 0
        self.isJump = False
        self.isDuck = False
        self.image = dino_walk_image[0]
        self.fcount = 0
        self.gcount = 0
        self.d = 0
        self.inv = 1
        self.isJump2 = False
        self.vel2 = 7
        self.inv2 = 1

    def move(self, keys):
        if not self.isJump and not self.isDuck and not self.isJump2:
            self.fcount += 1
            if self.fcount > 5:
                self.fcount = 0
            self.image = dino_walk_image[self.fcount // 3]

        elif self.isJump:
            if self.vel == 0:
                self.inv = -1
            self.image = dino_jump_image
            self.y -= (self.vel ** 2) * self.inv
            self.vel -= 1

            if self.vel == -9:
                self.isJump = False
                self.vel = 8
                self.inv = 1
        elif self.isJump2:
            if self.vel2 == 0:
                self.inv2 = -1
            self.image = dino_jump_image
            self.y -= (self.vel2 ** 2) * self.inv2
            self.vel2 -= 1

            if self.vel2 == -8:
                self.isJump2 = False
                self.vel2 = 7
                self.inv2 = 1
        else:
            self.gcount += 1
            if self.gcount > 5:
                self.gcount = 0
            self.image = dino_duck_image[self.gcount // 3]

    def jump(self):
        self.isJump = True

    def duck(self):
        self.isDuck = True

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def draw(self):

        if self.isDuck:
            self.y=320

        else:
            if not self.isJump and not self.isJump2:
                self.y=275

        win.blit(self.image, (self.x, self.y))


class Cactus:
    def __init__(self, x):
        self.x = x
        rand = random.randrange(0, 6)
        self.img = cactus_image[rand]
        if rand == 1 or rand == 2 or rand == 3 or rand == 4:
            self.y = 300
        else:
            self.y = 265

    def move(self, frame_vel):
        self.x -= frame_vel

    def collide(self, dino):
        dino_mask = dino.get_mask()
        top_mask = pygame.mask.from_surface(self.img)

        top_offset = (self.x - dino.x, self.y - dino.y)
        b_point = dino_mask.overlap(top_mask, top_offset)

        if b_point:
            return True
        else:
            return False

    def draw(self):
        win.blit(self.img, (self.x, self.y))


def redrawWindow(ground, dino, cactuses, score2, birds):
    win.fill((255, 255, 255))
    win.blit(ground_image1, (ground.x, 350))
    win.blit(ground_image1, (ground.x2, 350))
    for cactus in cactuses:
        cactus.draw()
    text = sfont.render(str(int(score2)), 1, (0, 0, 0))
    win.blit(text, (1000, 20))
    for bird in birds:
        bird.draw()
    dino.draw()
    pygame.display.update()

gen=0
def main():
    run = True
    frame_vel = 20
    birds = []
    cactuses = []
    ground = Ground(0)
    dino = Dino(40, 275)
    cact_counter = 0
    score = 0
    score2 = 0
    global gen
    gen+=1
    cact = 30
    bc = 0
    bird_count = 0
    while run:
        clock.tick(30)
        if score < 500:
            score += 0.3
            score2 += 0.3
        elif score < 1000:
            score += 0.6
            score2 += 0.6
        elif score < 2000:
            score += 0.9
            score2 += 0.9
        elif score < 4000:
            score += 1.2
            score2 += 1.2
        elif score < 8000:
            score += 1.5
            score2 += 1.5
        elif score < 16000:
            score += 1.8
            score2 += 1.8
        else:
            score += 3
            score2 += 3
        if bc == 0 and score > 500: bird_count = random.randrange(50, 170)
        if bird_count == 50 and len(cactuses) > 0:
            bc = 1
        else:
            bc = 0
        if bird_count == 50 and len(birds) == 0 and bc == 0:
            birds.append(Bird())
        cact_counter += 1
        if score2 > 700:
            if frame_vel <= 70:
                frame_vel += 10

                score2 = 0
        if cact_counter >= cact and len(birds) == 0 and bc == 0:
            cactuses.append(Cactus(random.randrange(1200, 2200, 100)))
            cact_counter = 0
        for ax, cactus in enumerate(cactuses):
            if ax > 0:
                if abs(cactuses[ax - 1].x - cactus.x) < 600:
                    cactuses.remove(cactus)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for cactus in cactuses:
            cactus.move(frame_vel)
        keys = pygame.key.get_pressed()
        for cactus in cactuses:
            if cactus.collide(dino):
                run = False
        if not dino.isJump and not dino.isJump2:
            if keys[pygame.K_DOWN]:
                dino.duck()
            elif keys[pygame.K_SPACE]:
                dino.isDuck = False
                dino.isJump2 = True
            elif keys[pygame.K_UP]:
                dino.isJump = True
                dino.isDuck = False
            else:
                dino.isDuck = False
        for cactus in cactuses:
            if cactus.x + cactus.img.get_width() < 0:
                cactuses.remove(cactus)
        for bird in birds:
            bird.move(frame_vel)
        for bird in birds:
            if bird.x < -92:
                birds.remove(bird)
        for bird in birds:
            if bird.collide(dino):
                run = False

        dino.move(keys)
        ground.move(frame_vel)
        redrawWindow(ground, dino, cactuses, score, birds)
    pygame.quit()
    quit()


main()
