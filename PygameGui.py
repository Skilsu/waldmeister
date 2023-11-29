import math
import sys

import pygame
from pygame import Rect
from pygame.locals import QUIT, MOUSEBUTTONDOWN

from game import WaldmeisterGame


class PygameWaldmeisterGUI:

    def __init__(self, game):
        self.window_width = 1400
        self.window_height = 800

        self.start_diff = self.window_width * 0.15
        self.end_diff = self.window_width * 0.15
        self.top_diff = self.window_height * 0.15
        self.bottom_diff = self.window_height * 0.3

        self.field_width = (self.window_width - self.start_diff - self.end_diff)
        self.field_height = (self.window_height - self.top_diff - self.bottom_diff)

        self.game = game
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Waldmeister')
        pygame.font.init()
        self.font_size = 30
        self.font = pygame.font.Font(None, self.font_size)

        self.symbol = True
        self.running = True

    def symbol_toggle(self):
        pygame.draw.line(self.screen, (255, 255, 255),
                         (self.window_width - 75, 49),
                         (self.window_width - 100, 49),
                         20)
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (self.window_width - 75, 50), 10)
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (self.window_width - 100, 50), 10)
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.window_width - 75, 49),
                         (self.window_width - 100, 49),
                         18)
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (self.window_width - 75, 50), 9)
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (self.window_width - 100, 50), 9)

        if self.symbol:
            text_surface = self.font.render("Symbols", True, (255, 255, 255))

            pygame.draw.circle(self.screen, (255, 255, 255),
                               (self.window_width - 100, 50), 15)
        else:
            text_surface = self.font.render("Sticks", True, (255, 255, 255))
            pygame.draw.circle(self.screen, (255, 255, 255),
                               (self.window_width - 75, 50), 15)

        text_rect = text_surface.get_rect()
        text_rect.center = (self.window_width - 88, 90)
        self.screen.blit(text_surface, text_rect)

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        self.symbol_toggle()

        edge_vertical = self.field_height / 14
        edge_horizontal = self.field_width / 14
        pygame.draw.polygon(self.screen, (125, 75, 0),
                            [(self.start_diff + self.field_width / 2, self.top_diff - edge_vertical),
                             (self.start_diff - edge_horizontal, self.top_diff + self.field_height / 2),
                             (
                                 self.start_diff + self.field_width / 2,
                                 self.top_diff + self.field_height + edge_vertical),
                             (self.start_diff + self.field_width + edge_horizontal,
                              self.top_diff + self.field_height / 2)])

        # find active positions to draw allowed lines
        active_positions = []
        for i in range(8):
            active_row = []
            for j in range(8):
                if self.game.active and (i == self.game.active[0]
                                         or j == self.game.active[1]
                                         or self.game.active[1] + self.game.active[0] == i + j):
                    active_row.append(1)
                else:
                    active_row.append(0)
            active_positions.append(active_row)

        # draw lines and dots
        x = -4
        y = 3
        for i in range(15):
            old_x = x
            old_y = y
            for j in range(15):
                x += 0.5
                y += 0.5
                if 0 <= x < 8 and 0 <= y < 8 and y == int(y) and x == int(x):
                    x_diamond = (j * self.field_width / 14 + self.start_diff)
                    y_diamond = (i * self.field_height / 14 + self.top_diff)
                    radius = int((self.field_width + self.field_height) / 110)
                    hight_multiplier = radius / 12

                    # draw lines
                    if y > 0 and x < 7:
                        pygame.draw.line(self.screen, (0, 0, 0),
                                         (x_diamond, y_diamond),
                                         (x_diamond, y_diamond + (self.field_height / 7)), radius + 2)
                        if active_positions[int(x)][int(y)] == 1 and self.game.active[1] + self.game.active[0] == int(
                                x) + int(y):
                            pygame.draw.line(self.screen, (25, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond, y_diamond + (self.field_height / 7)), radius)
                        else:
                            pygame.draw.line(self.screen, (150, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond, y_diamond + (self.field_height / 7)), radius)

                    if x < 7:
                        pygame.draw.line(self.screen, (0, 0, 0),
                                         (x_diamond, y_diamond),
                                         (x_diamond + self.field_width / 14, y_diamond + (self.field_height / 14)),
                                         radius + 2)
                        if active_positions[int(x)][int(y)] == 1 and self.game.active[1] == int(y):
                            pygame.draw.line(self.screen, (25, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond + self.field_width / 14, y_diamond + (self.field_height / 14)),
                                             radius)
                        else:
                            pygame.draw.line(self.screen, (150, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond + self.field_width / 14, y_diamond + (self.field_height / 14)),
                                             radius)

                    if y > 0:
                        pygame.draw.line(self.screen, (0, 0, 0),
                                         (x_diamond, y_diamond),
                                         (x_diamond - self.field_width / 14, y_diamond + (self.field_height / 14)),
                                         radius + 2)
                        if active_positions[int(x)][int(y)] == 1 and self.game.active[0] == int(x):
                            pygame.draw.line(self.screen, (25, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond - self.field_width / 14, y_diamond + (self.field_height / 14)),
                                             radius)
                        else:
                            pygame.draw.line(self.screen, (150, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond - self.field_width / 14, y_diamond + (self.field_height / 14)),
                                             radius)
                    # empty holes
                    pygame.draw.circle(self.screen, (0, 0, 0),
                                       (x_diamond, y_diamond), radius + 1)
                    pygame.draw.circle(self.screen, (110, 65, 0),
                                       (x_diamond, y_diamond), radius)

                    '''
                    # maybe ellipse for 3d effect
                    pygame.draw.ellipse(self.screen, (0, 0, 0),
                                        Rect(x_diamond - radius, y_diamond - radius, radius * 2, radius * 2))
                    '''

                    # sticks depending on height and color
                    if self.game.field[int(x)][int(y)] is not None:
                        if self.game.field[int(x)][int(y)][1] == 0:
                            a = 7  # red
                            b = 0
                            c = 0
                        elif self.game.field[int(x)][int(y)][1] == 1:
                            a = 0
                            b = 1
                            c = 5  # blue
                        else:
                            a = 0
                            b = 7  # green
                            c = 1

                        '''
                        # shadow (not quite convincing)
                        for k in range(10 + 10 * self.game.field[int(x)][int(y)][0]):
                            pygame.draw.circle(self.screen, (k * 6, k * 4, 0),
                                               (x_diamond + k * 1, y_diamond - k * 1), radius)
                        '''
                        if self.symbol:
                            if self.game.field[int(x)][int(y)][0] == 0:
                                pygame.draw.circle(self.screen, (0, 0, 0), (x_diamond, y_diamond),
                                                   radius * 1.5 + 1)  # black circle
                                pygame.draw.circle(self.screen, (a * 30, b * 30, c * 30), (x_diamond, y_diamond),
                                                   radius * 1.5)  # circle
                            elif self.game.field[int(x)][int(y)][0] == 1:
                                pygame.draw.rect(self.screen, (0, 0, 0),
                                                 (x_diamond - radius * 1.4 - 1, y_diamond - radius * 1.4 - 1,
                                                  radius * 2.8 + 2, radius * 2.8 + 2))  # black square
                                pygame.draw.rect(self.screen, (a * 30, b * 30, c * 30),
                                                 (x_diamond - radius * 1.4, y_diamond - radius * 1.4,
                                                  radius * 2.8, radius * 2.8))  # colored square
                            else:
                                height = math.sqrt(3) * radius * 2

                                # Calculate the coordinates of the three corners
                                x1 = x_diamond
                                y1 = y_diamond - height / 2 - radius / 2

                                x2 = x_diamond - radius * 2
                                y2 = y_diamond + height / 2 - radius / 2

                                x3 = x_diamond + radius * 2
                                y3 = y_diamond + height / 2 - radius / 2
                                pygame.draw.polygon(self.screen, (0, 0, 0),
                                                    [(x1, y1 - 2), (x2 - 1.5, y2 + 1),
                                                     (x3 + 1.5, y3 + 1)])  # black triangle
                                pygame.draw.polygon(self.screen, (a * 30, b * 30, c * 30),
                                                    [(x1, y1), (x2, y2), (x3, y3)])  # colored triangle

                        else:
                            # black background stick
                            for k in range(10 + 10 * self.game.field[int(x)][int(y)][0]):
                                pygame.draw.circle(self.screen, (0, 0, 0),
                                                   (x_diamond + k * 1 * hight_multiplier,
                                                    y_diamond - k * 2 * hight_multiplier), radius + 1)

                            # sticks with different color and height
                            for k in range(10 + 10 * self.game.field[int(x)][int(y)][0]):
                                if k == 10 + 10 * self.game.field[int(x)][int(y)][0] - 1:
                                    pygame.draw.circle(self.screen, (0, 0, 0),
                                                       (x_diamond + k * 1 * hight_multiplier,
                                                        y_diamond - k * 2 * hight_multiplier), radius + 1)
                                pygame.draw.circle(self.screen, (50 + k * a, 50 + k * b, 50 + k * c),
                                                   (x_diamond + k * 1 * hight_multiplier,
                                                    y_diamond - k * 2 * hight_multiplier), radius)

            x = old_x + 0.5
            y = old_y - 0.5

        x = -4
        y = 3
        for i in range(15):
            old_x = x
            old_y = y
            for j in range(15):
                x += 0.5
                y += 0.5
                if 0 <= x < 7 and 0 <= y < 7 and y == int(y) and x == int(x):
                    x_diamond = j * self.window_width / 17.5 + self.window_width / 10
                    y_diamond = i * self.window_height / 17.5 + self.window_height / 10
                    color = (125, 75, 0)
                    """pygame.draw.polygon(self.screen, color,
                                        [(x_diamond + 2, y_diamond - self.window_height / 20),
                                         (x_diamond + self.window_width / 20, y_diamond),
                                         (x_diamond + 2, y_diamond + self.window_height / 20)])

                    pygame.draw.polygon(self.screen, color,
                                        [(x_diamond - 2, y_diamond - self.window_height / 20),
                                         (x_diamond - 2, y_diamond + self.window_height / 20),
                                         (x_diamond - self.window_width / 20, y_diamond)])
"""
            x = old_x + 0.5
            y = old_y - 0.5

        pygame.display.update()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if the mouse click is inside any of the circles on the board
                x = -4
                y = 3
                for i in range(15):
                    old_x = x
                    old_y = y
                    for j in range(15):
                        x += 0.5
                        y += 0.5
                        if 0 <= x < 8 and 0 <= y < 8 and y == int(y) and x == int(x):
                            x_diamond = (j * self.field_width / 14 + self.start_diff)
                            y_diamond = (i * self.field_height / 14 + self.top_diff)
                            radius = int((self.field_width + self.field_height) / 110)

                            # Check if the mouse click is inside the current circle
                            if (
                                    (mouse_x - x_diamond) ** 2 + (mouse_y - y_diamond) ** 2
                            ) ** 0.5 <= radius + 5:
                                self.action([int(x), int(y)])
                    x = old_x + 0.5
                    y = old_y - 0.5
                if self.window_width - 115 < mouse_x < self.window_width - 60 and 35 < mouse_y < 65:
                    self.symbol = not self.symbol
                self.draw_board()

    def action(self, position):
        self.game.active = position

    def run_game(self):
        self.draw_board()
        while self.running:
            self.handle_event()


if __name__ == "__main__":
    game = WaldmeisterGame()
    gui = PygameWaldmeisterGUI(game)
    game.active = [1, 3]
    game.field[2][4] = [2, 1]
    game.field[4][5] = [1, 2]
    game.field[2][6] = [2, 2]
    game.field[0][0] = [1, 0]
    game.field[0][4] = [0, 1]
    game.field[7][6] = [1, 0]
    game.field[6][0] = [0, 2]
    game.field[5][5] = [1, 2]
    gui.run_game()
