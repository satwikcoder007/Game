import pygame
from utils.draw_menu import draw_menu
from network import connect_to_server
from firstGame import run_game
from utils.path import resource_path

def start_online_game(win):
    client, player_id, opponent_queue = connect_to_server()
    run_game(client, player_id, opponent_queue, win)
    print("Game ended, closing connection...")
    client.close()
    print("Connection closed.")
def init_menu_window():
    pygame.init()
    pygame.mixer.init()

    win = pygame.display.set_mode((500, 480))
    pygame.display.set_caption("First Game")

    bg = pygame.image.load(resource_path('assets/bg.jpg'))
    title_font = pygame.font.SysFont("comicsans", 40)
    menu_font = pygame.font.SysFont("comicsans", 20)

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
                    print("Starting online game...")
                    start_online_game(win)
                elif event.key == pygame.K_ESCAPE:
                    running = False
    pygame.quit()

if __name__ == "__main__":
    main()