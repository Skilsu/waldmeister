import math

import pygame

from WaldmeisterGame import WaldmeisterGame


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
        self.font_size = 28
        self.font = pygame.font.Font(None, self.font_size)
        self.font_size = 40
        self.font_large = pygame.font.Font(None, self.font_size)

        self.symbol = False
        self.color_scheme = True
        self.running = True
        self.active_positions = [[0 for _ in range(8)] for _ in range(8)]
        self.chosen_color = [None for _ in range(3)]
        self.winner = None

    def handle_resize_event(self, event):
        # Update screen size when the window is resized
        self.window_width, self.window_height = event.w, event.h

        self.start_diff = self.window_width * 0.2
        self.end_diff = self.window_width * 0.2
        self.top_diff = self.window_height * 0.1
        self.bottom_diff = self.window_height * 0.4

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

    def color_toggle(self):
        pygame.draw.line(self.screen, (255, 255, 255),
                         (self.window_width - 75, 149),
                         (self.window_width - 100, 149),
                         20)
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (self.window_width - 75, 150), 10)
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (self.window_width - 100, 150), 10)
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.window_width - 75, 149),
                         (self.window_width - 100, 149),
                         18)
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (self.window_width - 75, 150), 9)
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (self.window_width - 100, 150), 9)

        if self.color_scheme:
            text_surface = self.font.render("Default", True, (255, 255, 255))
            pygame.draw.circle(self.screen, (255, 255, 255),
                               (self.window_width - 75, 150), 15)
        else:
            text_surface = self.font.render("Colored", True, (255, 255, 255))
            pygame.draw.circle(self.screen, (255, 255, 255),
                               (self.window_width - 100, 150), 15)

        text_rect = text_surface.get_rect()
        text_rect.center = (self.window_width - 88, 190)
        self.screen.blit(text_surface, text_rect)

    def get_active_positions(self):
        # find active positions to draw allowed lines
        active_positions = []
        for i in range(8):
            active_row = []
            for j in range(8):
                if self.game.active_start and (i == self.game.active_start[0]
                                               or j == self.game.active_start[1]
                                               or self.game.active_start[1] + self.game.active_start[0] == i + j):
                    active_row.append(1)
                else:
                    active_row.append(0)
            active_positions.append(active_row)

        if self.game.active_start:
            x = self.game.active_start[0]
            toggle = False
            while x > 0:
                x -= 1
                if self.game.field[x][self.game.active_start[1]] is not None or toggle:
                    toggle = True
                    active_positions[x][self.game.active_start[1]] = 0
            x = self.game.active_start[0]
            toggle = False
            while x < 7:
                x += 1
                if self.game.field[x][self.game.active_start[1]] is not None or toggle:
                    toggle = True
                    active_positions[x][self.game.active_start[1]] = 0
            y = self.game.active_start[1]
            toggle = False
            while y > 0:
                y -= 1
                if self.game.field[self.game.active_start[0]][y] is not None or toggle:
                    toggle = True
                    active_positions[self.game.active_start[0]][y] = 0
            y = self.game.active_start[1]
            toggle = False
            while y < 7:
                y += 1
                if self.game.field[self.game.active_start[0]][y] is not None or toggle:
                    toggle = True
                    active_positions[self.game.active_start[0]][y] = 0

            x = self.game.active_start[0]
            y = self.game.active_start[1]
            toggle = False
            while y > 0 and x < 7:
                y -= 1
                x += 1
                if self.game.field[x][y] is not None or toggle:
                    toggle = True
                    active_positions[x][y] = 0
            x = self.game.active_start[0]
            y = self.game.active_start[1]
            toggle = False
            while y < 7 and x > 0:
                y += 1
                x -= 1
                if self.game.field[x][y] is not None or toggle:
                    toggle = True
                    active_positions[x][y] = 0

        self.active_positions = active_positions

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        self.symbol_toggle()
        self.color_toggle()

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

        self.get_active_positions()

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
                        if self.active_positions[int(x)][int(y)] == 1 and self.active_positions[int(x + 1)][
                            int(y - 1)] == 1 and self.game.active_start[1] + self.game.active_start[0] == int(
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
                        if self.active_positions[int(x)][int(y)] == 1 and self.active_positions[int(x + 1)][
                            int(y)] == 1 and self.game.active_start[1] == int(y):
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
                        if self.active_positions[int(x)][int(y)] == 1 and self.active_positions[int(x)][
                            int(y - 1)] == 1 and self.game.active_start[0] == int(x):
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
                    if self.game.active_end and x == self.game.active_end[0] and y == self.game.active_end[1]:
                        pygame.draw.circle(self.screen, (25, 150, 50),
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
                        a, b, c = 0, 0, 0
                        for kdx in range(3):
                            if kdx == self.game.field[int(x)][int(y)][1]:
                                if self.color_scheme:
                                    if self.game.field[int(x)][int(y)][1] == 0:  # olive (dark green)
                                        b = 2
                                    elif self.game.field[int(x)][int(y)][1] == 1:  # green
                                        b = 7
                                    else:  # yellow
                                        a = 7
                                        b = 7
                                else:
                                    if self.game.field[int(x)][int(y)][1] == 0:  # red
                                        a = 7
                                    elif self.game.field[int(x)][int(y)][1] == 1:  # green
                                        b = 7
                                    else:  # blue
                                        b = 2
                                        c = 7
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
                                pygame.draw.circle(self.screen, (a * 35, b * 35, c * 35), (x_diamond, y_diamond),
                                                   radius * 1.5)  # circle
                            elif self.game.field[int(x)][int(y)][0] == 1:
                                pygame.draw.rect(self.screen, (0, 0, 0),
                                                 (x_diamond - radius * 1.4 - 1, y_diamond - radius * 1.4 - 1,
                                                  radius * 2.8 + 2, radius * 2.8 + 2))  # black square
                                pygame.draw.rect(self.screen, (a * 35, b * 35, c * 35),
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
                                pygame.draw.polygon(self.screen, (a * 35, b * 35, c * 35),
                                                    [(x1, y1), (x2, y2), (x3, y3)])  # colored triangle

                        else:
                            # black background stick
                            for k in range(10 + 10 * self.game.field[int(x)][int(y)][0]):
                                pygame.draw.circle(self.screen, (0, 0, 0),
                                                   (x_diamond + k * 1 * hight_multiplier,
                                                    y_diamond - k * 2 * hight_multiplier), radius + 1)

                            # sticks with different color and height
                            for k in range(10 + 10 * self.game.field[int(x)][int(y)][0]):
                                load = k / (10 + 10 * self.game.field[int(x)][int(y)][0])
                                if k == 10 + 10 * self.game.field[int(x)][int(y)][0] - 1:
                                    pygame.draw.circle(self.screen, (0, 0, 0),
                                                       (x_diamond + k * 1 * hight_multiplier,
                                                        y_diamond - k * 2 * hight_multiplier), radius + 1)
                                pygame.draw.circle(self.screen, (int(10 * a + load * a * 25),
                                                                 int(10 * b + load * b * 25),
                                                                 int(10 * c + load * c * 25)),
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
        for pdx, player in enumerate(self.game.player):

            text_surface_big = self.font_large.render("Player", True, (150, 150, 150))
            text_rect_big = text_surface_big.get_rect()
            text_rect_height_big = text_rect_big.height + edge / 4
            text_rect_width_big = text_rect_big.width + edge / 4

            text_surface = self.font.render("Player", True, (150, 150, 150))
            text_rect = text_surface.get_rect()
            text_rect_height = text_rect.height + edge / 4
            info_box_height = max(self.field_height / 3, text_rect_height_big + text_rect_height * 4 + edge * 1.75)
            info_box_width = max(width / 2, text_rect_width_big + edge)

            pygame.draw.rect(self.screen, (30, 30, 30),
                             (edge * 0.5 + pdx * (self.window_width - info_box_width - edge),
                              y - info_box_height, info_box_width, info_box_height))

            pygame.draw.rect(self.screen, (30, 30, 30),
                             (x, y, width, height))
            if not self.game.active_player == pdx:
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 (edge * 0.5 + pdx * (self.window_width - info_box_width - edge) + 10,
                                  y - info_box_height + 10, info_box_width - 20, info_box_height - 20))
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 (x + 10, y + 10, width - 20, height - 20))

            num1 = str(self.game.count_points_per_layer(pdx, 0))
            num2 = str(self.game.count_points_per_layer(pdx, 1))
            num3 = str(self.game.count_points_per_layer(pdx, 2))
            num4 = str(self.game.count_points(pdx))
            part4 = "Total: " + num4
            if pdx == 0:
                if self.color_scheme:
                    heading = "Color"
                    part1 = "Olive: " + num1
                    part2 = "Green: " + num2
                    part3 = "Yellow: " + num3
                else:
                    heading = "Color"
                    part1 = "Red: " + num1
                    part2 = "Green: " + num2
                    part3 = "Blue: " + num3
            else:
                if self.symbol:
                    heading = "Symbol"
                    part1 = "Circle: " + num1
                    part2 = "Square: " + num2
                    part3 = "Triangle: " + num3
                else:
                    heading = "Height"
                    part1 = "Small: " + num1
                    part2 = "Medium: " + num2
                    part3 = "Tall: " + num3

            # Heading
            text_surface_big = self.font_large.render(heading, True, (150, 150, 150))
            text_rect_big.center = (edge + pdx * (self.window_width - info_box_width - edge) + text_rect_width_big / 2,
                                    edge * 0.5 + y - info_box_height + text_rect_height_big / 2)
            self.screen.blit(text_surface_big, text_rect_big)

            # Red
            text_surface = self.font.render(part1, True, (150, 150, 150))
            text_rect = text_surface.get_rect()
            text_rect_height = text_rect.height + edge / 2
            text_rect_width = text_rect.width + edge / 2
            text_rect.center = (edge + pdx * (self.window_width - info_box_width - edge) + text_rect_width / 2,
                                edge * 0.5 + y - info_box_height + text_rect_height_big + text_rect_height * 0.5)
            self.screen.blit(text_surface, text_rect)

            # Green
            text_surface = self.font.render(part2, True, (150, 150, 150))
            text_rect = text_surface.get_rect()
            text_rect_width = text_rect.width + edge / 2
            text_rect.center = (edge + pdx * (self.window_width - info_box_width - edge) + text_rect_width / 2,
                                edge * 0.5 + y - info_box_height + text_rect_height_big + text_rect_height * 1.5)
            self.screen.blit(text_surface, text_rect)

            # Blue
            text_surface = self.font.render(part3, True, (150, 150, 150))
            text_rect = text_surface.get_rect()
            text_rect_width = text_rect.width + edge / 2
            text_rect.center = (edge + pdx * (self.window_width - info_box_width - edge) + text_rect_width / 2,
                                edge * 0.5 + y - info_box_height + text_rect_height_big + text_rect_height * 2.5)
            self.screen.blit(text_surface, text_rect)

            # Sum
            text_surface = self.font.render(part4, True, (150, 150, 150))
            text_rect = text_surface.get_rect()
            text_rect_width = text_rect.width + edge / 2
            text_rect.center = (edge + pdx * (self.window_width - info_box_width - edge) + text_rect_width / 2,
                                edge * 0.5 + y - info_box_height + text_rect_height_big + text_rect_height * 3.5)
            self.screen.blit(text_surface, text_rect)

            for idx, i in enumerate(player):
                for jdx, j in enumerate(i):
                    a, b, c = 0, 0, 0
                    for kdx in range(3):
                        if kdx == jdx:
                            if self.color_scheme:
                                if jdx == 0:  # olive (dark green)
                                    b = 2
                                elif jdx == 1:  # green
                                    b = 7
                                else:  # yellow
                                    a = 7
                                    b = 7
                            else:
                                if jdx == 0:  # red
                                    a = 7
                                elif jdx == 1:  # green
                                    b = 7
                                else:  # blue
                                    b = 2
                                    c = 7

                    x_pos = x + (0.5 + idx) * width / 4
                    y_pos = y + (0.5 + jdx) * height / 4
                    if not self.symbol:
                        if self.chosen_color == [pdx, idx, jdx]:
                            pygame.draw.rect(self.screen, (255, 255, 255),
                                             (x_pos - 3, y_pos - 3, width / 6 + 6, height / 4 + 6))
                        pygame.draw.rect(self.screen, (a * 30, b * 30, c * 30),
                                         (x_pos, y_pos, width / 6, height / 4))
                    else:
                        if self.chosen_color == [pdx, idx, jdx]:
                            pygame.draw.rect(self.screen, (255, 255, 255),
                                             (x_pos - 3, y_pos - 3, width / 6 + 6, height / 4 + 6))
                        pygame.draw.rect(self.screen, (a * 15, b * 15, c * 15),
                                         (x_pos, y_pos, width / 6, height / 4))

                    for k in range(3 - j):
                        if k == 0:
                            x_pos = x + (0.7 + idx) * width / 4 + width / 16
                            y_pos = y + (1 + jdx) * height / 4 - height / 16
                        elif k == 1:
                            x_pos = x + (0.7 + idx) * width / 4
                            y_pos = y + (1 + jdx) * height / 4
                        else:
                            x_pos = x + (0.7 + idx) * width / 4 + width / 16
                            y_pos = y + (1 + jdx) * height / 4 + height / 16
                        if self.symbol:
                            if idx == 0:
                                if self.chosen_color == [pdx, idx, jdx]:
                                    pygame.draw.circle(self.screen, (255, 255, 255), (x_pos, y_pos),
                                                       radius * 1.5 + 2)  # white circle
                                else:
                                    pygame.draw.circle(self.screen, (0, 0, 0), (x_pos, y_pos),
                                                       radius * 1.5 + 1)  # black circle
                                pygame.draw.circle(self.screen, (a * 35, b * 35, c * 35), (x_pos, y_pos),
                                                   radius * 1.5)  # circle
                            elif idx == 1:
                                if self.chosen_color == [pdx, idx, jdx]:
                                    pygame.draw.rect(self.screen, (255, 255, 255),
                                                     (x_pos - radius * 1.4 - 2, y_pos - radius * 1.4 - 2,
                                                      radius * 2.8 + 4, radius * 2.8 + 4))  # white square
                                else:
                                    pygame.draw.rect(self.screen, (0, 0, 0),
                                                     (x_pos - radius * 1.4 - 1, y_pos - radius * 1.4 - 1,
                                                      radius * 2.8 + 2, radius * 2.8 + 2))  # black square
                                pygame.draw.rect(self.screen, (a * 35, b * 35, c * 35),
                                                 (x_pos - radius * 1.4, y_pos - radius * 1.4,
                                                  radius * 2.8, radius * 2.8))  # colored square
                            else:
                                height_triangle = math.sqrt(3) * radius * 2

                                # Calculate the coordinates of the three corners
                                x1 = x_pos
                                y1 = y_pos - height_triangle / 2 - radius / 2

                                x2 = x_pos - radius * 2
                                y2 = y_pos + height_triangle / 2 - radius / 2

                                x3 = x_pos + radius * 2
                                y3 = y_pos + height_triangle / 2 - radius / 2
                                if self.chosen_color == [pdx, idx, jdx]:
                                    pygame.draw.polygon(self.screen, (255, 255, 255),
                                                        [(x1, y1 - 4), (x2 - 3, y2 + 2),
                                                         (x3 + 3, y3 + 2)])  # white triangle
                                else:
                                    pygame.draw.polygon(self.screen, (0, 0, 0),
                                                        [(x1, y1 - 2), (x2 - 1.5, y2 + 1),
                                                         (x3 + 1.5, y3 + 1)])  # black triangle
                                pygame.draw.polygon(self.screen, (a * 35, b * 35, c * 35),
                                                    [(x1, y1), (x2, y2), (x3, y3)])  # colored triangle

                        else:
                            # background stick
                            for l in range(10 + 10 * idx):
                                if self.chosen_color == [pdx, idx, jdx]:
                                    pygame.draw.circle(self.screen, (255, 255, 255),
                                                       (x_pos + l * 1 * hight_multiplier,
                                                        y_pos - l * 2 * hight_multiplier), radius + 2)  # white stick
                                else:
                                    pygame.draw.circle(self.screen, (0, 0, 0),
                                                       (x_pos + l * 1 * hight_multiplier,
                                                        y_pos - l * 2 * hight_multiplier), radius + 1)  # black stick

                            # sticks with different color and height
                            for l in range(10 + 10 * idx):
                                load = l / (10 + 10 * idx)
                                if l == 10 + 10 * idx - 1:
                                    if self.chosen_color == [pdx, idx, jdx]:
                                        pygame.draw.circle(self.screen, (255, 255, 255),
                                                           (x_pos + l * 1 * hight_multiplier,
                                                            y_pos - l * 2 * hight_multiplier),
                                                           radius + 2)  # white top circle
                                    else:
                                        pygame.draw.circle(self.screen, (0, 0, 0),
                                                           (x_pos + l * 1 * hight_multiplier,
                                                            y_pos - l * 2 * hight_multiplier),
                                                           radius + 1)  # black top circle
                                pygame.draw.circle(self.screen, (int(10 * a + load * a * 25),
                                                                 int(10 * b + load * b * 25),
                                                                 int(10 * c + load * c * 25)),
                                                   (x_pos + l * 1 * hight_multiplier,
                                                    y_pos - l * 2 * hight_multiplier), radius)

            x = self.window_width - width - edge * 0.5
            y = self.window_height - self.bottom_diff + edge

        # Render the text
        text_surface = self.font.render("Make Move", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect_height = text_rect.height + 10  # Add padding for better visibility
        text_rect_width = text_rect.width + 10  # Add padding for better visibility

        height = min(75, max(text_rect_height, self.bottom_diff / 4))
        width = min(200, max(text_rect_width, self.window_width / 6))

        y = self.window_height - self.bottom_diff / 2 + edge
        x = self.window_width / 2
        if (all(item is not None for item in [self.game.active_start, self.game.active_end, *self.chosen_color])
                or self.game.empty_board and all(
                    item is not None for item in [self.game.active_end, *self.chosen_color])):
            pygame.draw.rect(self.screen, (0, 150, 50), (x - width / 2, y - height * 1.5, width, height))
        else:
            pygame.draw.rect(self.screen, (50, 50, 50), (x - width / 2, y - height * 1.5, width, height))
        # Draw the text
        text_rect.center = (x, y - height)
        self.screen.blit(text_surface, text_rect)

        if self.game.active_start is not None or self.game.active_end is not None or self.chosen_color != [None, None,
                                                                                                           None]:
            text_surface = self.font.render("Cancel", True, (150, 150, 150))
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            self.screen.blit(text_surface, text_rect)

        if self.winner is not None:
            pygame.draw.rect(self.screen, (50, 50, 50), (
                self.window_width / 3, self.window_height / 3, self.window_width / 3, self.window_height / 3))
            if self.color_scheme:
                p0 = "Color"
            else:
                p0 = "Color"
            if self.symbol:
                p1 = "Symbol"
            else:
                p1 = "Height"

            message = ""
            if self.winner == 0:
                message = "Player " + p0 + " has won with " + str(self.game.count_points(0)) + " Points!"
            elif self.winner == 1:
                message = "Player " + p1 + " has won with " + str(self.game.count_points(1)) + " Points!"
            elif self.winner == -1:
                message = "It's a draw with " + self.game.count_points(0) + " Points!"

            text_surface_big = self.font_large.render(message, True, (150, 150, 150))
            text_rect_big = text_surface_big.get_rect()
            text_rect_height_big = max(text_rect_big.height + 100, self.window_height / 3)
            text_rect_width_big = max(text_rect_big.width + 100, self.window_width / 3)

            pygame.draw.rect(self.screen, (50, 50, 50), (
                self.window_width / 2 - text_rect_width_big / 2, self.window_height / 2 - text_rect_height_big / 2,
                text_rect_width_big, text_rect_height_big))

            text_rect_big.center = (self.window_width / 2, self.window_height / 2)
            self.screen.blit(text_surface_big, text_rect_big)

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

                if self.winner is not None:
                    self.game.reset_game()
                    self.winner = None
                    self.draw_board()
                    return
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
                if self.window_width - 115 < mouse_x < self.window_width - 60 and 135 < mouse_y < 165:
                    self.color_scheme = not self.color_scheme

                edge_vertical = self.field_height / 14
                edge_horizontal = self.field_width / 14
                edge = min(edge_vertical, edge_horizontal)
                width = self.window_width / 3
                height = self.bottom_diff - edge * 1.5

                x = edge * 0.5
                y = self.window_height - self.bottom_diff + edge
                for pdx, player in enumerate(self.game.player):
                    for idx, i in enumerate(player):
                        for jdx, j in enumerate(i):
                            x_pos = x + (0.5 + idx) * width / 4
                            y_pos = y + (0.5 + jdx) * height / 4
                            if x_pos < mouse_x < x_pos + width / 6 and y_pos < mouse_y < y_pos + height / 4:
                                if j < 3 and self.game.active_player == pdx:
                                    self.chosen_color = [pdx, idx, jdx]

                    x = self.window_width - width - edge * 0.5
                    y = self.window_height - self.bottom_diff + edge

                # Render the text
                text_surface = self.font.render("Make Move", True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                text_rect_height = text_rect.height + 10  # Add padding for better visibility
                text_rect_width = text_rect.width + 10  # Add padding for better visibility

                height = min(75, max(text_rect_height, self.bottom_diff / 4))
                width = min(200, max(text_rect_width, self.window_width / 6))

                y = self.window_height - self.bottom_diff / 2 + edge
                x = self.window_width / 2
                if x - width / 2 < mouse_x < x + width / 2 and y - height * 1.5 < mouse_y < y - height * 0.5:
                    self.procceed_action()
                if x - width / 2 < mouse_x < x + width / 2 and y - height * 0.5 < mouse_y < y + height * 0.5:
                    self.game.active_start = None
                    self.game.active_end = None
                    self.chosen_color = [None for _ in range(3)]

                self.winner = self.game.winner()
                self.draw_board()

    def procceed_action(self):
        if self.game.empty_board and all(item is not None for item in [self.game.active_end, *self.chosen_color]):
            self.game.make_move(self.game.active_end, None, self.chosen_color[1:])
            self.game.active_end = None
            self.chosen_color = [None for _ in range(3)]

        if all(item is not None for item in [self.game.active_start, self.game.active_end, *self.chosen_color]):
            self.game.make_move(self.game.active_start, self.game.active_end, self.chosen_color[1:])
            self.game.active_start = None
            self.game.active_end = None
            self.chosen_color = [None for _ in range(3)]

    def action(self, position):
        if self.game.active_start and self.active_positions[position[0]][position[1]]:
            self.game.active_end = position
        elif self.game.field[position[0]][position[1]] is None and self.game.empty_board:
            self.game.active_end = position
        if self.game.field[position[0]][position[1]]:
            self.game.active_end = None
            self.game.active_start = position

    def run_game(self):
        self.draw_board()
        while self.running:
            self.handle_event()


if __name__ == "__main__":
    game = WaldmeisterGame()
    gui = PygameWaldmeisterGUI(game)
    gui.run_game()
