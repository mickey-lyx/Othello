
""" 游戏界面 """

import pygame
import sys
from pygame.locals import *
import time
from config import BLACK, WHITE, EMPTY, DEFAULT_LEVEL, HUMAN, COMPUTER, AI, COMBINATION
import os
import pygame_menu

class Gui:
    def __init__(self):
        """ 初始化类的属性 """
        pygame.init()#检查并初始化pygame包导入的模块
        # 定义需要用到的颜色
        self.BLACK = (0, 0, 0)
        self.BACKGROUND = (128, 64, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (128, 128, 0)

        # 定义需要用到的图形大小
        self.SCREEN_SIZE = (640, 480)
        self.BOARD_POS = (100, 20)
        self.BOARD = (120, 40)
        self.BOARD_SIZE = 400
        self.SQUARE_SIZE = 50
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)#设置游戏主窗口大小

        # 创建文本对象
        self.BLACK_LAB_POS = (5, self.SCREEN_SIZE[1] / 4)
        self.WHITE_LAB_POS = (560, self.SCREEN_SIZE[1] / 4)
        self.font = pygame.font.SysFont("Times New Roman", 22)#新罗马字体
        self.scoreFont = pygame.font.SysFont("Times New Roman", 58)

        # 载入需要用到的棋子、棋盘图片
        self.board_img = pygame.image.load(os.path.join("res", "board.bmp")).convert()  #棋盘
        self.black_img = pygame.image.load(os.path.join("res", "preta.bmp")).convert()  #黑子
        self.white_img = pygame.image.load(os.path.join("res", "branca.bmp")).convert() #白子
        self.tip_img = pygame.image.load(os.path.join("res", "tip.bmp")).convert()       #可行落子格
        self.clear_img = pygame.image.load(os.path.join("res", "nada.bmp")).convert()    #空白格
        # self.black_tip_img = pygame.image.load(os.path.join("res", "preta_tip.bmp")).convert()  # 黑子上一落子记录
        # self.white_tip_img = pygame.image.load(os.path.join("res", "branca_tip.bmp")).convert()  # 白子上一落子记录

    def show_menu(self, start_cb):
        """ 游戏初始界面，完成选边和选择对手 """
        pygame.display.set_caption('Othello by Liu & Ma')
        self.level = DEFAULT_LEVEL
        self.player1 = HUMAN
        self.player2 = COMPUTER
        # pygame-menu完成游戏初始界面
        self.menu = pygame_menu.Menu(480, 640, 'Othello',theme=pygame_menu.themes.THEME_SOLARIZED)   #游戏名设置
        self.menu.add_button('Start', lambda: start_cb(self.player1, self.player2, self.level))  #设置开始游戏按钮
        self.menu.add_selector('AI-Minimax Difficulty: ', [['Medium', 2], ['Easy', 1], ('Hard', 3)],
                                onchange=self.set_difficulty)                                     #难度选项
        self.menu.add_selector('First player(Black)', [[HUMAN, 1], [COMPUTER, 2],[AI, 3], [COMBINATION, 4]],
                               onchange=self.set_player_1)                                       #玩家1选项
        self.menu.add_selector('Second player(White)', [[COMPUTER, 2], [HUMAN, 1],[AI, 3], [COMBINATION, 4]],
                               onchange=self.set_player_2)                                       #玩家2选项
        self.menu.add_button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(self.screen)

    def show_end(self, player_color, score1, score2):
        """ 结算页面，用于显示最终对局信息 """
        pygame.display.set_caption('Othello by Liu & Ma')
        self.menu2 = pygame_menu.Menu(480, 640, 'Othello', theme=pygame_menu.themes.THEME_SOLARIZED)  # 游戏名设置
        Black_name = [f'Black Pieces: {score1}']
        White_name = [f'White Pieces: {score2}']
        # 展示获胜者
        if player_color == WHITE:
            self.menu2.add_label("White player wins!", align=pygame_menu.locals.ALIGN_CENTER, font_size=50, font_width=5, font_color=self.WHITE)
        elif player_color == BLACK:
            self.menu2.add_label("Black player wins!", align=pygame_menu.locals.ALIGN_CENTER, font_size=50, font_width=5, font_color=self.BLACK)
        else:
            self.menu2.add_label("Tie !", align=pygame_menu.locals.ALIGN_CENTER, font_size=50, font_width=5, font_color=self.BLUE)
        # 显示双方最终棋子数量
        for m in Black_name:
            self.menu2.add_label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=30, font_color=self.BLACK)
        for n in White_name:
            self.menu2.add_label(n, align=pygame_menu.locals.ALIGN_CENTER, font_size=30, font_color=self.WHITE)
        self.menu2.add_button('Restart', self.reset_menu2)      # 设置再来一局按钮
        self.menu2.add_button('Quit', pygame_menu.events.EXIT)  # 设置退出游戏按钮
        self.menu2.mainloop(self.screen)

    def set_player_1(self, value, player):
        self.player1 = [0, HUMAN, COMPUTER, AI, COMBINATION][player]

    def set_player_2(self, value, player):
        self.player2 = [0, HUMAN, COMPUTER, AI, COMBINATION][player]

    def reset_menu(self):
        self.menu.disable()
        self.menu.reset(1)

    def reset_menu2(self):
        self.menu2.disable()
        self.menu2.reset(1)

    def set_difficulty(self, value, difficulty):
        self.level = difficulty

    def show_game(self):
        """ 游戏画面 """
        self.reset_menu()                                                           #清除开始菜单
        # 绘制初始游戏画面
        pygame.display.set_caption('Othello by Liu & Ma')
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(self.BACKGROUND)                                       #设置背景
        self.score_size = 50
        self.score1 = pygame.Surface((self.score_size, self.score_size))
        self.score2 = pygame.Surface((self.score_size, self.score_size))            #得分面板
        self.screen.blit(self.background, (0, 0), self.background.get_rect())
        self.screen.blit(self.board_img, self.BOARD_POS, self.board_img.get_rect()) #棋盘对象粘贴至主窗口
        self.put_stone((3, 3), WHITE)
        self.put_stone((4, 4), WHITE)
        self.put_stone((3, 4), BLACK)
        self.put_stone((4, 3), BLACK)                                               #设置初始四颗棋子
        pygame.display.flip()

    def put_stone(self, pos, color):
        """ 根据坐标和颜色放置棋子位置 """
        if pos == None:
            return
        # 翻转方向，适配屏幕的xy轴设置
        pos = (pos[1], pos[0])
        if color == BLACK:
            img = self.black_img
        elif color == WHITE:
            img = self.white_img
        elif color == 'tip':
            img = self.tip_img
        else:
            img = self.clear_img
        x = pos[0] * self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1] * self.SQUARE_SIZE + self.BOARD[1]
        self.screen.blit(img, (x, y), img.get_rect())       #计算落子位置并用相应的图片覆盖
        pygame.display.flip()


    def clear_square(self, pos):
        """ 在一个位置上覆盖一个图片，达到类似清理替换的作用 """
        # 翻转方向
        pos = (pos[1], pos[0])
        x = pos[0] * self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1] * self.SQUARE_SIZE + self.BOARD[1]
        self.screen.blit(self.clear_img, (x, y), self.clear_img.get_rect())
        pygame.display.flip()

    def get_mouse_input(self):
        """ 获取鼠标点击位置 """
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos() #获取鼠标点击的事件
                    # 点击在棋盘外则忽略
                    if mouse_x > self.BOARD_SIZE + self.BOARD[0] or \
                       mouse_x < self.BOARD[0] or \
                       mouse_y > self.BOARD_SIZE + self.BOARD[1] or \
                       mouse_y < self.BOARD[1]:
                        continue
                    # 获取鼠标点击坐标
                    position = ((mouse_x - self.BOARD[0]) // self.SQUARE_SIZE), \
                               ((mouse_y - self.BOARD[1]) // self.SQUARE_SIZE)
                    # 翻转坐标
                    position = (position[1], position[0])
                    return position
                elif event.type == QUIT:
                    sys.exit(0)
            time.sleep(.05)

    def update(self, board, blacks, whites, current_player_color):
        """ 更新屏幕界面 """
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    self.put_stone((i, j), board[i][j])             #更新所有的落子图像
       # self.put_tip_stone(self.othello., current_player_color)
        blacks_str = '%02d ' % int(blacks)
        whites_str = '%02d ' % int(whites)
        self.showScore(blacks_str, whites_str, current_player_color)#更新计分板
        pygame.display.flip()

    def showScore(self, blackStr, whiteStr, current_player_color):
        """ 显示计分板功能 """
        black_background = self.BLUE if current_player_color == BLACK else self.BACKGROUND
        white_background = self.BLUE if current_player_color == WHITE else self.BACKGROUND #需要落子的一方计分板高亮
        text = self.scoreFont.render(blackStr, True, self.BLACK, black_background)
        text2 = self.scoreFont.render(whiteStr, True, self.WHITE, white_background)
        self.screen.blit(text, (self.BLACK_LAB_POS[0], self.BLACK_LAB_POS[1] + 40))
        self.screen.blit(text2, (self.WHITE_LAB_POS[0], self.WHITE_LAB_POS[1] + 40))

    def wait_quit(self):
        """ 等待用户关闭窗口 """
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                break

    def show_valid_moves(self, valid_moves):
        """ 提示可以落子的地方 """
        for move in valid_moves:
            self.put_stone(move, 'tip')

    def clear_board(self, valid_moves, board):
        """ 清除落子，配合show_valid_moves()使用 """
        for move in valid_moves:
            x, y = move
            if board.board[x][y] == EMPTY:
                self.put_stone(move, 'nada')

