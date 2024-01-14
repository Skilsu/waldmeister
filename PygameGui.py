import copy
import logging
import math
import threading

import pygame
from Waldmeister.WaldmeisterGame import WaldmeisterGame
from Waldmeister.WaldmeisterLogic import WaldmeisterLogic
from Waldmeister.WaldmeisterPlayers import AiWaldmeisterPlayer

log = logging.getLogger(__name__)

MODELS = [[["Easy", "best_nico_5.h5"], ["Difficult", "best_abdul_5.h5"]],
          [],
          [],
          [["Easy", "checkpoint_4_abdul_8.h5"], ["Difficult", "best_abdul_8.h5"]]]


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
        self.game_ai = WaldmeisterGame(self.game.board_size, self.game.color_amount)
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption('Waldmeister')
        pygame.font.init()
        self.font_size = 28
        self.font = pygame.font.Font(None, self.font_size)
        self.font_size = 40
        self.font_large = pygame.font.Font(None, self.font_size)

        self.active_positions = [[0 for _ in range(self.game.board_size)] for _ in range(self.game.board_size)]
        self.active_start = None
        self.active_end = None

        self.symbol = False
        self.color_scheme = True
        self.ai = False
        self.no_ai = False
        self.ai_types, self.ai_lambdas = self.generate_ai()
        self.chosen_ai_type = 0
        self.running = True
        self.ai_v_ai = False
        self.chosen_ai_type_2 = 0
        self.mirror = True
        self.moving = False
        self.auto_play = False

        self.chosen_color = [None for _ in range(3)]
        self.winner = 0
        self.active_player = -1  # can be -1 or 1 to access over self.player

    def generate_ai(self):
        ai_types = []
        ai_lambdas = []

        if not (self.game.board_size > len(MODELS) + 4):
            for model in MODELS[self.game.board_size - 5]:
                ai_types.append(model[0])
                ai_lambdas.append(AiWaldmeisterPlayer(self.game_ai, model[1]).play)
        if not ai_lambdas:
            self.no_ai = True
        ai_types.append("Alpha Beta")
        return ai_types, ai_lambdas

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

    def _toggle(self, x, y, names, value):
        size = len(names) - 1
        pygame.draw.line(self.screen, (255, 255, 255),
                         (x - 100 + size * 25, y + 49),
                         (x - 100, y + 49),
                         20)
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (x - 100 + size * 25, y + 50), 10)
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (x - 100, y + 50), 10)

        pygame.draw.line(self.screen, (0, 0, 0),
                         (x - 100 + size * 25, y + 49),
                         (x - 100, y + 49),
                         18)
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (x - 100 + size * 25, y + 50), 9)
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (x - 100, y + 50), 9)

        text_surface = self.font.render(names[int(value)], True, (255, 255, 255))
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (x - 100 + int(value) * 25, y + 50), 15)

        text_rect = text_surface.get_rect()
        text_rect.center = (x - 100 + size * 12, y + 90)
        self.screen.blit(text_surface, text_rect)

    def symbol_toggle(self):
        self._toggle(self.window_width, 0, ["Sticks", "Symbols"], not self.symbol)  # not bc aesthetics

    def color_toggle(self):
        self._toggle(self.window_width, 100, ["Default", "Colored"], self.color_scheme)

    def ai_toggle(self):
        self._toggle(175, 0, ["Human", "Ai"], self.ai)

    def ai_strength_toggle(self):
        self._toggle(250, 0, self.ai_types, self.chosen_ai_type)

    def ai_v_ai_toggle(self):
        self._toggle(175, 100, ["vs. Human", "vs. Ai"], self.ai_v_ai)

    def ai_type_toggle(self):
        self._toggle(250, 100, self.ai_types, self.chosen_ai_type_2)

    def mirror_toggle(self):
        self._toggle(400, 0, ["Left", "Right"], self.mirror)

    def auto_toggle(self):
        self._toggle(525, 0, ["Klick", "Auto"], self.auto_play)

    def draw_symbol(self, symbol, x_diamond, y_diamond, radius, height_multiplier, chosen_color):
        a, b, c = 0, 0, 0
        for kdx in range(3):
            if kdx == symbol[1]:
                if self.color_scheme:
                    if symbol[1] == 0:  # olive (dark green)
                        b = 2
                    elif symbol[1] == 1:  # green
                        b = 7
                    else:  # yellow
                        a = 7
                        b = 7
                else:
                    if symbol[1] == 0:  # red
                        a = 7
                    elif symbol[1] == 1:  # green
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
            if symbol[0] == 0:
                if chosen_color:
                    pygame.draw.circle(self.screen, (255, 255, 255), (x_diamond, y_diamond),
                                       radius * 1.5 + 2)  # white circle
                else:
                    pygame.draw.circle(self.screen, (0, 0, 0), (x_diamond, y_diamond),
                                       radius * 1.5 + 1)  # black circle
                pygame.draw.circle(self.screen, (a * 35, b * 35, c * 35), (x_diamond, y_diamond),
                                   radius * 1.5)  # circle
            elif symbol[0] == 1:
                if chosen_color:
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     (x_diamond - radius * 1.4 - 2, y_diamond - radius * 1.4 - 2,
                                      radius * 2.8 + 4, radius * 2.8 + 4))  # white square
                else:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (x_diamond - radius * 1.4 - 1, y_diamond - radius * 1.4 - 1,
                                      radius * 2.8 + 2, radius * 2.8 + 2))  # black square
                pygame.draw.rect(self.screen, (a * 35, b * 35, c * 35),
                                 (x_diamond - radius * 1.4, y_diamond - radius * 1.4,
                                  radius * 2.8, radius * 2.8))  # colored square
            else:
                height_triangle = math.sqrt(3) * radius * 2

                # Calculate the coordinates of the three corners
                x1 = x_diamond
                y1 = y_diamond - height_triangle / 2 - radius / 2

                x2 = x_diamond - radius * 2
                y2 = y_diamond + height_triangle / 2 - radius / 2

                x3 = x_diamond + radius * 2
                y3 = y_diamond + height_triangle / 2 - radius / 2
                if chosen_color:
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
            for l in range(10 + 10 * symbol[0]):
                if chosen_color:
                    pygame.draw.circle(self.screen, (255, 255, 255),
                                       (x_diamond + l * 1 * height_multiplier,
                                        y_diamond - l * 2 * height_multiplier), radius + 2)  # white stick
                else:
                    pygame.draw.circle(self.screen, (0, 0, 0),
                                       (x_diamond + l * 1 * height_multiplier,
                                        y_diamond - l * 2 * height_multiplier), radius + 1)  # black stick

            # sticks with different color and height
            for l in range(10 + 10 * symbol[0]):
                load = l / (10 + 10 * symbol[0])
                if l == 10 + 10 * symbol[0] - 1:
                    if chosen_color:
                        pygame.draw.circle(self.screen, (255, 255, 255),
                                           (x_diamond + l * 1 * height_multiplier,
                                            y_diamond - l * 2 * height_multiplier),
                                           radius + 2)  # white top circle
                    else:
                        pygame.draw.circle(self.screen, (0, 0, 0),
                                           (x_diamond + l * 1 * height_multiplier,
                                            y_diamond - l * 2 * height_multiplier),
                                           radius + 1)  # black top circle
                pygame.draw.circle(self.screen, (int(10 * a + load * a * 25),
                                                 int(10 * b + load * b * 25),
                                                 int(10 * c + load * c * 25)),
                                   (x_diamond + l * 1 * height_multiplier,
                                    y_diamond - l * 2 * height_multiplier), radius)

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        self.symbol_toggle()
        self.color_toggle()
        self.ai_toggle()
        if self.ai:
            self.ai_strength_toggle()
            self.mirror_toggle()
            self.auto_toggle()
            self.ai_v_ai_toggle()
            if self.ai_v_ai:
                self.ai_type_toggle()

        edge_vertical = self.field_height / (self.game.board_size * 2 - 2)
        edge_horizontal = self.field_width / (self.game.board_size * 2 - 2)
        pygame.draw.polygon(self.screen, (125, 75, 0),
                            [(self.start_diff + self.field_width / 2, self.top_diff - edge_vertical),
                             (self.start_diff - edge_horizontal, self.top_diff + self.field_height / 2),
                             (
                                 self.start_diff + self.field_width / 2,
                                 self.top_diff + self.field_height + edge_vertical),
                             (self.start_diff + self.field_width + edge_horizontal,
                              self.top_diff + self.field_height / 2)])

        if self.winner != 0:
            pygame.draw.rect(self.screen, (50, 50, 50), (
                self.window_width / 3, 0, self.window_width / 3, self.top_diff))
            ai = ""
            if self.ai:
                ai = "Ai: "
            if self.color_scheme:
                p0 = "Color"
            else:
                p0 = "Color"
            if self.symbol:
                p1 = "Symbol"
            else:
                p1 = "Height"
            if self.mirror:
                p1 = ai + p1
            else:
                p0 = ai + p0
            message = ""
            if self.winner == -1:
                message = "Player " + p0 + " has won with " + str(self.game.count_points(0)) + " Points!"
            elif self.winner == 1:
                message = "Player " + p1 + " has won with " + str(self.game.count_points(1)) + " Points!"
            elif self.winner != 0:
                message = "It's a draw with " + str(self.game.count_points(0)) + " Points!"

            text_surface_big = self.font_large.render(message, True, (255, 255, 255))
            text_rect_big = text_surface_big.get_rect()
            text_rect_height_big = text_rect_big.height + 100
            text_rect_width_big = max(text_rect_big.width + 100, self.window_width / 3)

            pygame.draw.rect(self.screen, (50, 50, 50), (
                self.window_width / 2 - text_rect_width_big / 2, 0,
                text_rect_width_big, text_rect_height_big))

            text_rect_big.center = (self.window_width / 2, self.top_diff / 2)
            self.screen.blit(text_surface_big, text_rect_big)

        if self.active_start:
            self.active_positions = self.game.get_active_positions(self.active_start)

        # draw lines and dots
        x = -(self.game.board_size / 2)
        y = (self.game.board_size / 2) - 1
        for i in range(self.game.board_size * 2 - 1):
            old_x = x
            old_y = y
            for j in range(self.game.board_size * 2 - 1):
                x += 0.5
                y += 0.5
                if 0 <= x < self.game.board_size and 0 <= y < self.game.board_size and y == int(y) and x == int(x):
                    x_diamond = (j * self.field_width / (self.game.board_size * 2 - 2) + self.start_diff)
                    y_diamond = (i * self.field_height / (self.game.board_size * 2 - 2) + self.top_diff)
                    radius = int((self.field_width + self.field_height) / 110)
                    height_multiplier = radius / 12

                    # draw lines
                    if y > 0 and x < self.game.board_size - 1:
                        pygame.draw.line(self.screen, (0, 0, 0),
                                         (x_diamond, y_diamond),
                                         (x_diamond, y_diamond + (self.field_height / self.game.board_size - 1)),
                                         radius + 2)
                        if self.active_start and self.active_positions[int(x)][int(y)] == 1 and \
                                self.active_positions[int(x + 1)][
                                    int(y - 1)] == 1 and self.active_start[1] + self.active_start[0] == int(x) + int(y):
                            pygame.draw.line(self.screen, (25, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond, y_diamond + (self.field_height / self.game.board_size - 1)),
                                             radius)
                        else:
                            pygame.draw.line(self.screen, (150, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond, y_diamond + (self.field_height / self.game.board_size - 1)),
                                             radius)
                    # diagonal forward
                    if x < self.game.board_size - 1:
                        pygame.draw.line(self.screen, (0, 0, 0),
                                         (x_diamond, y_diamond),
                                         (x_diamond + self.field_width / (self.game.board_size * 2 - 2),
                                          y_diamond + (self.field_height / (self.game.board_size * 2 - 2))),
                                         radius + 2)
                        if self.active_start and self.active_positions[int(x)][int(y)] == 1 and \
                                self.active_positions[int(x + 1)][
                                    int(y)] == 1 and self.active_start[1] == int(y):
                            pygame.draw.line(self.screen, (25, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond + self.field_width / (self.game.board_size * 2 - 2),
                                              y_diamond + (self.field_height / (self.game.board_size * 2 - 2))),
                                             radius)
                        else:
                            pygame.draw.line(self.screen, (150, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond + self.field_width / (self.game.board_size * 2 - 2),
                                              y_diamond + (self.field_height / (self.game.board_size * 2 - 2))),
                                             radius)
                    # diagonal backwards
                    if y > 0:
                        pygame.draw.line(self.screen, (0, 0, 0),
                                         (x_diamond, y_diamond),
                                         (x_diamond - self.field_width / (self.game.board_size * 2 - 2),
                                          y_diamond + (self.field_height / (self.game.board_size * 2 - 2))),
                                         radius + 2)
                        if self.active_start and self.active_positions[int(x)][int(y)] == 1 and \
                                self.active_positions[int(x)][
                                    int(y - 1)] == 1 and self.active_start[0] == int(x):
                            pygame.draw.line(self.screen, (25, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond - self.field_width / (self.game.board_size * 2 - 2),
                                              y_diamond + (self.field_height / (self.game.board_size * 2 - 2))),
                                             radius)
                        else:
                            pygame.draw.line(self.screen, (150, 150, 50),
                                             (x_diamond, y_diamond),
                                             (x_diamond - self.field_width / (self.game.board_size * 2 - 2),
                                              y_diamond + (self.field_height / (self.game.board_size * 2 - 2))),
                                             radius)
                    # empty holes
                    pygame.draw.circle(self.screen, (0, 0, 0),
                                       (x_diamond, y_diamond), radius + 1)
                    if self.active_end and x == self.active_end[0] and y == self.active_end[1]:
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

                    if self.game.field[int(x)][int(y)] is not None:
                        self.draw_symbol(self.game.field[int(x)][int(y)], x_diamond, y_diamond, radius,
                                         height_multiplier, False)
            x = old_x + 0.5
            y = old_y - 0.5

        edge = min(edge_vertical, edge_horizontal)
        width = self.window_width / 3
        height = self.bottom_diff - edge * 1.5
        radius = int((self.field_width + self.field_height) / 110)
        height_multiplier = radius / 12

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
            if not self.active_player == pdx and not (self.active_player == -1 and pdx == 0):
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
            ai = ""
            if self.ai:
                ai = "Ai: "
            if pdx == 0:
                if self.mirror and not self.ai_v_ai:
                    ai = ""
                if self.color_scheme:
                    heading = ai + "Color"
                    part1 = "Olive: " + num1
                    part2 = "Green: " + num2
                    part3 = "Yellow: " + num3
                else:
                    heading = ai + "Color"
                    part1 = "Red: " + num1
                    part2 = "Green: " + num2
                    part3 = "Blue: " + num3
            else:
                if not self.mirror and not self.ai_v_ai:
                    ai = ""
                if self.symbol:
                    heading = ai + "Symbol"
                    part1 = "Circle: " + num1
                    part2 = "Square: " + num2
                    part3 = "Triangle: " + num3
                else:
                    heading = ai + "Height"
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

                    # rect behind symbols/sticks
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

                    # adjusting pos of current stick/symbol
                    for k in range(self.game.color_amount - j):
                        if k == 0:
                            x_pos = x + (0.7 + idx) * width / 4 + width / 16
                            y_pos = y + (1 + jdx) * height / 4 - height / 16
                        elif k == 1:
                            x_pos = x + (0.7 + idx) * width / 4
                            y_pos = y + (1 + jdx) * height / 4
                        else:
                            x_pos = x + (0.7 + idx) * width / 4 + width / 16
                            y_pos = y + (1 + jdx) * height / 4 + height / 16

                        chosen_color = bool(self.chosen_color == [pdx, idx, jdx])
                        self.draw_symbol([idx, jdx], x_pos, y_pos, radius, height_multiplier, chosen_color)

            x = self.window_width - width - edge * 0.5
            y = self.window_height - self.bottom_diff + edge

        # Render the text
        button_text = "Make Move"
        text_surface = self.font.render(button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect_height = text_rect.height + 10  # Add padding for better visibility
        text_rect_width = text_rect.width + 10  # Add padding for better visibility

        height = min(75, max(text_rect_height, self.bottom_diff / 4))
        width = min(200, max(text_rect_width, self.window_width / 6))

        y = self.window_height - self.bottom_diff / 2 + edge
        x = self.window_width / 2
        if ((all(item is not None for item in [self.active_start, self.active_end, *self.chosen_color])
             or self.game.empty_board()
             and all(item is not None for item in [self.active_end, *self.chosen_color])) or not self.moving and
                (self.ai and
                 (self.ai_v_ai or
                  (self.mirror and self.active_player == 1 or not self.mirror and self.active_player == -1)))):
            if self.ai and self.ai_v_ai and self.auto_play:
                button_text = "Play"
            pygame.draw.rect(self.screen, (0, 150, 50), (x - width / 2, y - height * 1.5, width, height))
        else:
            if self.ai and self.ai_v_ai and self.auto_play:
                button_text = "Running..."
            pygame.draw.rect(self.screen, (50, 50, 50), (x - width / 2, y - height * 1.5, width, height))
        # Draw the text
        text_surface = self.font.render(button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y - height)
        self.screen.blit(text_surface, text_rect)

        if self.active_start is not None or self.active_end is not None or self.chosen_color != [None, None, None]:
            text_surface = self.font.render("Cancel", True, (150, 150, 150))
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            self.screen.blit(text_surface, text_rect)

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

                if self.winner != 0:
                    self.game.__init__(self.game.board_size, self.game.color_amount)
                    self.winner = 0
                    self.draw_board()
                    return
                # Check if the mouse click is inside any of the circles on the board
                x = -(self.game.board_size / 2)
                y = (self.game.board_size / 2) - 1

                # handle toggles
                if self.window_width - 115 < mouse_x < self.window_width - 60 and 35 < mouse_y < 65:
                    self.symbol = not self.symbol
                if self.window_width - 115 < mouse_x < self.window_width - 60 and 135 < mouse_y < 165:
                    self.color_scheme = not self.color_scheme
                if 60 < mouse_x < 115 and 35 < mouse_y < 65 and not self.no_ai:
                    self.ai = not self.ai
                if self.ai:
                    if 125 < mouse_x < 235 and 35 < mouse_y < 65:
                        if self.chosen_ai_type < len(self.ai_types) - 1:
                            self.chosen_ai_type += 1
                        else:
                            self.chosen_ai_type = 0
                    if 60 < mouse_x < 115 and 135 < mouse_y < 165:
                        self.ai_v_ai = not self.ai_v_ai
                    if self.ai_v_ai and 125 < mouse_x < 235 and 135 < mouse_y < 165:
                        if self.chosen_ai_type_2 < len(self.ai_types) - 1:
                            self.chosen_ai_type_2 += 1
                        else:
                            self.chosen_ai_type_2 = 0
                    if 280 < mouse_x < 340 and 35 < mouse_y < 65:
                        self.mirror = not self.mirror
                    if 405 < mouse_x < 465 and 35 < mouse_y < 65:
                        self.auto_play = not self.auto_play

                edge_vertical = self.field_height / (self.game.board_size * 2 - 2)
                edge_horizontal = self.field_width / (self.game.board_size * 2 - 2)
                edge = min(edge_vertical, edge_horizontal)
                if not self.moving:
                    if (not (self.ai and
                             (self.ai_v_ai or
                              (self.mirror and self.active_player == 1
                               or not self.mirror and self.active_player == -1)))):
                        for i in range(self.game.board_size * 2 - 1):
                            old_x = x
                            old_y = y
                            for j in range(self.game.board_size * 2 - 1):
                                x += 0.5
                                y += 0.5
                                if 0 <= x < self.game.board_size and 0 <= y < self.game.board_size and y == int(
                                        y) and x == int(x):
                                    x_diamond = (
                                            j * self.field_width / (self.game.board_size * 2 - 2) + self.start_diff)
                                    y_diamond = (i * self.field_height / (self.game.board_size * 2 - 2) + self.top_diff)
                                    radius = int((self.field_width + self.field_height) / 110)

                                    # Check if the mouse click is inside the current circle
                                    if (
                                            (mouse_x - x_diamond) ** 2 + (mouse_y - y_diamond) ** 2
                                    ) ** 0.5 <= radius + 5:
                                        self.action([int(x), int(y)])
                            x = old_x + 0.5
                            y = old_y - 0.5

                        # get figure choices

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
                                        if j < self.game.color_amount and self.active_player == pdx or (
                                                self.active_player == -1 and pdx == 0):
                                            self.chosen_color = [pdx, idx, jdx]

                            x = self.window_width - width - edge * 0.5
                            y = self.window_height - self.bottom_diff + edge

                    # Get Button pressed
                    text_surface = self.font.render("Make Move", True, (255, 255, 255))
                    text_rect = text_surface.get_rect()
                    text_rect_height = text_rect.height + 10  # Add padding for better visibility
                    text_rect_width = text_rect.width + 10  # Add padding for better visibility

                    height = min(75, max(text_rect_height, self.bottom_diff / 4))
                    width = min(200, max(text_rect_width, self.window_width / 6))

                    y = self.window_height - self.bottom_diff / 2 + edge
                    x = self.window_width / 2
                    if x - width / 2 < mouse_x < x + width / 2 and y - height * 1.5 < mouse_y < y - height * 0.5:
                        self.proceed_action()
                    if x - width / 2 < mouse_x < x + width / 2 and y - height * 0.5 < mouse_y < y + height * 0.5:
                        self.game.active_start = None
                        self.active_end = None
                        self.chosen_color = [None for _ in range(3)]

                self.winner = self.game.winner()
                self.draw_board()

    def proceed_action(self):
        if (self.ai and
                (self.ai_v_ai or
                 (self.mirror and self.active_player == 1 or not self.mirror and self.active_player == -1))):
            self.moving = True
            self.draw_board()
            self.proceed_ai_action()
            self.moving = False
            self.active_player = -self.active_player
            if self.auto_play and self.winner == 0:
                self.draw_board()
                self.handle_event()
                self.winner = self.game.winner()
                if self.winner == 0:
                    self.proceed_action()
        else:
            if self.game.empty_board() and all(item is not None for item in [self.active_end, *self.chosen_color]):
                self.game.make_move(starting_from=self.active_end,
                                    figure=self.chosen_color[1:],
                                    player=self.active_player)
                self.active_player = -self.active_player
                self.active_end = None
                self.chosen_color = [None for _ in range(3)]

            if all(item is not None for item in [self.active_start, self.active_end, *self.chosen_color]):
                self.game.make_move(starting_from=self.active_start,
                                    moving_to=self.active_end,
                                    figure=self.chosen_color[1:],
                                    player=self.active_player)
                self.active_player = -self.active_player
                self.active_start = None
                self.active_end = None
                self.chosen_color = [None for _ in range(3)]
            if self.ai and self.auto_play and self.winner == 0:
                self.draw_board()
                self.handle_event()
                self.winner = self.game.winner()
                self.active_player = -self.active_player
                if self.winner == 0:
                    self.proceed_action()

    def proceed_ai_action(self):
        if not self.ai_v_ai:
            chosen_ai = self.chosen_ai_type
        else:
            if self.mirror and self.active_player == 1 or not self.mirror and self.active_player == -1:
                chosen_ai = self.chosen_ai_type
            else:
                chosen_ai = self.chosen_ai_type_2

        board = self.game_ai.return_np_format(self.game.field, self.game.player)
        moving_to = None
        moving = None
        if chosen_ai == len(self.ai_types) - 1:
            starting_from, figure, moving_to = self.alpha_beta()
        else:
            action = self.ai_lambdas[chosen_ai](self.game_ai.getCanonicalForm(board, self.active_player))

            valids = self.game_ai.getValidMoves(self.game_ai.getCanonicalForm(board, self.active_player), 1)

            if valids[action] == 0:
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0

            starting_from, figure, moving = self.game_ai.get_move_from_action(action, self.active_player)
        self.game.make_move(starting_from=starting_from,
                            figure=figure,
                            moving=moving,
                            player=self.active_player,
                            moving_to=moving_to)

    def alpha_beta(self):
        player = self.active_player
        if player == -1:
            player = 0
        if self.game.empty_board():
            actions = []
            values = []
            for idx, row in enumerate(self.game.field):
                for jdx, position in enumerate(row):
                    for kdx, color_list in enumerate(self.game.player[player]):
                        for ldx, figure_pos in enumerate(color_list):
                            if figure_pos < self.game.color_amount:
                                copied_player = copy.deepcopy(self.game.player)
                                copied_player[player][kdx][ldx] += 1
                                copied_field = copy.deepcopy(self.game.field)
                                copied_field[idx][jdx] = [kdx, ldx]
                                values.append([[idx, jdx], [kdx, ldx], None])
                                actions.append(self.calculate_position([copied_player, copied_field],
                                                                       -self.active_player, 1))
            max_val = max(actions)
            max_index = actions.index(max_val)
        else:
            actions = []
            values = []
            for idx, row in enumerate(self.game.field):
                for jdx, position in enumerate(row):
                    if position is not None:
                        for kdx, color_list in enumerate(self.game.player[player]):
                            for ldx, figure_pos in enumerate(color_list):
                                if figure_pos < self.game.color_amount:
                                    for mdx, m in enumerate(self.game.get_active_positions([idx, jdx])):
                                        for ndx, n in enumerate(m):
                                            if n == 1 and not (mdx == idx and ndx == jdx):
                                                copied_player = copy.deepcopy(self.game.player)
                                                copied_player[player][kdx][ldx] += 1
                                                copied_field = copy.deepcopy(self.game.field)
                                                copied_field[mdx][ndx] = copied_field[idx][jdx]
                                                copied_field[idx][jdx] = [kdx, ldx]
                                                values.append([[idx, jdx], [kdx, ldx], [mdx, ndx]])
                                                actions.append(self.calculate_position([copied_player, copied_field],
                                                                                       -self.active_player, 1))
            max_val = max(actions)
            max_index = actions.index(max_val)
        return values[max_index][0], values[max_index][1], values[max_index][2]

    def calculate_position(self, board, active_player, iteration=3):
        copied_player = copy.deepcopy(board[0])
        copied_field = copy.deepcopy(board[1])
        player = active_player
        if player == -1:
            player = 0
        actions = []
        left_moves = False
        for p in copied_player:
            for i in p:
                for j in i:
                    if j < self.game.color_amount:
                        left_moves = True
        if iteration > 0 and left_moves:
            for idx, row in enumerate(copied_field):
                for jdx, position in enumerate(row):
                    if position is not None:
                        for kdx, color_list in enumerate(copied_player[player]):
                            for ldx, figure_pos in enumerate(color_list):
                                if figure_pos < self.game.color_amount:
                                    for mdx, m in enumerate(self.game.get_active_positions([idx, jdx])):
                                        for ndx, n in enumerate(m):
                                            if n == 1 and not mdx == idx and not ndx == jdx:
                                                new_copied_player = copy.deepcopy(copied_player)
                                                new_copied_player[player][kdx][ldx] += 1
                                                new_copied_field = copy.deepcopy(copied_field)
                                                new_copied_field[mdx][ndx] = new_copied_field[idx][jdx]
                                                new_copied_field[idx][jdx] = [kdx, ldx]
                                                actions.append(self.calculate_position([new_copied_player, new_copied_field],
                                                                                       -active_player, (iteration - 1)))
            if active_player == -1:
                max_val = min(actions)
            else:
                max_val = max(actions)
        else:
            game = WaldmeisterLogic(self.game.board_size, self.game.color_amount)
            game.field = copied_field
            max_val = game.count_points(1) - game.count_points(-1)
        return max_val

    def action(self, position):
        if self.active_start and self.active_positions[position[0]][position[1]]:
            self.active_end = position
        elif self.game.field[position[0]][position[1]] is None and self.game.empty_board():
            self.active_end = position
        if self.game.field[position[0]][position[1]]:
            self.active_end = None
            self.active_start = position

    def run_game(self):
        self.draw_board()
        while self.running:
            self.handle_event()


if __name__ == "__main__":
    game = WaldmeisterLogic(board_size=5)
    gui = PygameWaldmeisterGUI(game=game)
    gui.run_game()
