import pygame
import random
import neat
import os
pygame.init()
cactus_image = [pygame.image.load("images/bigcactus.png"), pygame.image.load("images/smallcactus.png"),
                pygame.image.load("images/manycactus.png"), pygame.image.load("images/manycactus2.png"),
                pygame.image.load("images/manycactus3.png"), pygame.image.load("images/smallcactus2.png")]
dino_walk_image = [pygame.image.load("images/dinorun1.png"), pygame.image.load("images/dinorun2.png")]
dino_duck_image = [pygame.image.load("images/dinoduck1.png"), pygame.image.load("images/dinoduck2.png")]
dino_jump_image = pygame.image.load("images/dinojump.png")
bird_image = [pygame.image.load("images/bird1.png"), pygame.image.load("images/bird2.png")]
ground_image1 = pygame.image.load("images/ground.png")
ground_image2 = pygame.image.load("images/ground.png")
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

    def move(self):
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
            win.blit(self.image, (self.x, self.y))
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


def redrawWindow(ground, dinos, cactuses, score2, birds,length):
    win.fill((255, 255, 255))
    win.blit(ground_image1, (ground.x, 350))
    win.blit(ground_image1, (ground.x2, 350))
    for cactus in cactuses:
        cactus.draw()
    text = sfont.render(str(int(score2)), 1, (0, 0, 0))
    win.blit(text, (1000, 20))
    text1 = sfont.render("Alive: "+str(int(length)), 1, (0, 0, 0))
    win.blit(text1, (500, 20))
    text3 = sfont.render("Gen: "+str(int(gen)), 1, (0, 0, 0))
    win.blit(text3, (80, 20))
    for bird in birds:
        bird.draw()
    for dino in dinos:
        dino.draw()
    pygame.display.update()

gen=0
def main(genomes, config):
    run = True
    frame_vel = 20
    birds = []
    cactuses = []
    ground = Ground(0)
    global gen
    gen+=1
    dinos = []
    nets = []
    ge = []
    for l, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dino(40, 275))
        g.fitness = 0
        ge.append(g)

    cact_counter = 0
    score = 0
    score2 = 0
    cact = 30
    bc = 0
    bird_count = 0


    while run:

        clock.tick(30)

        cactuses_copy = []
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
        if bc == 0 and score > 0: bird_count = random.randrange(50, 170)
        if bird_count == 50 and len(cactuses) > 0:
            bc = 1
        else:
            bc = 0
        if bird_count == 50 and len(birds) == 0 and bc == 0:
            birds.append(Bird())
        cact_counter += 1
        if score2 > 100:
            if frame_vel <= 50:
                frame_vel += 5

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
                pygame.quit()
                quit()
        for cactus in cactuses:
            cactus.move(frame_vel)

        for cactus in cactuses:
            for x,dino in enumerate(dinos):
                if cactus.collide(dino):
                    dinos.remove(dino)
                    ge[x].fitness -= 2
                    nets.pop(x)
                    ge.pop(x)
        if len(dinos)==0:

            break

        for cactus in cactuses:
            if cactus.x + cactus.img.get_width() < 0:
                cactuses.remove(cactus)
        for bird in birds:
            bird.move(frame_vel)
        for bird in birds:
            if bird.x < -92:
                birds.remove(bird)
        for bird in birds:
            for x,dino in enumerate(dinos):
                if bird.collide(dino):
                    dinos.remove(dino)
                    ge[x].fitness -= 2
                    nets.pop(x)
                    ge.pop(x)
        if len(dinos)==0:

            break
        length=len(dinos)
        if len(birds)==0:
            birx=-1
            biry = -1
        else:
            birx=birds[0].x
            biry = birds[0].y
        for cactus in cactuses:
            cactuses_copy.append(cactus.x)
        cactuses_copy.sort()
        for cact in cactuses_copy:
            if cact<dinos[0].x:
                cactuses_copy.remove(cact)
        if len(cactuses_copy)==0:
            next_cact=-1
            next_cact2 = -1
        elif len(cactuses_copy)==1:
            next_cact=cactuses_copy[0]
            next_cact2=-1
        else:
            next_cact = cactuses_copy[0]
            next_cact2 = cactuses_copy[1]
        for ind,dino in enumerate(dinos):
            dino.move()
            ge[ind].fitness += 0.1
            output = nets[ind].activate(
                (dino.y,frame_vel,next_cact,next_cact2,birx,biry))
            keys=output.index(max(output))
            if not dino.isJump and not dino.isJump2:
                if keys==0:
                    dino.duck()
                elif keys==1:
                    dino.isDuck = False
                    dino.isJump2 = True
                elif keys==2:
                    dino.isDuck = False
                    dino.isJump = True
                else:
                    dino.isDuck = False

        for x,dino in enumerate(dinos):
            if dino.image not in dino_duck_image and dino.y>280:
                dinos.pop(x)
                ge[x].fitness-=10
                ge.pop(x)
                nets.pop(x)

            elif dino.image in dino_duck_image and dino.y<310:
                dinos.pop(x)
                ge[x].fitness-=10
                ge.pop(x)
                nets.pop(x)

        ground.move(frame_vel)
        redrawWindow(ground, dinos, cactuses, score, birds,length)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,config_file)
    p = neat.Population(config)
    p.run(main, 10000)


if 1>0:
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
