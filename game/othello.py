""" 游戏核心循环 """

import pygame
import ui
import player
import board
import threading
from config import BLACK, WHITE, HUMAN, COMPUTER, AI, COMBINATION

'''class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args
        self.setDaemon(True)
        self.start()  # 在这里开始
    def run(self):
        self.func(*self.args)'''


class Othello(object):
    """ 游戏核心类 """

    def __init__(self):
        """ 主屏幕展示和开始页面 """
        # 开始游戏
        self.gui = ui.Gui()
        self.board = board.Board()
        self.gui.show_menu(self.start)

    def start(self, *args):
        """ 开始游戏设置 """
        player1, player2, level = args
        # 玩家选边设置，now_playing一般为黑子先手，other_player为后手
        if player1 == HUMAN and player2 == COMPUTER:
            self.now_playing = player.Human(self.gui, BLACK)
            self.other_player = player.Computer(WHITE, level)
        if player1 == HUMAN and player2 == AI:
            self.now_playing = player.Human(self.gui, BLACK)
            self.other_player = player.AI(WHITE)
        if player1 == HUMAN and player2 == HUMAN:
            self.now_playing = player.Human(self.gui, BLACK)
            self.other_player = player.Human(self.gui, WHITE)
        if player1 == HUMAN and player2 == COMBINATION:
            self.now_playing = player.Human(self.gui, BLACK)
            self.other_player = player.Combination(WHITE, level)
        if player1 == COMPUTER and player2 == HUMAN:
            self.now_playing = player.Computer(BLACK, level)
            self.other_player = player.Human(self.gui, WHITE)
        if player1 == COMPUTER and player2 == AI:
            self.now_playing = player.Computer(BLACK, level)
            self.other_player = player.AI(WHITE)
        if player1 == COMPUTER and player2 == COMPUTER:
            self.now_playing = player.Computer(BLACK, level)
            self.other_player = player.Computer(WHITE, level)
        if player1 == COMPUTER and player2 == COMBINATION:
            self.now_playing = player.Computer(BLACK, level)
            self.other_player = player.Combination(WHITE, level)
        if player1 == AI and player2 == HUMAN:
            self.now_playing = player.AI(BLACK)
            self.other_player = player.Human(self.gui, WHITE)
        if player1 == AI and player2 == COMPUTER:
            self.now_playing = player.AI(BLACK)
            self.other_player = player.Computer(WHITE, level)
        if player1 == AI and player2 == AI:
            self.now_playing = player.AI(BLACK)
            self.other_player = player.AI(WHITE)
        if player1 == AI and player2 == COMBINATION:
            self.now_playing = player.AI(BLACK)
            self.other_player = player.Combination(WHITE, level)
        if player1 == COMBINATION and player2 == HUMAN:
            self.now_playing = player.Combination(BLACK, level)
            self.other_player = player.Human(self.gui, WHITE)
        if player1 == COMBINATION and player2 == COMPUTER:
            self.now_playing = player.Combination(BLACK, level)
            self.other_player = player.Computer(WHITE, level)
        if player1 == COMBINATION and player2 == AI:
            self.now_playing = player.Combination(BLACK, level)
            self.other_player = player.AI(WHITE)
        if player1 == COMBINATION and player2 == COMBINATION:
            self.now_playing = player.Combination(BLACK, level)
            self.other_player = player.Combination(WHITE, level)

        self.gui.show_game()
        self.gui.update(self.board.board, 2, 2, self.now_playing.color)  # 更新屏幕开始游戏

    def run(self):
        """ 游戏运行设置 """
        clock = pygame.time.Clock()  # 创建时钟对象
        while True:
            clock.tick(60)  # 通过时钟对象，指定循环频率，每秒循环60次
            if self.board.game_ended():  # 首先判断游戏是否结束
                whites, blacks, empty = self.board.count_stones()
                if whites > blacks:  # 判断是否产生获胜者
                    winner = WHITE
                elif blacks > whites:
                    winner = BLACK
                else:
                    winner = None
                break
            self.now_playing.get_current_board(self.board)
            valid_moves = self.board.get_valid_moves(self.now_playing.color)
            self.gui.show_valid_moves(valid_moves)  # 高亮可以落子的区域
            if valid_moves != []:
                score, self.board = self.now_playing.get_move()
                whites, blacks, empty = self.board.count_stones()
                self.blacks_str2 = '%02d ' % int(blacks)
                self.whites_str2 = '%02d ' % int(whites)
            self.now_playing, self.other_player = self.other_player, self.now_playing
            self.gui.update(self.board.board, blacks, whites, self.now_playing.color)
            self.gui.clear_board(valid_moves, self.board)  # 交换双方操作权，并更新分数板
        self.gui.show_end(winner, self.blacks_str2, self.whites_str2)
        self.restart()

    def restart(self):
        """ 再来一局 """
        self.board = board.Board()
        self.gui.show_menu(self.start)
        self.run()


def main():
    game = Othello()
    pygame.init()
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
