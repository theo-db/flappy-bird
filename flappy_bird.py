import pygame, random

def main():
    width = 800
    height = 600
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("flappy bird")
    font = pygame.font.SysFont("monospace", 50)

    #load images
    pipeU = pygame.image.load("pipe1.png")
    pipeD = pygame.image.load("pipe2.png")
    birds = list(map(pygame.image.load, ["bird1.png", "bird2.png"]))

    #dimensions for the images
    bird_dim = [60,40]
    pipe_dim = [100, height]

    #resize images
    pipeU = pygame.transform.scale(pipeU, pipe_dim)
    pipeD = pygame.transform.scale(pipeD, pipe_dim)
    birds = list(map(pygame.transform.scale, birds, [bird_dim,]*2))
    
    done = False
    def game():
        nonlocal done
        started = False
        fail = False
        bounce = -2
        gravity = 0.02
        position = [100, (height-bird_dim[1])/2]
        pipesU = []
        pipesD = []
        passed = []
        velocity = 0
        speed = 1
        min_gap = 200 #gaps between the two pipes for the bird to fly through
        max_gap = 300
        padding = 50 #minimum distance between the gap and the edge of the screen
        min_spacing = 200 #the distance between horizontally adjacent pipes
        max_spacing = 500
        spacing = 0
        score = 0

        def draw():
            screen.fill((255,255,255))
            for pos in pipesU:
                screen.blit(pipeU, pos)
            for pos in pipesD:
                screen.blit(pipeD, pos)
            screen.blit(birds[0], position)
            t = font.render(str(score), False, (0,0,0))
            size = t.get_rect()
            screen.blit(t, ((width-size[2])/2, 10))
            pygame.display.flip()
            pygame.time.wait(1)

        def collide():
            nonlocal fail, passed, score
            for i in range(len(pipesU + pipesD)):
                p = (pipesU + pipesD)[i]
                if all((position[1] < p[1] + pipe_dim[1],
                       position[1] + bird_dim[1] > p[1],
                       position[0] + bird_dim[0] > p[0],
                       position[0] < p[0] + pipe_dim[0])):
                    fail = True
                if i < len(pipesU):
                    if position[0] > p[0] + pipe_dim[0] and not passed[i]:
                        passed[i] = True
                        score += 1
            if position[1] < 0:
                fail = True
            elif position[1] + bird_dim[1] > height:
                fail = True               

        def add_pipe():
            nonlocal spacing, pipesU, pipesD, passed
            gap = random.randint(min_gap, max_gap)
            heightD = random.randint(gap+padding, height-padding)
            heightU = heightD - pipe_dim[1] - gap
            pipesU.append([width, heightU])
            pipesD.append([width, heightD])
            passed.append(False)
            spacing = random.randint(min_spacing, max_spacing)

        def move():
            nonlocal pipesU, pipesD
            for i in range(len(pipesU)):
                pipesU[i][0] -= speed
            for i in range(len(pipesD)):
                pipesD[i][0] -= speed
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not started:
                            started = True
                        velocity = bounce

            draw()
            if not started:
                continue
            velocity += gravity
            position[1] += velocity

            #find if pipes need to be added or taken away
            if len(pipesU) > 0:
                if width - (pipesU[-1][0] + pipe_dim[0]) > spacing:
                    add_pipe()
                if pipesU[0][0] + pipe_dim[0] < 0:
                    del pipesU[0]
                    del pipesD[0]
                    del passed[0]    
            elif len(pipesU) == 0:
                add_pipe()
                
            collide()
            move()
            if fail:
                break
                            
    while not done:
        game()
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
    finally:
        pygame.quit()
