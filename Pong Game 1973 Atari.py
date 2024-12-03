import pygame, sys, random

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = screen_width / 2 - 10
    ball.y = random.randint(10, 100)
    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])

def point_won(winner):
    global cpu_points, player_points

    if winner == "player1":
        cpu_points += 1
    if winner == "player2":
        player_points += 1

    reset_ball()

def animate_ball():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    if ball.right >= screen_width:
        point_won("player2")

    if ball.left <= 0:
        point_won("player1")

    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1
        pong_sound.play()  # PLAY SOUND WHEN THE BALL IS HIT

def animate_player1():
    player1.y += player1_speed

    if player1.top <= 0:
        player1.top = 0

    if player1.bottom >= screen_height:
        player1.bottom = screen_height

def animate_player2():
    player2.y += player2_speed

    if player2.top <= 0:
        player2.top = 0

    if player2.bottom >= screen_height:
        player2.bottom = screen_height

# GAME OVER FUNCTIONS
def display_game_over():
    game_over_font = pygame.font.Font("Pong Score.ttf", 100)
    game_over_surface = game_over_font.render("GAME OVER", True, "yellow")
    screen.blit(game_over_surface, (screen_width / 2 - game_over_surface.get_width() / 2, screen_height / 2 - game_over_surface.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)  # WAIT 3 SECONDS BEFORE LEAVING
    pygame.quit()
    sys.exit()

pygame.init()

screen_width = 1280
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong Game!")

clock = pygame.time.Clock()

ball = pygame.Rect(0, 0, 30, 30)
ball.center = (screen_width / 2, screen_height / 2)

player1 = pygame.Rect(0, 0, 20, 100) 
player1.midleft = (20, screen_height / 2)

player2 = pygame.Rect(0, 0, 20, 100) 
player2.midright = (screen_width - 20, screen_height / 2) 

ball_speed_x = 6
ball_speed_y = 6
player1_speed = 0
player2_speed = 0

cpu_points, player_points = 0, 0

# FONT SCORE
score_font = pygame.font.Font("Pong Score.ttf", 60)

# LOADING SOUND
pong_sound = pygame.mixer.Sound("pong_sound.wav")

while True:
    # CHECK FOR EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # PLAYER A = KEY W
                player1_speed = -6
            if event.key == pygame.K_s:  # PLAYER A = KEY S
                player1_speed = 6
            if event.key == pygame.K_UP:  # PLAYER B = KEY UP
                player2_speed = -6
            if event.key == pygame.K_DOWN:  # PLAYER B = KEY DOWN
                player2_speed = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w: 
                player1_speed = 0
            if event.key == pygame.K_s: 
                player1_speed = 0
            if event.key == pygame.K_UP: 
                player2_speed = 0
            if event.key == pygame.K_DOWN:
                player2_speed = 0

    # CHANGE THE POSITIONS OF THE GAME OBJECTS
    animate_ball()
    animate_player1()
    animate_player2()
        
    # CLEAR THE SCREEN
    screen.fill('black')

    # DRAW THE SCORE 
    cpu_score_surface = score_font.render(str(cpu_points), True, "white")
    player_score_surface = score_font.render(str(player_points), True, "white")
    
    # POSITION THE SCORE
    screen.blit(cpu_score_surface, (screen_width / 4 + 50, 20))
    screen.blit(player_score_surface, (3 * screen_width / 4 - 150, 20))

    # DRAW THE GAME OBJECTS
    pygame.draw.aaline(screen, 'white', (screen_width / 2, 0), (screen_width / 2, screen_height), 20)
    pygame.draw.ellipse(screen, 'yellow', ball)
    pygame.draw.rect(screen, 'white', player1)
    pygame.draw.rect(screen, 'white', player2)

    # CHECK IF ANYONE HAS REACHED 10 POINTS
    if cpu_points >= 10 or player_points >= 10:
        display_game_over()  # VIEW THE MESSAGE OF GAME OVER

    # UPDATE THE DISPLAY
    pygame.display.update()
    clock.tick(80)
