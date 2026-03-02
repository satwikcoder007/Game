import pygame
from utils.draw_menu import draw_menu
from network import connect_to_server
from firstGame import run_game

def start_online_game():
    client, player_id, opponent_queue = connect_to_server()
    run_game(client, player_id, opponent_queue)

def init_menu_window():
    pygame.init()
    pygame.mixer.init()

    win = pygame.display.set_mode((600, 480))
    pygame.display.set_caption("First Game")

    bg = pygame.image.load('assets/bg.jpg')
    title_font = pygame.font.SysFont("comicsans", 50)
    menu_font = pygame.font.SysFont("comicsans", 25)

    return win, bg, title_font, menu_font

def main():
    
    win, bg, title_font, menu_font = init_menu_window()
    running = True
    while running:
        draw_menu(win, title_font, menu_font, bg)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_online_game()
                    win, bg, title_font, menu_font = init_menu_window()
    pygame.quit()

if __name__ == "__main__":
    main()