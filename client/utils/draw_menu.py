import pygame

def draw_text_center(win, text, font, color, y, shadow=True):
    text_surface = font.render(text, True, color)

    x = win.get_width() // 2 - text_surface.get_width() // 2

    # shadow for readability
    if shadow:
        shadow_surface = font.render(text, True, (0, 0, 0))
        win.blit(shadow_surface, (x + 2, y + 2))

    win.blit(text_surface, (x, y))


def draw_menu(win, title_font,menu_font, bg):
    # draw background
    win.blit(bg, (0, 0))

    # 🔹 dark transparent overlay (makes everything readable)
    overlay = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))   # last value = transparency
    win.blit(overlay, (0, 0))

    # 🔹 centered panel (game-style UI box)
    panel_width = 420
    panel_height = 220
    panel_x = win.get_width() // 2 - panel_width // 2
    panel_y = 120

    pygame.draw.rect(win, (30, 30, 30), (panel_x, panel_y, panel_width, panel_height), border_radius=12)
    pygame.draw.rect(win, (200, 200, 200), (panel_x, panel_y, panel_width, panel_height), 2, border_radius=12)

    # 🔹 text
    draw_text_center(win, "Battle Master", title_font, (255, 255, 255), panel_y + 20)
    draw_text_center(win, "Press ENTER to Play", menu_font, (220, 220, 220), panel_y + 100)
    draw_text_center(win, "Press ESC to Quit", menu_font, (220, 220, 220), panel_y + 140)

    pygame.display.update()