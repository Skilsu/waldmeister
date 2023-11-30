import math

import pygame

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
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption('Waldmeister')
        pygame.font.init()
        self.font_size = 30
        self.font = pygame.font.Font(None, self.font_size)

        self.symbol = False
        self.running = True

    def handle_resize_event(self, event):
        # Update screen size when the window is resized
        self.window_width, self.window_height = event.w, event.h

        self.start_diff = self.window_width * 0.15
        self.end_diff = self.window_width * 0.15
        self.top_diff = self.window_height * 0.15
        self.bottom_diff = self.window_height * 0.3

        self.field_width = (self.window_width - self.start_diff - self.end_diff)
        self.field_height = (self.window_height - self.top_diff - self.bottom_diff)

        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        self.draw_board()

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

    def get_active_positions(self):
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

        if self.game.active:
            x = self.game.active[0]
            toggle = False
            while x > 0:
                x -= 1
                if self.game.field[x][self.game.active[1]] is not None or toggle:
                    toggle = True
                    active_positions[x][self.game.active[1]] = 0
            x = self.game.active[0]
            toggle = False
            while x < 7:
                x += 1
                if self.game.field[x][self.game.active[1]] is not None or toggle:
                    toggle = True
                    active_positions[x][self.game.active[1]] = 0
            y = self.game.active[1]
            toggle = False
            while y > 0:
                y -= 1
                if self.game.field[self.game.active[0]][y] is not None or toggle:
                    toggle = True
                    active_positions[self.game.active[0]][y] = 0
            y = self.game.active[1]
            toggle = False
            while y < 7:
                y += 1
                if self.game.field[self.game.active[0]][y] is not None or toggle:
                    toggle = True
                    active_positions[self.game.active[0]][y] = 0

            x = self.game.active[0]
            y = self.game.active[1]
            toggle = False
            while y > 0 and x < 7:
                y -= 1
                x += 1
                if self.game.field[x][y] is not None or toggle:
                    toggle = True
                    active_positions[x][y] = 0
            x = self.game.active[0]
            y = self.game.active[1]
            toggle = False
            while y < 7 and x > 0:
                y += 1
                x -= 1
                if self.game.field[x][y] is not None or toggle:
                    toggle = True
                    active_positions[x][y] = 0

        return active_positions

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

        active_positions = self.get_active_positions()

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
                        if active_positions[int(x)][int(y)] == 1 and active_positions[int(x + 1)][int(y - 1)] == 1 and self.game.active[1] + self.game.active[0] == int(
                                x) + int(y):
                            pygame.draw.line(self.screen, (25, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond, y_diamond + (self.field_height / 7)), radius)
                        else:
                            pygame.draw.line(self.screen, (150, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond, y_diamond + (self.field_height / 7)), radius)
                    # diagonal forward
                    if x < 7:
                        pygame.draw.line(self.screen, (0, 0, 0),
                                         (x_diamond, y_diamond),
                                         (x_diamond + self.field_width / 14, y_diamond + (self.field_height / 14)),
                                         radius + 2)
                        if active_positions[int(x)][int(y)] == 1 and active_positions[int(x + 1)][int(y)] == 1 and self.game.active[1] == int(y):
                            pygame.draw.line(self.screen, (25, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond + self.field_width / 14, y_diamond + (self.field_height / 14)),
                                             radius)
                        else:
                            pygame.draw.line(self.screen, (150, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond + self.field_width / 14, y_diamond + (self.field_height / 14)),
                                             radius)
                    # diagonal backwards
                    if y > 0:
                        pygame.draw.line(self.screen, (0, 0, 0),
                                         (x_diamond, y_diamond),
                                         (x_diamond - self.field_width / 14, y_diamond + (self.field_height / 14)),
                                         radius + 2)
                        if active_positions[int(x)][int(y)] == 1 and active_positions[int(x)][int(y - 1)] == 1 and self.game.active[0] == int(x):
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
                    if self.game.active and x == self.game.active[0] and y == self.game.active[1]:
                        pygame.draw.circle(self.screen, (150, 150, 50),
                                           (x_diamond, y_diamond), radius)
                    else:
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

        edge = min(edge_vertical, edge_horizontal)
        width = self.window_width / 3
        height = self.bottom_diff - edge * 1.5
        radius = int((self.field_width + self.field_height) / 110)
        hight_multiplier = radius / 12

        x = edge * 0.5
        y = self.window_height - self.bottom_diff + edge
        for player in self.game.player:
            pygame.draw.rect(self.screen, (30, 30, 30),
                             (x, y, width, height))
            for idx, i in enumerate(player):
                for jdx, j in enumerate(i):
                    if jdx == 0:
                        a = 7  # red
                        b = 0
                        c = 0
                    elif jdx == 1:
                        a = 0
                        b = 1
                        c = 5  # blue
                    else:
                        a = 0
                        b = 7  # green
                        c = 1
                    for k in range(3 - j):
                        if self.symbol:
                            if idx == 0:
                                pygame.draw.circle(self.screen, (0, 0, 0), (x + (1 + idx) * width / 4 + width / 16 * k, y + (1 + jdx) * height / 4),
                                                   radius * 1.5 + 1)  # black circle
                                pygame.draw.circle(self.screen, (a * 30, b * 30, c * 30), (x + (1 + idx) * width / 4 + width / 16 * k, y + (1 + jdx) * height / 4),
                                                   radius * 1.5)  # circle
                            elif idx == 1:
                                pygame.draw.rect(self.screen, (0, 0, 0),
                                                 ((x + (1 + idx) * width / 4 + width / 16 * k) - radius * 1.4 - 1, (y + (1 + jdx) * height / 4) - radius * 1.4 - 1,
                                                  radius * 2.8 + 2, radius * 2.8 + 2))  # black square
                                pygame.draw.rect(self.screen, (a * 30, b * 30, c * 30),
                                                 ((x + (1 + idx) * width / 4 + width / 16 * k) - radius * 1.4, (y + (1 + jdx) * height / 4) - radius * 1.4,
                                                  radius * 2.8, radius * 2.8))  # colored square
                            else:
                                height_triangle = math.sqrt(3) * radius * 2

                                # Calculate the coordinates of the three corners
                                x1 = x + (1 + idx) * width / 4 + width / 16 * k
                                y1 = (y + (1 + jdx) * height / 4) - height_triangle / 2 - radius / 2

                                x2 = (x + (1 + idx) * width / 4) - radius * 2 + width / 16 * k
                                y2 = (y + (1 + jdx) * height / 4) + height_triangle / 2 - radius / 2

                                x3 = (x + (1 + idx) * width / 4) + radius * 2 + width / 16 * k
                                y3 = (y + (1 + jdx) * height / 4) + height_triangle / 2 - radius / 2
                                pygame.draw.polygon(self.screen, (0, 0, 0),
                                                    [(x1, y1 - 2), (x2 - 1.5, y2 + 1),
                                                     (x3 + 1.5, y3 + 1)])  # black triangle
                                pygame.draw.polygon(self.screen, (a * 30, b * 30, c * 30),
                                                    [(x1, y1), (x2, y2), (x3, y3)])  # colored triangle

                        else:
                            # black background stick
                            for l in range(10 + 10 * idx):
                                pygame.draw.circle(self.screen, (0, 0, 0),
                                                   ((x + (1 + idx) * width / 4 + width / 16 * k) + l * 1 * hight_multiplier,
                                                    (y + (1 + jdx) * height / 4) - l * 2 * hight_multiplier), radius + 1)

                            # sticks with different color and height
                            for l in range(10 + 10 * idx):
                                if l == 10 + 10 * idx - 1:
                                    pygame.draw.circle(self.screen, (0, 0, 0),
                                                       ((x + (1 + idx) * width / 4 + width / 16 * k) + l * 1 * hight_multiplier,
                                                        (y + (1 + jdx) * height / 4) - l * 2 * hight_multiplier), radius + 1)
                                pygame.draw.circle(self.screen, (50 + l * a, 50 + l * b, 50 + l * c),
                                                   ((x + (1 + idx) * width / 4 + width / 16 * k) + l * 1 * hight_multiplier,
                                                    (y + (1 + jdx) * height / 4) - l * 2 * hight_multiplier), radius)

            x = self.window_width - width - edge * 0.5
            y = self.window_height - self.bottom_diff + edge
        '''
        self.start_diff = self.window_width * 0.15
        self.end_diff = self.window_width * 0.15
        self.top_diff = self.window_height * 0.15
        self.bottom_diff = self.window_height * 0.3
        '''

        pygame.display.update()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize_event(event)
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
        if self.game.field[position[0]][position[1]]:
            self.game.active = position

    def run_game(self):
        self.draw_board()
        while self.running:
            self.handle_event()


if __name__ == "__main__":
    game = WaldmeisterGame()
    gui = PygameWaldmeisterGUI(game)
    game.field[2][4] = [2, 1]
    game.field[4][5] = [1, 2]
    game.field[2][6] = [2, 2]
    game.field[0][0] = [1, 0]
    game.field[0][4] = [0, 1]
    game.field[7][6] = [1, 0]
    game.field[6][0] = [0, 2]
    game.field[5][5] = [1, 2]
    gui.run_game()
